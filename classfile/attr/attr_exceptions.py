import numpy as np
from ..class_reader import ClassReader
from ..attribute_info import AttributeInfo


class ExceptionsAttribute(AttributeInfo):
    def __init__(self):
        self.exceptionIndexTable: [np.uint16] = None

    def read_info(self, reader: ClassReader):
        self.exceptionIndexTable = reader.read_uint16s()

    def exception_index_table(self) -> [np.uint16]:
        return self.exceptionIndexTable
