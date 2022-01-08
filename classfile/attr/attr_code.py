import numpy as np
from ..class_reader import ClassReader
from ..attribute_info import AttributeInfo, read_attributes
from ..constant_pool import ConstantPool
from .attr_line_number_table import LineNumberTableAttribute


class CodeAttribute(AttributeInfo):

    class ExceptionEntry(object):
        def __init__(self):
            self.startPc: np.uint16 = None
            self.endPc: np.uint16 = None
            self.handlerPc: np.uint16 = None
            self.catchType: np.uint16 = None

        def start_pc(self):
            return self.startPc

        def end_pc(self):
            return self.endPc

        def handler_pc(self):
            return self.handlerPc

        def catch_type(self):
            return self.catchType

    def __init__(self, cp: ConstantPool):
        self.cp: ConstantPool = cp
        self.maxStack: np.uint16 = None
        self.maxLocals: np.uint16 = None
        self.codes: bytes = None
        self.exceptionTable: [CodeAttribute.ExceptionEntry] = None
        self.attributes: [AttributeInfo] = None

    def max_stack(self) -> np.uint16:
        return self.maxStack

    def max_locals(self) -> np.uint16:
        return self.maxLocals

    def code(self) -> bytes:
        return self.codes

    def exception_table(self) -> []:
        return self.exceptionTable

    def line_number_table_attribute(self) -> LineNumberTableAttribute:
        for attr in self.attributes:
            if isinstance(attr, LineNumberTableAttribute):
                return attr

    def read_info(self, reader: ClassReader):
        self.maxStack = reader.read_uint16()
        self.maxLocals = reader.read_uint16()
        code_length = reader.read_uint32()
        self.codes = reader.read_bytes(code_length)
        self.exceptionTable = self.__read_exception_table(reader)
        self.attributes = read_attributes(reader, self.cp)

    @staticmethod
    def __read_exception_table(reader: ClassReader) -> []:
        exception_table_length = reader.read_uint16()
        table = []
        for i in range(exception_table_length):
            entry = CodeAttribute.ExceptionEntry()
            entry.startPc = reader.read_uint16()
            entry.endPc = reader.read_uint16()
            entry.handlerPc = reader.read_uint16()
            entry.catchType = reader.read_uint16()
            table.append(entry)
        return table

