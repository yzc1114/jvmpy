from ..instruction import NoOperandsInstruction
from runtime.frame import Frame


class INEG(NoOperandsInstruction):
    def execute(self, frame: Frame):
        stack = frame.operand_stack()
        v1 = stack.pop_int()
        stack.push_int(-v1)


class LNEG(NoOperandsInstruction):
    def execute(self, frame: Frame):
        stack = frame.operand_stack()
        v1 = stack.pop_long()
        stack.push_long(-v1)


class DNEG(NoOperandsInstruction):
    def execute(self, frame: Frame):
        stack = frame.operand_stack()
        v1 = stack.pop_double()
        stack.push_double(-v1)


class FNEG(NoOperandsInstruction):
    def execute(self, frame: Frame):
        stack = frame.operand_stack()
        v1 = stack.pop_float()
        stack.push_float(-v1)
