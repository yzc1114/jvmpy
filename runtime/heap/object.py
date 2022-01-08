import numpy as np


class Object(object):
    def __init__(self, cls, data = None):
        self.cls: Class = cls
        # extra在类对象中使用，作为Class类指针使用
        self.extra: object = None
        if data is None:
            self.data: object = Slots(cls.instanceSlotCount)
        else:
            self.data: object = data

    def is_instance_of(self, cls):
        return cls.is_assignable_from(self.cls)

    def bytes(self) -> [np.int8]:
        assert isinstance(self.data, list)
        return self.data

    def shorts(self) -> [np.int16]:
        assert isinstance(self.data, list)
        return self.data

    def ints(self) -> [np.int32]:
        assert isinstance(self.data, list)
        return self.data

    def longs(self) -> [np.int64]:
        assert isinstance(self.data, list)
        return self.data

    def chars(self) -> [np.uint16]:
        assert isinstance(self.data, list)
        return self.data

    def floats(self) -> [np.float32]:
        assert isinstance(self.data, list)
        return self.data

    def doubles(self) -> [np.float64]:
        assert isinstance(self.data, list)
        return self.data

    def refs(self) -> []:
        assert isinstance(self.data, list)
        return self.data

    def array_length(self) -> int:
        assert isinstance(self.data, list)
        return len(self.data)

    def set_ref_var(self, name: str, descriptor: str, var):
        field = self.cls.get_field(name=name, descriptor=descriptor, is_static=False)
        slots = self.data
        assert isinstance(slots, Slots)
        assert isinstance(var, Object)
        slots.set_ref(field.slotId, var)

    def get_ref_var(self, name: str, descriptor: str):
        field = self.cls.get_field(name=name, descriptor=descriptor, is_static=False)
        slots = self.data
        assert isinstance(slots, Slots)
        return slots.get_ref(field.slotId)

    def get_int_var(self, name: str, descriptor: str):
        field = self.cls.get_field(name=name, descriptor=descriptor, is_static=False)
        slots = self.data
        assert isinstance(slots, Slots)
        return slots.get_int(field.slotId)

    def set_int_var(self, name: str, descriptor: str, var: int):
        field = self.cls.get_field(name=name, descriptor=descriptor, is_static=False)
        slots = self.data
        assert isinstance(slots, Slots)
        slots.set_int(field.slotId, var)

    def array_copy(self, dest, src_pos: int, des_pos: int, length: int):
        assert self.cls.is_array()
        assert isinstance(dest, Object)
        assert dest.cls.is_array()
        src = self
        dest.data[des_pos: des_pos + length] = src.data[src_pos: src_pos + length]

    def clone(self):
        return Object(self.cls, self.__clone_data())

    def __clone_data(self):
        assert isinstance(self.data, list) or isinstance(self.data, Slots)
        sample = self.data[0]
        if isinstance(sample, Slot):
            return copy.deepcopy(self.data)
        else:
            return copy.copy(self.data)

    def to_string(self) -> str:
        return StringPool.chars_to_string(self.data)


import copy
from .slots import Slots, Slot
from .class_ import Class
from ..heap.string_pool import StringPool