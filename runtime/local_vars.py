import numpy as np


class LocalVars(object):
    def __init__(self, max_locals: int):
        self.vars: [Slot] = [Slot(0, None) for _ in range(max_locals)]

    def set_int(self, index: int, val: int):
        self.vars[index] = Slot(np.uint32(val), None)

    def get_int(self, index: int) -> np.int32:
        return np.int32(self.vars[index].num)

    def get_boolean(self, index: int) -> bool:
        return self.get_int(index) == 1

    def set_long(self, index: int, val: int):
        self.vars[index] = Slot(np.uint32(val), None)
        self.vars[index + 1] = Slot(np.uint32(val >> 32), None)

    def get_long(self, index: int) -> np.int64:
        index = int(index)
        low = self.vars[index].num
        high = self.vars[index + 1].num
        return np.int64(high << 32) | np.int64(low)

    def set_float(self, index: int, val: float):
        self.vars[index] = Slot(bytes_to_uint32(float32_to_bytes(np.float32(val))), None)

    def get_float(self, index: int) -> np.float32:
        return bytes_to_float32(uint32_to_bytes(self.vars[index].num))

    def set_double(self, index: int, val: float):
        self.set_long(index, bytes_to_int64(float64_to_bytes(np.float32(val))))

    def get_double(self, index: int) -> np.float64:
        return bytes_to_float64(int64_to_bytes(self.get_long(index)))

    def set_ref(self, index: int, ref):
        self.vars[index] = Slot(0, ref)

    def get_ref(self, index: int):
        return self.vars[index].ref

    def set_slot(self, index: int, slot):
        self.vars[index] = slot

    def get_slot(self, index):
        return self.vars[index]

    def get_this(self):
        return self.get_ref(0)

    def __getitem__(self, index):
        return self.get_slot(index)

from .slot import Slot
from utils.bits_converter import *