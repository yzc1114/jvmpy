import numpy as np
from ..class_reader import ClassReader
from ..attribute_info import AttributeInfo
from ..constant_pool import ConstantPool


class SourceFileAttribute(AttributeInfo):
    def __init__(self, cp: ConstantPool):
        self.cp: ConstantPool = cp
        self.sourceFileIndex: np.uint16 = None

    def read_info(self, reader: ClassReader):
        self.sourceFileIndex = reader.read_uint16()

    def file_name(self) -> str:
        return self.cp.get_utf8(self.sourceFileIndex)
