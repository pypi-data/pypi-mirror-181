
"""
Defines an operation that can be applied to a table with Table.updateBy(Collection, String...)
"""

#
# Copyright (c) 2016-2019 Deephaven Data Labs and Patent Pending
#

##############################################################################
# This code is auto generated. DO NOT EDIT FILE!
# Run "./gradlew :Generators:generatePythonIntegrationStaticMethods" to generate
##############################################################################


import jpy
import wrapt


_java_type_ = None  # None until the first _defineSymbols() call


def _defineSymbols():
    """
    Defines appropriate java symbol, which requires that the jvm has been initialized through the :class:`jpy` module,
    for use throughout the module AT RUNTIME. This is versus static definition upon first import, which would lead to an
    exception if the jvm wasn't initialized BEFORE importing the module.
    """

    if not jpy.has_jvm():
        raise SystemError("No java functionality can be used until the JVM has been initialized through the jpy module")

    global _java_type_
    if _java_type_ is None:
        # This will raise an exception if the desired object is not the classpath
        _java_type_ = jpy.get_type("com.illumon.iris.db.v2.updateby.UpdateByClause")


# every module method should be decorated with @_passThrough
@wrapt.decorator
def _passThrough(wrapped, instance, args, kwargs):
    """
    For decoration of module methods, to define necessary symbols at runtime

    :param wrapped: the method to be decorated
    :param instance: the object to which the wrapped function was bound when it was called
    :param args: the argument list for `wrapped`
    :param kwargs: the keyword argument dictionary for `wrapped`
    :return: the decorated version of the method
    """

    _defineSymbols()
    return wrapped(*args, **kwargs)


# Define all of our functionality, if currently possible
try:
    _defineSymbols()
except Exception as e:
    pass


@_passThrough
def ema(*args):
    """
    **Incompatible overloads text - text from the first overload:**
    
    Create an Exponential Moving Average of the specified columns, using ticks as the decay unit. 
     The formula used is
    
         a = e^(-1 / timeScaleTicks)
         ema_next = a * ema_last + (1 - a) * value
    
    *Overload 1*  
      :param timeScaleTicks: (long) - the decay rate (tau) in ticks
      :param control: (com.illumon.iris.db.v2.updateby.ema.EmaControl.Builder) - a control object that defines how special cases should behave.
                      See EmaControl for further details.
      :param columns: (java.lang.String...) - the columns to apply the EMA to.
      :return: (com.illumon.iris.db.v2.updateby.UpdateByClause) a new UpdateByClause for performing an EMA with Table.updateBy(UpdateByControl, Collection, MatchPair...)
      
    *Overload 2*  
      :param timeScaleTicks: (long) - the decay rate (tau) in ticks
      :param control: (com.illumon.iris.db.v2.updateby.ema.EmaControl) - a control object that defines how special cases should behave.
                      See EmaControl for further details.
      :param columns: (java.lang.String...) - the columns to apply the EMA to.
      :return: (com.illumon.iris.db.v2.updateby.UpdateByClause) a new UpdateByClause for performing an EMA with Table.updateBy(UpdateByControl, Collection, MatchPair...)
      
    *Overload 3*  
      :param timestampColumn: (java.lang.String) - the column in the source table to use for timestamps
      :param timeScaleNanos: (long) - the decay rate (tau) in nanoseconds
      :param control: (com.illumon.iris.db.v2.updateby.ema.EmaControl.Builder) - a control object that defines how special cases should behave.
                      See EmaControl for further details.
      :param columns: (java.lang.String...) - the columns to apply the EMA to.
      :return: (com.illumon.iris.db.v2.updateby.UpdateByClause) a new UpdateByClause for performing an EMA with Table.updateBy(UpdateByControl, Collection, MatchPair...)
      
    *Overload 4*  
      :param timestampColumn: (java.lang.String) - the column in the source table to use for timestamps
      :param timeScaleNanos: (long) - the decay rate (tau) in nanoseconds
      :param control: (com.illumon.iris.db.v2.updateby.ema.EmaControl) - a control object that defines how special cases should behave.
                      See EmaControl for further details.
      :param columns: (java.lang.String...) - the columns to apply the EMA to.
      :return: (com.illumon.iris.db.v2.updateby.UpdateByClause) a new UpdateByClause for performing an EMA with Table.updateBy(UpdateByControl, Collection, MatchPair...)
    """
    return _java_type_.ema(*args)


@_passThrough
def fill(*columnsToFill):
    """
    Create a forward fill operation for the specified columns.
    
    :param columnsToFill: (java.lang.String...) - the columns to fill.
    :return: (com.illumon.iris.db.v2.updateby.UpdateByClause) a new UpdateByClause for performing a forward fill with Table.updateBy(UpdateByControl, Collection, MatchPair...)
    """
    return _java_type_.fill(*columnsToFill)


@_passThrough
def max(*columns):
    """
    Create a Cumulative Maximum of the specified columns.
    
    :param columns: (java.lang.String...) - the columns to find the min
    :return: (com.illumon.iris.db.v2.updateby.UpdateByClause) a new UpdateByClause for performing a cumulative max with Table.updateBy(UpdateByControl, Collection, MatchPair...)
    """
    return _java_type_.max(*columns)


@_passThrough
def min(*columns):
    """
    Create a Cumulative Minimum of the specified columns.
    
    :param columns: (java.lang.String...) - the columns to find the min
    :return: (com.illumon.iris.db.v2.updateby.UpdateByClause) a new UpdateByClause for performing a cumulative min with Table.updateBy(UpdateByControl, Collection, MatchPair...)
    """
    return _java_type_.min(*columns)


@_passThrough
def of(*args):
    """
    **Incompatible overloads text - text from the first overload:**
    
    Conjoin an UpdateBySpec with columns for it to be applied to so the engine can construct
     the proper operators.
    
    *Overload 1*  
      :param spec: (com.illumon.iris.db.v2.updateby.spec.UpdateBySpec) - the UpdateBySpec that defines the operation to perform
      :param columns: (java.lang.String...) - the columns to apply the operation to.
      :return: (com.illumon.iris.db.v2.updateby.ColumnUpdateClause) a ColumnUpdateClause that will be used to construct operations for each column
      
    *Overload 2*  
      :param operations: (com.illumon.iris.db.v2.updateby.UpdateByClause...) - the operations to wrap.
      :return: (java.util.Collection<com.illumon.iris.db.v2.updateby.UpdateByClause>) a collection for use with Table.updateBy(UpdateByControl, Collection, MatchPair...)
    """
    return _java_type_.of(*args)


@_passThrough
def prod(*columns):
    """
    Create a Cumulative Product of the specified columns.
    
    :param columns: (java.lang.String...) - the columns to find the min
    :return: (com.illumon.iris.db.v2.updateby.UpdateByClause) a new UpdateByClause for performing a cumulative produce with Table.updateBy(UpdateByControl, Collection, MatchPair...)
    """
    return _java_type_.prod(*columns)


@_passThrough
def sum(*columnsToSum):
    """
    Create a forward fill operation for the specified columns.
    
    :param columnsToSum: (java.lang.String...) - the columns to fill.
    :return: (com.illumon.iris.db.v2.updateby.UpdateByClause) a new UpdateByClause for performing a forward fill with Table.updateBy(UpdateByControl, Collection, MatchPair...)
    """
    return _java_type_.sum(*columnsToSum)
