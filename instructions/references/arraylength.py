from ..instruction import NoOperandsInstruction
from runtime.frame import Frame


class ARRAY_LENGTH(NoOperandsInstruction):
    def execute(self, frame: Frame):
        stack = frame.operand_stack()
        arr_ref = stack.pop_ref()
        if arr_ref is None:
            raise Exception("java.lang.NullPointerException")
        arr_len = arr_ref.array_length()
        stack.push_int(arr_len)