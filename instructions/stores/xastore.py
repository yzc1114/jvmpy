from ..instruction import NoOperandsInstruction
from ..bytecode_reader import ByteCodeReader
from runtime.frame import Frame
import numpy as np


def _check_not_none(ref):
    if ref is None:
        raise Exception("java.lang.NullPointerException")

def _check_index(length, index):
    if index < 0 or index >= length:
        raise Exception("ArrayIndexOutOfBoundsException")


class IASTORE(NoOperandsInstruction):
    def execute(self, frame: Frame):
        stack = frame.operand_stack()
        val = stack.pop_int()
        index = stack.pop_int()
        arr_ref = stack.pop_ref()

        _check_not_none(arr_ref)
        ints = arr_ref.ints()
        _check_index(len(ints), index)
        ints[index] = np.int32(val)


class BASTORE(NoOperandsInstruction):
    def execute(self, frame: Frame):
        stack = frame.operand_stack()
        val = stack.pop_int()
        index = stack.pop_int()
        arr_ref = stack.pop_ref()

        _check_not_none(arr_ref)
        vals = arr_ref.bytes()
        _check_index(len(vals), index)
        vals[index] = np.int8(val)


class CASTORE(NoOperandsInstruction):
    def execute(self, frame: Frame):
        stack = frame.operand_stack()
        val = stack.pop_int()
        index = stack.pop_int()
        arr_ref = stack.pop_ref()

        _check_not_none(arr_ref)
        vals = arr_ref.chars()
        _check_index(len(vals), index)
        vals[index] = np.uint16(val)


class DASTORE(NoOperandsInstruction):
    def execute(self, frame: Frame):
        stack = frame.operand_stack()
        val = stack.pop_double()
        index = stack.pop_int()
        arr_ref = stack.pop_ref()

        _check_not_none(arr_ref)
        doubles = arr_ref.doubles()
        _check_index(len(doubles), index)
        doubles[index] = np.float64(val)


class FASTORE(NoOperandsInstruction):
    def execute(self, frame: Frame):
        stack = frame.operand_stack()
        val = stack.pop_float()
        index = stack.pop_int()
        arr_ref = stack.pop_ref()

        _check_not_none(arr_ref)
        floats = arr_ref.floats()
        _check_index(len(floats), index)
        floats[index] = np.float32(val)


class LASTORE(NoOperandsInstruction):
    def execute(self, frame: Frame):
        stack = frame.operand_stack()
        val = stack.pop_long()
        index = stack.pop_int()
        arr_ref = stack.pop_ref()

        _check_not_none(arr_ref)
        longs = arr_ref.longs()
        _check_index(len(longs), index)
        longs[index] = np.int32(val)


class SASTORE(NoOperandsInstruction):
    def execute(self, frame: Frame):
        stack = frame.operand_stack()
        val = stack.pop_int()
        index = stack.pop_int()
        arr_ref = stack.pop_ref()

        _check_not_none(arr_ref)
        shorts = arr_ref.shorts()
        _check_index(len(shorts), index)
        shorts[index] = np.int32(val)


class AASTORE(NoOperandsInstruction):
    def execute(self, frame: Frame):
        stack = frame.operand_stack()
        val = stack.pop_ref()
        index = stack.pop_int()
        arr_ref = stack.pop_ref()

        _check_not_none(arr_ref)
        refs = arr_ref.refs()
        _check_index(len(refs), index)
        refs[index] = val