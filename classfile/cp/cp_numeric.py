from classfile.class_reader import ClassReader
from ..constant_info import ConstantInfo
from utils.bits_converter import *
import numpy as np


class ConstantIntegerInfo(ConstantInfo):

    def __init__(self):
        self.val: np.int32 = None

    def read_info(self, reader: ClassReader):
        bs = reader.read_bytes(4)
        self.val = bytes_to_int32(bs)

    def value(self) -> np.uint32:
        return self.val


class ConstantFloatInfo(ConstantInfo):

    def __init__(self):
        self.val: np.float32 = None

    def read_info(self, reader: ClassReader):
        bs = reader.read_bytes(4)
        self.val = bytes_to_float32(bs)

    def value(self) -> np.float32:
        return self.val


class ConstantLongInfo(ConstantInfo):

    def __init__(self):
        self.val: np.int64 = None

    def read_info(self, reader: ClassReader):
        bs = reader.read_bytes(8)
        self.val = bytes_to_int64(bs)

    def value(self) -> np.int64:
        return self.val


class ConstantDoubleInfo(ConstantInfo):

    def __init__(self):
        self.val: np.float64 = None

    def read_info(self, reader: ClassReader):
        bs = reader.read_bytes(8)
        self.val = bytes_to_float64(bs)

    def value(self) -> np.float64:
        return self.val
