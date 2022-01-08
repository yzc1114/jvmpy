from classfile.class_reader import ClassReader
from ..constant_info import ConstantInfo
import numpy as np


class ConstantUtf8Info(ConstantInfo):
    def __init__(self):
        self.string_val: str = None

    def read_info(self, reader: ClassReader):
        length = np.uint32(reader.read_uint16())
        bs = reader.read_bytes(length)
        self.string_val = bs.decode('utf-8')

    def string(self) -> str:
        return self.string_val
