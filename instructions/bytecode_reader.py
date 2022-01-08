from utils.bits_converter import *
import numpy as np


class ByteCodeReader(object):
    def __init__(self):
        self.code: bytes = None
        self.pc_val: int = None

    def reset(self, code:bytes, pc: int):
        self.code = code
        self.pc_val = pc

    def pc(self) -> int:
        return self.pc_val

    def read_uint8(self) -> np.uint8:
        val = self.code[self.pc_val]
        self.pc_val += 1
        return np.uint8(val)

    def read_int8(self) -> np.int8:
        return np.int8(self.read_uint8())

    def read_uint16(self) -> np.uint16:
        return bytes_to_uint16(bytes([self.read_uint8(), self.read_uint8()]))

    def read_int16(self) -> np.int16:
        return np.int16(self.read_uint16())

    def read_int32(self) -> np.int32:
        return bytes_to_int32(bytes([self.read_uint8() for _ in range(4)]))

    def read_int32s(self, n) -> [np.int32]:
        return [self.read_int32() for _ in range(n)]

    def skip_padding(self):
        while self.pc_val % 4 != 0:
            self.read_uint8()
