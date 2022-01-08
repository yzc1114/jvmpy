from ..instruction import NoOperandsInstruction
from runtime.frame import Frame


class D2F(NoOperandsInstruction):
    def execute(self, frame: Frame):
        stack = frame.operand_stack()
        d = stack.pop_double()
        stack.push_float(float(d))


class D2I(NoOperandsInstruction):
    def execute(self, frame: Frame):
        stack = frame.operand_stack()
        d = stack.pop_double()
        stack.push_int(int(d))


class D2L(NoOperandsInstruction):
    def execute(self, frame: Frame):
        stack = frame.operand_stack()
        d = stack.pop_double()
        stack.push_long(int(d))
