import numpy as np
from ..class_reader import ClassReader
from ..attribute_info import AttributeInfo


class LocalVariableTableAttribute(AttributeInfo):

    class LocalVariableTableEntry(object):
        def __init__(self):
            self.startPc: np.uint16 = None
            self.length: np.uint16 = None
            self.nameIndex: np.uint16 = None
            self.descriptorIndex: np.uint16 = None
            self.index: np.uint16 = None

    def __init__(self):
        self.localVariableTable: [LocalVariableTableAttribute.LocalVariableTableEntry] = None

    def read_info(self, reader: ClassReader):
        local_variable_table_length = reader.read_uint16()
        self.localVariableTable = []
        for i in range(local_variable_table_length):
            entry = LocalVariableTableAttribute.LocalVariableTableEntry()
            entry.startPc = reader.read_uint16()
            entry.length = reader.read_uint16()
            entry.nameIndex = reader.read_uint16()
            entry.descriptorIndex = reader.read_uint16()
            entry.index = reader.read_uint16()


