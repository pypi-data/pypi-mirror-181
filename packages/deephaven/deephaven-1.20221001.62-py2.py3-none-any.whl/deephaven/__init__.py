#
# Copyright (c) 2016-2019 Deephaven Data Labs and Patent Pending
#

"""
Main Deephaven python module.

For convenient usage in the python console, the main sub-packages of deephaven have been imported here with aliases:

* Calendars imported as cals

* ComboAggregateFactory imported as caf

* DBTimeUtils imported as dbtu

* MovingAverages imported as mavg

* npy as npy

* Plot imported as plt

* QueryScope imported as qs

* TableManagementTools imported as tmt

* TableTools imported as ttools *(`tt` is frequently used for time table)*

Additionally, the following methods have been imported into the main deephaven namespace:

* from Plot import figure_wrapper as figw

* from java_to_python import tableToDataFrame, columnToNumpyArray, convertJavaArray

* from python_to_java import dataFrameToTable, createTableFromData

* from conversion_utils import convertToJavaArray, convertToJavaList, convertToJavaArrayList,
       convertToJavaHashSet, convertToJavaHashMap

* from ExportTools import JdbcLogger, TableLoggerBase

* from ImportTools import CsvImport, DownsampleImport, JdbcHelpers, JdbcImport, JsonImport,
       MergeData, XmlImport

* from InputTableTools import InputTable, TableInputHandler, LiveInputTableEditor

* from Parallel imported as para

* from TableManipulation import ColumnRenderersBuilder, DistinctFormatter,
       DownsampledWhereFilter, LayoutHintBuilder, PersistentQueryTableHelper, PivotWidgetBuilder,
       SmartKey, SortPair, TotalsTableBuilder, WindowCheck

For ease of namespace population in a python console, consider::

>>> from deephaven import *  # this will import the submodules into the main namespace
>>> print(dir())  # this will display the contents of the main namespace
>>> help(plt)  # will display the help entry (doc strings) for the illumon.iris.plot module
>>> help(columnToNumpyArray)  # will display the help entry for the columnToNumpyArray method
"""

__all__ = [
    "PythonFunction", "PythonListenerAdapter", "PythonShiftAwareListenerAdapter",
    "TableListenerHandle", "listen", "doLocked",  # from here

    "DeephavenDb",  # from DeephavenDb

    "convertJavaArray", "tableToDataFrame", "columnToNumpyArray",  # from java_to_python

    "createTableFromData", "dataFrameToTable",  # from python_to_java

    "convertToJavaArray", "convertToJavaList", "convertToJavaArrayList", "convertToJavaHashSet",
    "convertToJavaHashMap",  # from conversion_utils

    'JdbcLogger',  'TableLoggerBase',  # from ExportTools

    'CsvImport', 'DownsampleImport', 'JdbcHelpers', 'JdbcImport', 'JsonImport', 'MergeData',
    'XmlImport',  # from ImportTools

    'InputTable', 'TableInputHandler', 'LiveInputTableEditor',  # from InputTableTools

    'ParallelQueryExecution',  # from Parallel

    'ColumnRenderersBuilder', 'DistinctFormatter', 'DownsampledWhereFilter', 'LayoutHintBuilder',
    'PersistentQueryTableHelper', 'PersistentQueryControllerClient', 'PivotWidgetBuilder', 'SmartKey',
    'SortPair', 'TotalsTableBuilder', 'WindowCheck',  # from TableManipulation

    "cals", "caf", "dbtu", "figw", "mavg", "npy", "plt", "qs", "tmt", "ttools"  # subpackages with abbreviated names
]

import jpyutil
jpyutil.preload_jvm_dll()
import jpy
import sys
import base64  # builtin
import inspect

import wrapt  # dependencies
import dill

from .ImportTools import *
from .ExportTools import *
from .InputTableTools import *
from .Parallel import *
from .TableManipulation import *

from .DeephavenDb import DeephavenDb
from .java_to_python import convertJavaArray, tableToDataFrame, columnToNumpyArray
from .python_to_java import dataFrameToTable, createTableFromData
from .conversion_utils import convertToJavaArray, convertToJavaList, convertToJavaArrayList, convertToJavaHashSet, \
    convertToJavaHashMap, getJavaClassObject

from . import Calendars as cals, \
    ComboAggregateFactory as caf, \
    DBTimeUtils as dbtu, \
    MovingAverages as mavg, \
    npy, \
    Plot as plt, \
    QueryScope as qs, \
    TableManagementTools as tmt, \
    TableTools as ttools, \
    Parallel as para

from .Plot import figure_wrapper as figw


# NB: this must be defined BEFORE importing .jvm_init or .start_jvm (circular import)
def initialize():
    __initializer__(jpy.get_type("com.fishlib.configuration.Configuration"), Config)
    __initializer__(jpy.get_type("com.illumon.iris.db.tables.remotequery.RemoteQueryClient"), RemoteQueryClient)
    __initializer__(jpy.get_type("com.illumon.iris.db.util.PythonRemoteQuery"), PythonRemoteQuery)
    __initializer__(jpy.get_type("com.illumon.iris.db.util.PythonRemoteQuery$PickledResult"), PythonRemoteQueryPickledResult)
    __initializer__(jpy.get_type("com.illumon.iris.db.util.PythonPushClassQuery"), PythonPushClassQuery)
    __initializer__(jpy.get_type("com.illumon.iris.db.util.PythonEvalQuery"), PythonEvalQuery)
    __initializer__(jpy.get_type("com.illumon.iris.db.tables.remote.RemoteDatabase"), RemoteDatabase)
    __initializer__(jpy.get_type("com.illumon.iris.db.tables.remote.Inflatable"), Inflatable)
    __initializer__(jpy.get_type("com.illumon.iris.db.tables.remote.ExportedTableDescriptorMessage"), ExportedTableDescriptorMessage)
    __initializer__(jpy.get_type("com.illumon.integrations.python.PythonListenerAdapter"), PythonListenerAdapter)
    __initializer__(jpy.get_type("com.illumon.integrations.python.PythonFunction"), PythonFunction)

    # ensure that all the symbols are called and reimport the broken symbols
    cals._defineSymbols()
    caf._defineSymbols()
    dbtu._defineSymbols()
    mavg._defineSymbols()
    plt._defineSymbols()
    figw._defineSymbols()
    qs._defineSymbols()
    tmt._defineSymbols()
    ttools._defineSymbols()
    para._defineSymbols()
    import deephaven.npy.table2numpy
    deephaven.npy.table2numpy._defineSymbols()

    import deephaven.ExportTools
    deephaven.ExportTools._defineSymbols()
    global TableLoggerBase
    from deephaven.ExportTools import TableLoggerBase
    JdbcLogger._defineSymbols()

    CsvImport._defineSymbols()
    DownsampleImport._defineSymbols()
    JdbcHelpers._defineSymbols()
    JdbcImport._defineSymbols()
    JsonImport._defineSymbols()
    MergeData._defineSymbols()
    XmlImport._defineSymbols()

    import deephaven.InputTableTools
    deephaven.InputTableTools._defineSymbols()
    global LiveInputTableEditor
    from deephaven.InputTableTools import LiveInputTableEditor
    InputTable._defineSymbols()
    TableInputHandler._defineSymbols()

    import deephaven.TableManipulation
    deephaven.TableManipulation._defineSymbols()
    global ColumnRenderersBuilder, DistinctFormatter, DownsampledWhereFilter, LayoutHintBuilder, \
        PivotWidgetBuilder, SmartKey, SortPair, TotalsTableBuilder
    from deephaven.TableManipulation import ColumnRenderersBuilder, DistinctFormatter, \
        DownsampledWhereFilter, LayoutHintBuilder, PivotWidgetBuilder, SmartKey, SortPair, \
        TotalsTableBuilder

    PersistentQueryTableHelper._defineSymbols()
    WindowCheck._defineSymbols()

    global Figure, PlottingConvenience
    Figure = FigureUnsupported
    PlottingConvenience = FigureUnsupported

    jpy.type_translations['com.illumon.iris.db.tables.remote.RemoteDatabase'] = wrap_db


from .jvm_init import jvm_init
from .start_jvm import start_jvm


Figure = None  # variable for initialization
PlottingConvenience = None  # variable for initialization


def verifyPicklingCompatibility(otherPythonVersion):
    """
    Check a provided python version string versus the present instance string for pickling safety.

    :param otherPythonVersion: other version string
    :return: True is safe, False otherwise
    """

    if otherPythonVersion is None:
        return False
    sPyVer = otherPythonVersion.split('.')
    if len(sPyVer) < 3:
        return False
    try:
        major, minor = int(sPyVer[0]), int(sPyVer[1])
        # We need both major and minor agreement for pickling compatibility
        return major == sys.version_info[0] and minor == sys.version_info[1]
    except Exception:
        return False


class DbWrapper(wrapt.ObjectProxy):
    def executeQuery(self, query, concurrent=False, execute_async=False):
        pickled = dill.dumps(query)
        return self.executeRemoteQuery(PythonRemoteQuery(pickled), concurrent=concurrent, execute_async=execute_async)  # note that the protocol flag doesn't help with cross compatibility

    def executeRemoteQuery(self, remoteQuery, concurrent=False, execute_async=False):
        if execute_async:
            qpc = self.__wrapped__.getProcessorConnection()
            res = qpc.executeQueryAsync(remoteQuery, concurrent).get()
        else:
            if concurrent: print("Executing Concurrent")
            res = self.__wrapped__.executeQuery(remoteQuery) if not concurrent else self.__wrapped__.executeConcurrentQuery(remoteQuery)
        return self.inflateResult(res)

    def executeQueryParallel(self, query, default, parameter_list):
        if not hasattr(query, 'execute_query') or not hasattr(query, 'execute_reduce'):
            raise RuntimeError("Missing required query attribute:  " + "execute_reduce" if hasattr(query, 'execute_query') else "execute_query")

        self.eval("import deephaven")

        # push the query class to the server, and instantiate
        self.pushClass(query)
        self.eval("deephaven.__query__ = " + query.__name__)

        # serialize/deserialize these to the server as well-defined variable-names in the deephaven module
        self.pushObject("deephaven.__default__", default)
        self.pushObject("deephaven.__param_list__", parameter_list)

        # execute the query, which will use the now-serialized members
        return self.executeQuery(para.ParallelQueryExecution.RemoteParallelQuery())

    def pushClass(self, classToDefine, concurrent=False, execute_async=False):
        if not inspect.isclass(classToDefine):
            raise TypeError("{} is not a class!".format(classToDefine))

        name = classToDefine.__name__
        pickled = dill.dumps(classToDefine)
        pushQuery = PythonPushClassQuery(name, pickled)
        self.executeRemoteQuery(pushQuery, concurrent=concurrent, execute_async=execute_async)

    def eval(self, string, concurrent=False, execute_async=False):
        evalQuery = PythonEvalQuery(string)
        self.executeRemoteQuery(evalQuery, concurrent=concurrent, execute_async=execute_async)

    def pushObject(self, an_attribute, an_object, concurrent=False, execute_async=False):
        self.eval(an_attribute + " = dill.loads(base64.b64decode(\"" + base64.b64encode(dill.dumps(an_object)).decode() + "\"))", concurrent=concurrent, execute_async=execute_async)

    def fetch(self, name):
        fetchQuery = PythonEvalQuery(name)
        res = self.__wrapped__.executeQuery(fetchQuery)
        return self.inflateResult(res)

    def inflateResult(self, obj):
        if isinstance(obj, jpy.get_type("com.illumon.iris.db.tables.remote.Inflatable")):
            return obj.inflate(self.__wrapped__.getProcessorConnection())
        elif isinstance(obj, jpy.get_type("com.illumon.iris.db.tables.remote.ExportedTableDescriptorMessage")):
            return obj.inflate(self.__wrapped__.getProcessorConnection())
        elif isinstance(obj, jpy.get_type("com.illumon.iris.db.util.PythonRemoteQuery$PickledResult")):
            if not verifyPicklingCompatibility(obj.getPythonVersion()):
                raise RuntimeError("Attempting to inflate a result pickled using a python version instance {} "
                                   "on the present python version instance {}. These versions are incompatible for "
                                   "serialization/pickling.".format(obj.getPythonVersion(), sys.version))
            return dill.loads(base64.b64decode(obj.getPickled()))
        else:
            return obj

    def importClass(self, classToImport):
        if isinstance(classToImport, str):
            classToImport = getJavaClassObject(classToImport)
        elif hasattr(classToImport, 'jclass'):
            classToImport = classToImport.jclass
        self.__wrapped__.importClass(classToImport)


class FigureUnsupported(object):
    def __init__(self):
        raise Exception("Can not create a plot outside of the console.")


def __initializer__(jtype, obj):
    for key, value in jtype.__dict__.items():
        obj.__dict__.update({key: value})


def wrap_db(type, obj):
    return DbWrapper(obj)


def AuthenticationManager():
    return jpy.get_type("com.fishlib.auth.WAuthenticationClientManager")


def RemoteQueryClient(*args):
    jtype = jpy.get_type("com.illumon.iris.db.tables.remotequery.RemoteQueryClient")
    if len(args) > 2:
        return jtype(args[:3])
    else:
        return jtype(*args)


def PythonRemoteQuery(dilledObject):
    return jpy.get_type("com.illumon.iris.db.util.PythonRemoteQuery")(dilledObject, sys.version)


def PythonRemoteQueryPickledResult(pickled):
    return jpy.get_type("com.illumon.iris.db.util.PythonRemoteQuery$PickledResult")(pickled, sys.version)


def PythonPushClassQuery(name, dilledObject):
    return jpy.get_type("com.illumon.iris.db.util.PythonPushClassQuery")(name, dilledObject, sys.version)


def PythonEvalQuery(string):
    return jpy.get_type("com.illumon.iris.db.util.PythonEvalQuery")(string)


def RemoteDatabase(processorConnection):
    return jpy.get_type("com.illumon.iris.db.tables.remote.RemoteDatabase")(processorConnection)


def Inflatable():  # what purpose does this serve?
    return jpy.get_type("com.illumon.iris.db.tables.remote.Inflatable")


def ExportedTableDescriptorMessage(id):
    return jpy.get_type("com.illumon.iris.db.tables.remote.ExportedTableDescriptorMessage")(id)


def Config():
    return jpy.get_type("com.fishlib.configuration.Configuration").getInstance()


def Logger():
    return jpy.get_type("com.fishlib.util.process.ProcessEnvironment").getDefaultLog()


def PythonListenerAdapter(dynamicTable, implementation, description=None, retain=True, replayInitialImage=False):
    """
    Constructs the InstrumentedListenerAdapter, implemented in Python, and plugs it into the table's
    listenForUpdates method.

    :param dynamicTable: table to which to listen - NOTE: it will be cast to DynamicTable.
    :param implementation: the body of the implementation for the InstrumentedListenerAdapter.onUpdate method, and
      must either be a class with onUpdate method or a callable.
    :param description: A description for the UpdatePerformanceTracker to append to its entry description.
    :param retain: Whether a hard reference to this listener should be maintained to prevent it from being collected.
    :param replayInitialImage: False to only process new rows, ignoring any previously existing rows in the Table;
      True to process updates for all initial rows in the table PLUS all new row changes.
    """

    dt = jpy.cast(dynamicTable, jpy.get_type('com.illumon.iris.db.v2.DynamicTable'))
    jtype = jpy.get_type('com.illumon.integrations.python.PythonListenerAdapter')
    ListenerInstance = jtype(description, dynamicTable, retain, implementation)
    dt.listenForUpdates(ListenerInstance, replayInitialImage)


def PythonShiftAwareListenerAdapter(dynamicTable, implementation, description=None, retain=True):
    """
    Constructs the InstrumentedShiftAwareListenerAdapter, implemented in Python, and plugs it into the table's
    listenForUpdates method.

    :param dynamicTable: table to which to listen - NOTE: it will be cast to DynamicTable.
    :param implementation: the body of the implementation for the InstrumentedShiftAwareListenerAdapter.onUpdate method, and
      must either be a class with onUpdate method or a callable.
    :param description: A description for the UpdatePerformanceTracker to append to its entry description.
    :param retain: Whether a hard reference to this listener should be maintained to prevent it from being collected.
    """

    jtype = jpy.get_type('com.illumon.integrations.python.PythonShiftAwareListenerAdapter')
    dt = jpy.cast(dynamicTable, jpy.get_type('com.illumon.iris.db.v2.DynamicTable'))
    ListenerInstance = jtype(description, dt, retain, implementation)
    dt.listenForUpdates(ListenerInstance)


def PythonFunction(func, classString):
    """
    Constructs a Java Function<PyObject, Object> implementation from the given python function `func`. The proper
    Java object interpretation for the return of `func` must be provided.

    :param func: Python callable or class instance with `apply` method (single argument)
    :param classString: the fully qualified class path of the return for `func`. This is really anticipated to be one
                        of `java.lang.String`, `double`, 'float`, `long`, `int`, `short`, `byte`, or `boolean`,
                        and any other value will result in `java.lang.Object` and likely be unusable.
    :return: com.illumon.integrations.python.PythonFunction instance, primarily intended for use in PivotWidgetBuilder usage
    """

    jtype = jpy.get_type('com.illumon.integrations.python.PythonFunction')
    return jtype(func, getJavaClassObject(classString))


class TableListenerHandle:
    """
    A handle for a table listener.
    """

    def __init__(self, t, listener):
        """
        Creates a new table listener handle.

        :param t: dynamic table being listened to.
        :param listener: listener object.
        """
        self.t = t
        self.listener = listener
        self.isRegistered = False


    def register(self):
        """
        Register the listener with the table and listen for updates.
        """

        if self.isRegistered:
            raise RuntimeError("Attempting to register an already registered listener..")

        self.t.listenForUpdates(self.listener)

        self.isRegistered = True


    def deregister(self):
        """
        Deregister the listener from the table and stop listening for updates.
        """

        if not self.isRegistered:
            raise RuntimeError("Attempting to deregister an unregistered listener..")

        self.t.removeUpdateListener(self.listener)
        self.isRegistered = False


def _nargsListener(listener):
    """
    Returns the number of arguments the listener takes.

    :param listener: listener
    :return: number of arguments the listener takes.
    """

    if callable(listener):
        f = listener
    elif hasattr(listener, 'onUpdate'):
        f = listener.onUpdate
    else:
        raise ValueError("Listener is neither callable nor has an 'onUpdate' method")

    if sys.version[0] == "2":
        import inspect
        return len(inspect.getargspec(f).args)
    elif sys.version[0] == "3":
        from inspect import signature
        return len(signature(f).parameters)
    else:
        raise NotImplementedError("Unsupported python version: version={}".format(sys.version))


def listen(t, listener, description=None, retain=True, ltype="auto", start_listening=True, replay_initial=False, lock_type="shared"):
    """
    Listen to table changes.

    Table change events are processed by listener, which can be either (1) a callable (e.g. function) or
    (2) an object which provides an "onUpdate" method.
    In either case, the method must have one of the following signatures.

    * (added, removed, modified): legacy
    * (isReplay, added, removed, modified): legacy + replay
    * (update): shift-aware
    * (isReplay, update): shift-aware + replay

    For legacy listeners, added, removed, and modified are the indices of the rows which changed.
    For shift-aware listeners, update is an object which describes the table update.
    Listeners which support replaying the initial table snapshot have an additional parameter, inReplay, which is
    true when replaying the initial snapshot and false during normal updates.

    See the Deephaven listener documentation for details on processing update events.  This documentation covers the
    details of the added, removed, and modified indices; index shift information; as well as the details of how to apply
    the update object.  It also has examples on how to access current and previous-tick table values.

    :param t: dynamic table to listen to.
    :param listener: listener to process changes.
    :param description: description for the UpdatePerformanceTracker to append to the listener's entry description.
    :param retain: whether a hard reference to this listener should be maintained to prevent it from being collected.
    :param ltype: listener type.  Valid values are "auto", "legacy", and "shift_aware".  "auto" (default) uses inspection to automatically determine the type of input listener.  "legacy" is for a legacy listener, which takes three (added, removed, modified) or four (isReplay, added, removed, modified) arguments.  "shift_aware" is for a shift-aware listener, which takes one (update) or two (isReplay, update) arguments.
    :param start_listening: True to create the listener and register the listener with the table.  The listener will see updates.  False to create the listener, but do not register the listener with the table.  The listener will not see updates.
    :param replay_initial: True to replay the initial table contents to the listener.  False to only listen to new table changes.  To replay the initial image, the listener must support replay.
    :param lock_type: LTM lock type.  Used when replay_initial=True.  See :func:`doLocked` for valid values.
    :return: table listener handle.
    """

    if replay_initial and not start_listening:
        raise ValueError("Unable to create listener.  Inconsistent arguments.  If the initial snapshot is replayed (replay_initial=True), then the listener must be registered to start listening (start_listening=True).")

    _java_type_DynamicTable = jpy.get_type("com.illumon.iris.db.v2.DynamicTable")
    dt = jpy.cast(t, _java_type_DynamicTable)

    nargs = _nargsListener(listener)

    if ltype == None  or ltype == "auto":
        if nargs == 1 or nargs == 2:
            ltype = "shift_aware"
        elif nargs == 3 or nargs == 4:
            ltype = "legacy"
        else:
            raise ValueError("Unable to autodetect listener type.  Listener does not take an expected number of arguments.  args={}".format(nargs))

    if ltype == "legacy":
        if nargs == 3:
            if replay_initial:
                raise ValueError("Listener does not support replay: ltype={} nargs={}".format(ltype, nargs))

            ListenerAdapter = jpy.get_type("com.illumon.integrations.python.PythonListenerAdapter")
            listener_adapter = ListenerAdapter(description, dt, retain, listener)
        elif nargs == 4:
            ListenerAdapter = jpy.get_type("com.illumon.integrations.python.PythonReplayListenerAdapter")
            listener_adapter = ListenerAdapter(description, dt, retain, listener)
        else:
            raise ValueError("Legacy listener must take 3 (added, removed, modified) or 4 (isReplay, added, removed, modified) arguments.")

    elif ltype == "shift_aware":
        if nargs == 1:
            if replay_initial:
                raise ValueError("Listener does not support replay: ltype={} nargs={}".format(ltype, nargs))

            ListenerAdapter = jpy.get_type("com.illumon.integrations.python.PythonShiftAwareListenerAdapter")
            listener_adapter = ListenerAdapter(description, dt, retain, listener)
        elif nargs == 2:
            ListenerAdapter = jpy.get_type("com.illumon.integrations.python.PythonShiftAwareReplayListenerAdapter")
            listener_adapter = ListenerAdapter(description, dt, retain, listener)
        else:
            raise ValueError("Shift-aware listener must take 1 (update) or 2 (isReplay, update) arguments.")

    else:
        raise ValueError("Unsupported listener type: ltype={}".format(ltype))

    handle = TableListenerHandle(dt, listener_adapter)

    def start():
        if replay_initial:
            listener_adapter.replay()

        if start_listening:
            handle.register()

    if replay_initial:
        doLocked(start, lock_type=lock_type)
    else:
        start()

    return handle


def doLocked(f, lock_type="shared"):
    """
    Executes a function while holding the LiveTableMonitor (LTM) lock.  Holding the LTM lock
    ensures that the contents of a table will not change during a computation, but holding
    the lock also prevents table updates from happening.  The lock should be held for as little
    time as possible.

    :param f: function to execute while holding the LTM lock.  f must be callable or have an apply attribute which is callable.
    :param lock_type: LTM lock type.  Valid values are "exclusive" and "shared".  "exclusive" allows only a single reader or writer to hold the lock.  "shared" allows multiple readers or a single writer to hold the lock.
    """
    ThrowingRunnable = jpy.get_type("com.illumon.integrations.python.PythonThrowingRunnable")
    LiveTableMonitor = jpy.get_type("com.illumon.iris.db.tables.live.LiveTableMonitor")

    if lock_type == "exclusive":
        LiveTableMonitor.DEFAULT.exclusiveLock().doLocked(ThrowingRunnable(f))
    elif lock_type == "shared":
        LiveTableMonitor.DEFAULT.sharedLock().doLocked(ThrowingRunnable(f))
    else:
        raise ValueError("Unsupported lock type: lock_type={}".format(lock_type))
