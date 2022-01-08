from runtime.heap.object import Object
import numpy as np
from utils.bits_converter import *


class StringPool(object):
    internedStrings : {str: Object} = {}

    @classmethod
    def java_string(cls, loader, pystr: str) -> Object:
        if pystr in cls.internedStrings.keys():
            return cls.internedStrings[pystr]

        chars = cls.__string_to_utf16(pystr)
        # 得到String对象内部的字节数组对象
        j_chars = Object(cls=loader.load_class('[C'), data=chars)
        # 得到java的String对象
        j_str = loader.load_class("java/lang/String").new_object()
        # 将String对象内部的字节数组对象赋值
        j_str.set_ref_var("value", "[C", j_chars)

        cls.internedStrings[pystr] = j_str
        return j_str

    @staticmethod
    def chars_to_string(l: [np.uint16]) -> str:
        sl = [None for _ in range(len(l))]
        for i, c in enumerate(l):
            sl[i] = chr(c)
        return "".join(sl)

    @staticmethod
    def __string_to_utf16(s: str) -> [np.uint16]:
        res = [0 for _ in range(len(s))]
        for i, c in enumerate(s):
            res[i] = np.uint16(ord(c))
        return res

    @classmethod
    def py_str(cls, j_str: Object) -> str:
        chars_obj = j_str.get_ref_var("value", "[C")
        chars = chars_obj.chars()
        return cls.chars_to_string(chars)

    @classmethod
    def intern_string(cls, j_str: Object) -> Object:
        pystr = cls.py_str(j_str)
        if pystr in cls.internedStrings.keys():
            return cls.internedStrings[pystr]
        cls.internedStrings[pystr] = j_str
        return j_str