from ..instruction import NoOperandsInstruction
from runtime.frame import Frame


class F2D(NoOperandsInstruction):
    def execute(self, frame: Frame):
        stack = frame.operand_stack()
        d = stack.pop_float()
        stack.push_float(float(d))


class F2I(NoOperandsInstruction):
    def execute(self, frame: Frame):
        stack = frame.operand_stack()
        d = stack.pop_float()
        stack.push_int(int(d))


class F2L(NoOperandsInstruction):
    def execute(self, frame: Frame):
        stack = frame.operand_stack()
        d = stack.pop_float()
        stack.push_long(int(d))
