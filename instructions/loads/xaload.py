from ..instruction import NoOperandsInstruction
from runtime.frame import Frame


def _check_not_none(ref):
    if ref is None:
        raise Exception("java.lang.NullPointerException")

def _check_index(length, index):
    if index < 0 or index >= length:
        raise Exception("ArrayIndexOutOfBoundsException")


class AALOAD(NoOperandsInstruction):
    def execute(self, frame: Frame):
        stack = frame.operand_stack()
        index = stack.pop_int()
        arr_ref = stack.pop_ref()

        _check_not_none(arr_ref)
        refs = arr_ref.refs()
        _check_index(len(refs), index)
        stack.push_ref(refs[index])


class BALOAD(NoOperandsInstruction):
    def execute(self, frame: Frame):
        stack = frame.operand_stack()
        index = stack.pop_int()
        arr_ref = stack.pop_ref()

        _check_not_none(arr_ref)
        vals = arr_ref.bytes()
        _check_index(len(vals), index)
        stack.push_int(vals[index])


class CALOAD(NoOperandsInstruction):
    def execute(self, frame: Frame):
        stack = frame.operand_stack()
        index = stack.pop_int()
        arr_ref = stack.pop_ref()

        _check_not_none(arr_ref)
        vals = arr_ref.chars()
        _check_index(len(vals), index)
        stack.push_int(vals[index])


class DALOAD(NoOperandsInstruction):
    def execute(self, frame: Frame):
        stack = frame.operand_stack()
        index = stack.pop_int()
        arr_ref = stack.pop_ref()

        _check_not_none(arr_ref)
        vals = arr_ref.doubles()
        _check_index(len(vals), index)
        stack.push_double(vals[index])


class FALOAD(NoOperandsInstruction):
    def execute(self, frame: Frame):
        stack = frame.operand_stack()
        index = stack.pop_int()
        arr_ref = stack.pop_ref()

        _check_not_none(arr_ref)
        vals = arr_ref.floats()
        _check_index(len(vals), index)
        stack.push_float(vals[index])


class IALOAD(NoOperandsInstruction):
    def execute(self, frame: Frame):
        stack = frame.operand_stack()
        index = stack.pop_int()
        arr_ref = stack.pop_ref()

        _check_not_none(arr_ref)
        vals = arr_ref.ints()
        _check_index(len(vals), index)
        stack.push_int(vals[index])


class LALOAD(NoOperandsInstruction):
    def execute(self, frame: Frame):
        stack = frame.operand_stack()
        index = stack.pop_int()
        arr_ref = stack.pop_ref()

        _check_not_none(arr_ref)
        vals = arr_ref.longs()
        _check_index(len(vals), index)
        stack.push_long(vals[index])


class SALOAD(NoOperandsInstruction):
    def execute(self, frame: Frame):
        stack = frame.operand_stack()
        index = stack.pop_int()
        arr_ref = stack.pop_ref()

        _check_not_none(arr_ref)
        vals = arr_ref.shorts()
        _check_index(len(vals), index)
        stack.push_int(vals[index])