
"""
Tools for programmatically executing CSV batch imports.
"""

#
# Copyright (c) 2016-2021 Deephaven Data Labs and Patent Pending
#

##############################################################################
# This code is auto generated. DO NOT EDIT FILE!
# Run "./gradlew :Generators:generatePythonImportTools" to generate
##############################################################################


import jpy
import wrapt


_java_type_ = None  # None until the first _defineSymbols() call
_builder_type_ = None  # None until the first _defineSymbols() call


def _defineSymbols():
    """
    Defines appropriate java symbol, which requires that the jvm has been initialized through the :class:`jpy` module,
    for use throughout the module AT RUNTIME. This is versus static definition upon first import, which would lead to an
    exception if the jvm wasn't initialized BEFORE importing the module.
    """

    if not jpy.has_jvm():
        raise SystemError("No java functionality can be used until the JVM has been initialized through the jpy module")

    global _java_type_, _builder_type_
    if _java_type_ is None:
        # This will raise an exception if the desired object is not the classpath
        _java_type_ = jpy.get_type("com.illumon.iris.importers.util.CsvImport")
        _builder_type_ = jpy.get_type("com.illumon.iris.importers.util.CsvImport$Builder")


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
def builder(namespace, table):
    """
    Deprecated. use fromFiles(String, String) instead.
    
    :param namespace: (java.lang.String) - The String name of the namespace into which data will be imported.
    :param table: (java.lang.String) - The String name of the table into which data will be imported.
    :return: (com.illumon.iris.importers.util.CsvImportBuilder) A new CsvImportBuilder.
    """
    return CsvImportBuilder(namespace, table)


@_passThrough
def fromFiles(namespace, table):
    """
    Creates a new CsvImportBuilder to configure an CSV importer that pulls data from a set of files on disk.
    
    :param namespace: (java.lang.String) - The String name of the namespace into which data will be imported.
    :param table: (java.lang.String) - The String name of the table into which data will be imported.
    :return: (com.illumon.iris.importers.util.CsvImportBuilder) A new CsvImportBuilder.
    """
    return _java_type_.fromFiles(namespace, table)


@_passThrough
def fromStream(namespace, table, stream):
    """
    Creates a new CsvImportBuilder to configure an CSV importer that pulls data from a specific InputStream.
    
    :param namespace: (java.lang.String) - The String name of the namespace into which data will be imported.
    :param table: (java.lang.String) - The String name of the table into which data will be imported.
    :param stream: java.io.InputStream
    :return: (com.illumon.iris.importers.util.CsvImportBuilder) A new CsvImportBuilder.
    """
    return _java_type_.fromStream(namespace, table, stream)


class CsvImportBuilder(object):
    def __init__(self, *args, **kwargs):
        """
        Either *args or **kwargs should be provided for successful construction.
        - *args, when provided, should take the form (namespace, table)
        - **kwargs, when provided, should take the form {'builder': *value*}, and is generally 
          meant for internal use
        """
        _defineSymbols()
        builder = kwargs.get('builder', None)
        if builder is not None:
            self._builder = builder
        else:
            self._builder = _java_type_.builder(*args)

    @property
    def builder(self):
        """The java builder object."""
        return self._builder

    def build(self):
        """
        Builds the importer.
        
        :return: (ImportBuilder.IMPORT_TYPE) importer.
        """
        return self._builder.build()

    def setColumnNames(self, columnNames):
        return CsvImportBuilder(builder=self._builder.setColumnNames(columnNames))

    def setConstantColumnValue(self, constantColumnValue):
        return CsvImportBuilder(builder=self._builder.setConstantColumnValue(constantColumnValue))

    def setDelimiter(self, delimiter):
        return CsvImportBuilder(builder=self._builder.setDelimiter(delimiter))

    def setDestinationDirectory(self, destinationDirectory):
        """
        Sets the destination directory.
        
        :param destinationDirectory: (java.io.File) - destination directory.
        :return: (ImportBuilder.BUILDER_TYPE) this builder.
        """
        return CsvImportBuilder(builder=self._builder.setDestinationDirectory(destinationDirectory))

    def setDestinationPartitions(self, destinationPartitions):
        """
        Sets the destination partitions
        
        *Overload 1*  
          :param destinationPartitions: (java.lang.String) - destination partitions.
          :return: (ImportBuilder.BUILDER_TYPE) this builder.
          
        *Overload 2*  
          :param destinationPartitions: (java.lang.String[]) - destination partitions.
          :return: (ImportBuilder.BUILDER_TYPE) this builder.
        """
        return CsvImportBuilder(builder=self._builder.setDestinationPartitions(destinationPartitions))

    def setFileFormat(self, fileFormat):
        return CsvImportBuilder(builder=self._builder.setFileFormat(fileFormat))

    def setNoHeader(self, noHeader):
        return CsvImportBuilder(builder=self._builder.setNoHeader(noHeader))

    def setOutputMode(self, outputMode):
        """
        Sets the output mode.
        
        *Overload 1*  
          :param outputMode: (com.illumon.iris.importers.ImportOutputMode) - output mode.
          :return: (ImportBuilder.BUILDER_TYPE) this builder.
          
        *Overload 2*  
          :param outputMode: (java.lang.String) - output mode.
          :return: (ImportBuilder.BUILDER_TYPE) this builder.
        """
        return CsvImportBuilder(builder=self._builder.setOutputMode(outputMode))

    def setPartitionColumn(self, partitionColumn):
        """
        Sets the partition column.
        
        :param partitionColumn: (java.lang.String) - partition column.
        :return: (ImportBuilder.BUILDER_TYPE) this builder.
        """
        return CsvImportBuilder(builder=self._builder.setPartitionColumn(partitionColumn))

    def setSchemaService(self, schemaService):
        """
        Sets the schema service.
        
        :param schemaService: (com.illumon.iris.db.schema.SchemaService) - schema service.
        :return: (ImportBuilder.BUILDER_TYPE) this builder.
        """
        return CsvImportBuilder(builder=self._builder.setSchemaService(schemaService))

    def setSkipFooterLines(self, skipFooterLines):
        return CsvImportBuilder(builder=self._builder.setSkipFooterLines(skipFooterLines))

    def setSkipLines(self, skipLines):
        return CsvImportBuilder(builder=self._builder.setSkipLines(skipLines))

    def setSourceDirectory(self, sourceDirectory):
        """
        Sets the source directory.
        
        *Overload 1*  
          :param sourceDirectory: (java.io.File) - source directory
          :return: (FileImportBuilder.BUILDER_TYPE) this builder
          
        *Overload 2*  
          :param sourceDirectory: (java.lang.String) - source directory
          :return: (FileImportBuilder.BUILDER_TYPE) this builder
        """
        return CsvImportBuilder(builder=self._builder.setSourceDirectory(sourceDirectory))

    def setSourceFile(self, sourceFile):
        """
        Sets the source file.
        
        :param sourceFile: (java.lang.String) - source file
        :return: (FileImportBuilder.BUILDER_TYPE) this builder
        """
        return CsvImportBuilder(builder=self._builder.setSourceFile(sourceFile))

    def setSourceGlob(self, sourceGlob):
        """
        Sets the source glob.
        
        :param sourceGlob: (java.lang.String) - source glob
        :return: (FileImportBuilder.BUILDER_TYPE) this builder
        """
        return CsvImportBuilder(builder=self._builder.setSourceGlob(sourceGlob))

    def setSourceName(self, sourceName):
        """
        Sets the source name.
        
        :param sourceName: (java.lang.String) - source name.
        :return: (ImportBuilder.BUILDER_TYPE) this builder.
        """
        return CsvImportBuilder(builder=self._builder.setSourceName(sourceName))

    def setStrict(self, strict):
        """
        Sets strict checking.
        
        :param strict: (boolean) - strict.
        :return: (ImportBuilder.BUILDER_TYPE) this builder.
        """
        return CsvImportBuilder(builder=self._builder.setStrict(strict))

    def setTrim(self, trim):
        return CsvImportBuilder(builder=self._builder.setTrim(trim))
