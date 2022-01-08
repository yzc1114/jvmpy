from .slot import Slot
from runtime.heap.object import Object
from utils.bits_converter import *
import numpy as np


class OperandStack(object):
    def __init__(self, max_size: int):
        self.size: np.uint32 = np.uint32(0)
        self.slots = [Slot(0, None) for _ in range(max_size)]
        self.max_size = max_size

    def push_int(self, val: int):
        self.slots[int(self.size)] = Slot(np.uint32(val), None)
        self.size += 1

    def pop_int(self) -> np.int32:
        self.size -= 1
        val = np.int32(self.slots[self.size].num)
        self.slots[self.size] = Slot(0, None)
        return val

    def push_float(self, val: float):
        self.slots[int(self.size)] = Slot(bytes_to_uint32(float32_to_bytes(np.float32(val))), None)
        self.size += 1

    def pop_float(self) -> np.float32:
        self.size -= 1
        val = bytes_to_float32(uint32_to_bytes(self.slots[int(self.size)].num))
        self.slots[int(self.size)] = Slot(0, None)
        return val

    def push_long(self, val: int):
        self.slots[int(self.size)] = Slot(np.uint32(val), None)
        self.slots[int(self.size + 1)] = Slot(np.uint32(val >> 32), None)
        self.size += 2

    def pop_long(self) -> np.int64:
        self.size -= 2
        low = self.slots[int(self.size)].num
        high = self.slots[int(self.size + 1)].num
        self.slots[int(self.size)] = Slot(0, None)
        self.slots[int(self.size + 1)] = Slot(0, None)
        return np.int64(high) << 32 | np.int64(low)

    def push_double(self, val: float):
        bs = float64_to_bytes(np.float64(val))
        self.push_long(bytes_to_int64(bs))

    def pop_double(self) -> np.float64:
        return bytes_to_float64(int64_to_bytes(self.pop_long()))

    def push_ref(self, obj):
        self.slots[self.size] = Slot(0, obj)
        self.size += 1

    def pop_ref(self) -> Object:
        self.size -= 1
        ref = self.slots[self.size].ref
        self.slots[self.size] = Slot(0, None)
        return ref

    def push_boolean(self, val: bool):
        if val:
            self.push_int(1)
        else:
            self.push_int(0)

    def pop_boolean(self) -> bool:
        return self.pop_int() == 1

    def push_slot(self, slot: Slot):
        self.slots[self.size] = slot
        self.size += 1

    def pop_slot(self) -> Slot:
        self.size -= 1
        s = self.slots[self.size]
        new_s = Slot(s.num, s.ref)
        self.slots[self.size] = Slot(0, None)
        return new_s

    def get_ref_from_top(self, index: int) -> Object:
        return self.slots[self.size - index - 1].ref

    def clear(self):
        while self.size > 0:
            self.pop_slot()