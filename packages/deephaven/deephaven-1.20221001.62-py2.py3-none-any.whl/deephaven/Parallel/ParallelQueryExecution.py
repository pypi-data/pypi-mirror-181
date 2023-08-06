#
# Copyright (c) 2016-2021 Deephaven Data Labs and Patent Pending
#

"""Class for executing parallel workers"""

import base64
import dill
import jpy
import threading
import time

import deephaven

GIGABYTE = 1024.0 * 1024.0 * 1024.0
NO_WORK_AVAILABLE = -1

def get_worker_name(db):
    remote_db_type = jpy.get_type('com.illumon.iris.db.tables.remote.RemoteDatabase')
    maybe_remote = jpy.cast(db, remote_db_type)
    if isinstance(maybe_remote, remote_db_type):
        return db.getProcessorConnection().getProcessorName()
    else:
        return db.getWorkerName()


class ParallelQueryExecution(object):
    """
    Parallel Execution handle
    """

    def __init__(self,
                 query,
                 default,
                 params,
                 allow_deflate=True,
                 keep_alive=False,
                 scope_map=None,
                 max_workers=-1,
                 max_heap=-1,
                 jvm_properties=None,
                 max_outstanding=None
                 ):
        """
        Constructs a new Parallel Execution instance. The provided query will not be executed until the object's
        `execute(db)` method is called
        :param query: a class which implements `execute_query(db, param)`, `execute_reduce(db, previous, new)`, and optionally `execute_default(db, param)`
        :param default: a default/initial value used in the reduction method. If the optional `execute_default(db, param)` method is implemented, this value will be passed to the method for retrieval of the default value
        :param params: a list of serializable parameters, each of which will be passed in to `execute_query(db, param)`
        :param allow_deflate: identifies if deflatable return-values from workers should be deflated or serialized as-is
        :param keep_alive: identifies if the sub-workers should be auto-terminated upon completion of the reduction. If set to True, the user must call this instance's `close_dbs()` to terminate the downstream workers
        :param scope_map: an optional list of name->serializable_python_object, which will be pushed to each downstream worker's python-scope
        :param max_workers: an optional maximum number of sub-workers created by the main worker. If not supplied, the number is based on the number of input parameters, with a system-defined maximum
        :param max_heap: an optional maximum heap (in MB) of downstream workers. If not supplied, the current worker max-heap will be used
        :param jvm_properties: an optional list of jvm-properties used in the initialization of downstream workers
        :param max_outstanding: the maximum number of outstanding reductions to perform, default 2*max_workers.  Set to 0 for no limit
        :return: a new instance of this class
        """
        if jvm_properties is None:
            jvm_properties = []
        self.query_class = query
        self.default = default
        self.params = params
        self.allow_deflate = allow_deflate
        self.keep_alive = keep_alive
        if scope_map is None:
            self.scope_statement = None
        else:
            self.scope_statement = "import dill\nimport base64\n"
            for key in scope_map:
                self.scope_statement = self.scope_statement + str(
                    key) + " = dill.loads(base64.b64decode(\"" + base64.b64encode(
                    dill.dumps(scope_map[key])).decode() + "\"))\n"

        self.log = deephaven.Logger()
        self.max_workers = min(len(params),
                               max_workers if max_workers > 0 else deephaven.Config().getIntegerWithDefault(
                                   "ParallelQueryExecution.defaultMaxWorkers", 10))

        if max_outstanding is None:
            self.max_outstanding = 2 * max_workers

        # if user passed in a max_heap, store that. else grab the max_heap of the current worker. this will be used as
        # our sub-worker's max_heap
        from math import ceil
        self.max_heap = int(ceil(jpy.get_type(
            "java.lang.Runtime").getRuntime().maxMemory() / GIGABYTE) * 1024 if max_heap <= 0 else max_heap)
        self.jvm_properties = jvm_properties.copy()
        if deephaven.Config().hasProperty('jpy.env'):
            self.jvm_properties.append("-Djpy.env=" + str(deephaven.Config().getProperty('jpy.env')))

        self.query_futures = [None] * len(self.params)
        self.remote_dbs = [None] * self.max_workers
        self.worker_param_idx = [None] * self.max_workers
        self.warn_active = False

    def execute(self, db):
        """
        Starts parallel execution of the provided query
        :param db: the `db` instance within the current worker's scope
        :return: the results of the query, after reducing the results of all parameterized query-executions
        """
        self.log.debug().append("In ParallelQueryExecution...").endl()
        if self.params is None or len(self.params) < 1:
            self.log.warn().append("No parameters detected").endl()
            return

        try:
            query = self.query_class()
            # initialize the result; via method (if available), or straight from the user-defined default
            result = query.execute_default(db, self.default) if hasattr(query, 'execute_default') else self.default
            threads = []

            # spawn a number of downstream worker instances in parallel
            for i in range(self.max_workers):
                self.log.info().append("Spawning Worker: ").append(str(i)).endl()
                new_thread = threading.Thread(target=self.spawn_worker, args=(db.getServerHost(), i))
                new_thread.setDaemon(True)
                threads.append(new_thread)
                new_thread.start()

            # wait for all remote-db instances to start (or fail)...
            for thread in threads:
                thread.join()

            # if any remote-db instances are failed, we cannot continue. force termination, with remote-worker cleanup
            for maybe_exception in self.remote_dbs:
                if isinstance(maybe_exception, Exception):
                    raise maybe_exception
                else:
                    self.log.info().append("Started Worker: ").append(get_worker_name(maybe_exception)).endl()

            # The spawn_worker method will also kick off work for each worker, so if we get this far, then
            # we know that at most max_workers work has been assigned and can start there for future assignments
            next_work_idx = min(self.max_workers, len(self.params))

            # This list will keep track of what set of parameters each worker is actively working on so we can collate
            # the results properly

            result_cache = [None] * len(self.params)
            result_worker_cache = [None] * len(self.params)

            next_reduction_index = 0
            num_pending_reductions = 0
            while next_reduction_index < len(self.params):
                for worker_idx, remote_db in enumerate(self.remote_dbs):
                    param_idx = self.worker_param_idx[worker_idx]
                    # If param_idx < 0 then the worker was idle and we should not revisit it.
                    if param_idx < 0:
                        continue

                    future_result = self.query_futures[param_idx]
                    if future_result is not None:
                        # First check to see if any failed on assignment.
                        if isinstance(future_result, Exception):
                            raise future_result

                        # This worker isn't done, so just move on
                        if not future_result.isReady():
                            continue

                        self.query_futures[param_idx] = None

                        # Get the completed work
                        param_str = self.get_param_str(param_idx)
                        worker_name = get_worker_name(remote_db)
                        new_result = future_result.get()
                        self.log.debug().append("Fetched Result; Param: ").append(param_str).append(" on Worker: ") \
                            .append(worker_name).endl()

                        # maybe inflate/unpickle the result before handing off to the reduction method
                        if isinstance(new_result, Exception):
                            raise new_result
                        elif isinstance(new_result, jpy.get_type("com.illumon.iris.db.tables.remote.Inflatable")) \
                                or isinstance(new_result, jpy.get_type(
                            "com.illumon.iris.db.tables.remote.ExportedTableDescriptorMessage")):
                            new_result = new_result.inflate(remote_db.getProcessorConnection())
                        elif isinstance(new_result,
                                        jpy.get_type("com.illumon.iris.db.util.PythonRemoteQuery$PickledResult")):
                            new_result = dill.loads(base64.b64decode(new_result.getPickled()))

                        # save off the result for reduction
                        result_cache[param_idx] = new_result
                        result_worker_cache[param_idx] = worker_idx
                        num_pending_reductions += 1

                    if 0 < self.max_outstanding <= num_pending_reductions:
                        if not self.warn_active:
                            self.log.warn() \
                                .append("Maximum pending reductions reached, not assigning further work").endl()
                            self.warn_active = True
                    else:
                        self.warn_active = False
                        if next_work_idx < len(self.params):
                            self.execute_sub_query(worker_idx, next_work_idx)
                            next_work_idx += 1
                        else:
                            self.worker_param_idx[worker_idx] = -1

                # Do any reductions that we can do
                while next_reduction_index < len(self.params) and result_cache[next_reduction_index] is not None:
                    param_str = self.get_param_str(next_reduction_index)
                    new_result = result_cache[next_reduction_index]

                    # Release the result so it can be cleaned up.  Note that the query itself is responsible
                    # for doing any cleanup (closing tables, etc.) during the reduce phase.
                    result_cache[next_reduction_index] = None
                    self.log.info().append("Reducing; Param: ").append(param_str).append(" Value: ") \
                        .append(str(new_result)).append(" Pending: ").append(num_pending_reductions).endl()
                    result = query.execute_reduce(
                        self.remote_dbs[result_worker_cache[next_reduction_index]], result, new_result)
                    next_reduction_index += 1
                    num_pending_reductions -= 1

                if next_reduction_index < len(self.params):
                    time.sleep(1)

        except Exception as e:
            self.log.warn().append("Exception: ").append(str(e)).endl()
            self.keep_alive = False
            result = e
        finally:
            if not self.keep_alive:
                self.close_dbs()

        return result

    def spawn_worker(self, host, idx):
        """
        Used internally to spawn a downstream worker instance
        """
        try:
            self.log.info().append("Launching SubWorker with maxHeap=") \
                .append(str(self.max_heap)).append(", jvm_properties=") \
                .append(str(self.jvm_properties)).endl()
            rqc = deephaven.RemoteQueryClient(host, deephaven.Config()
                                              .getInteger("RemoteQueryDispatcherParameters.queryPort"))
            self.remote_dbs[idx] = rqc.getRemoteDB(self.max_heap, "Default") \
                if not len(self.jvm_properties) else rqc.getRemoteDB(self.max_heap, "Default", *self.jvm_properties)

            # Automatically launch work on the worker as soon as it is available
            self.execute_sub_query(idx, idx)
        except Exception as e:
            self.log.warn().append("Exception for SubWorker ").append(idx).append("; ").append(str(e)).endl()
            self.remote_dbs[idx] = e

    def get_param_str(self, idx):
        param = self.params[idx]
        if hasattr(param, 'jclass'):
            # this is a java type; we could allow the .toString() of the object to be used, but that can be unsafe (like
            # in the case of an Index, etc). instead, simply return the class & index for logging purposes
            return '{ ' + str(param.jclass) + '[' + str(idx) + '] }'
        else:
            # this is a native python type. ensure the returned "string" isn't too long
            param_str = str(param)
            if len(param_str) > 100:
                return param_str[:97] + '...'
            else:
                return param_str

    def push_scope(self, db, identity=None):
        """
        Used internally to serialize python-scope objects to downstream worker instances
        """
        if self.scope_statement is None:
            return

        if identity is not None:
            self.log.info().append(identity).endl()
        db.executeQuery(deephaven.PythonEvalQuery(self.scope_statement))

    def execute_sub_query(self, worker_idx, param_idx):
        """
        Used internally to start execution of work for a specific parameter on a remote worker
        """
        db = self.remote_dbs[worker_idx]
        param_str = self.get_param_str(param_idx)
        worker_name = get_worker_name(db)
        self.log.info().append("Starting Execution; Param: ").append(param_str).append(" on Worker: ") \
            .append(worker_name).endl()
        try:
            self.push_scope(db, identity="PushScope for Param: " + param_str + "/" + worker_name)
            self.log.info().append("Pushing Param: ").append(param_str).append(" to ").append(worker_name).endl()
            pickled = dill.dumps(ExecutionWrapper(self.query_class, self.params[param_idx]), recurse=True)
            self.log.info().append("ExecuteQuery for Param: ").append(param_str).append("/").append(worker_name).endl()
            self.worker_param_idx[worker_idx] = param_idx
            self.query_futures[param_idx] = db.getProcessorConnection().executeQueryAsync(
                deephaven.PythonRemoteQuery(pickled).setAutoDeflate(self.allow_deflate), True)
        except Exception as e:
            self.log.warn().append("Exception for Param: ").append(param_str).append("/").append(worker_name) \
                .append("; reason: ").append(str(e)).endl()
            self.query_futures[param_idx] = e
            self.worker_param_idx[worker_idx] = -1

    def close_dbs(self):
        """
        Closes remote DB connections, effectively terminating downstream workers
        """
        remote_db_type = jpy.get_type('com.illumon.iris.db.tables.remote.RemoteDatabase')

        for remote_db in self.remote_dbs:
            if remote_db is not None:
                maybe_remote = jpy.cast(remote_db, remote_db_type)
                if isinstance(maybe_remote, remote_db_type):
                    remote_db.shutdown()
                else:
                    self.log.warn().append("Not Closing DB: ").append(str(remote_db)).endl()


class ExecutionWrapper(object):
    """
    Used internally to serialize query and parameter to downstream worker instance
    """

    def __init__(self, query, param):
        self.execute_query = query.execute_query
        self.param = param

    def __getstate__(self):
        state = {'execute_query': self.execute_query, 'param': self.param}
        deephaven.Logger().debug().append("In ExecutionWrapper.__getstate__(...): ").append(str(state)).endl()
        return state

    def __setstate__(self, state):
        deephaven.Logger().debug().append("In ExecutionWrapper.__setstate__(...): ").append(str(state)).endl()
        self.execute_query = state['execute_query']
        self.param = state['param']
        # see https://github.com/uqfoundation/dill/issues/219
        self.execute_query.__globals__["__builtins__"] = globals()["__builtins__"]

    def execute(self, db):
        deephaven.Logger().debug().append("In ExecutionWrapper.execute(" + str(db)).append(", ") \
            .append(str(self.param)).append(")...").endl()
        return self.execute_query(None, db, self.param)


class RemoteParallelQuery:
    """
    Used internally by client-level (as opposed to server/worker-level) python scripts to start parallel execution
    """

    def execute(self, db):
        deephaven.Logger().info().append("Running RemoteParallelQuery.execute(...); ") \
            .append(str(deephaven.__default__)).endl()
        return ParallelQueryExecution(deephaven.__query__, deephaven.__default__, deephaven.__param_list__).execute(db)
