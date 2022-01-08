from classfile.class_reader import ClassReader
from ..constant_info import ConstantInfo
from ..constant_pool import ConstantPool
import numpy as np


class ConstantStringInfo(ConstantInfo):

    def __init__(self, cp: ConstantPool):
        self.cp: ConstantPool = cp
        self.stringIndex: np.uint16 = None

    def read_info(self, reader: ClassReader):
        self.stringIndex = reader.read_uint16()

    def string(self) -> str:
        return self.cp.get_utf8(self.stringIndex)