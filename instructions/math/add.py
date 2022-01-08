from ..instruction import NoOperandsInstruction
from runtime.frame import Frame


class IADD(NoOperandsInstruction):
    def execute(self, frame: Frame):
        stack = frame.operand_stack()
        v2 = stack.pop_int()
        v1 = stack.pop_int()
        stack.push_int(v1 + v2)


class LADD(NoOperandsInstruction):
    def execute(self, frame: Frame):
        stack = frame.operand_stack()
        v2 = stack.pop_long()
        v1 = stack.pop_long()
        stack.push_long(v1 + v2)


class DADD(NoOperandsInstruction):
    def execute(self, frame: Frame):
        stack = frame.operand_stack()
        v2 = stack.pop_double()
        v1 = stack.pop_double()
        stack.push_double(v1 + v2)


class FADD(NoOperandsInstruction):
    def execute(self, frame: Frame):
        stack = frame.operand_stack()
        v2 = stack.pop_float()
        v1 = stack.pop_float()
        stack.push_float(v1 + v2)
