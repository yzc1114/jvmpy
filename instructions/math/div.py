from ..instruction import NoOperandsInstruction
from runtime.frame import Frame


class IDIV(NoOperandsInstruction):
    def execute(self, frame: Frame):
        stack = frame.operand_stack()
        v2 = stack.pop_int()
        v1 = stack.pop_int()
        if v1 == 0:
            raise Exception("java.lang.ArithmeticException: / by zero")
        stack.push_int(v1 / v2)


class LDIV(NoOperandsInstruction):
    def execute(self, frame: Frame):
        stack = frame.operand_stack()
        v2 = stack.pop_long()
        v1 = stack.pop_long()
        if v2 == 0:
            raise Exception("java.lang.ArithmeticException: / by zero")
        stack.push_long(v1 / v2)


class DDIV(NoOperandsInstruction):
    def execute(self, frame: Frame):
        stack = frame.operand_stack()
        v2 = stack.pop_double()
        v1 = stack.pop_double()
        stack.push_double(v1 / v2)


class FDIV(NoOperandsInstruction):
    def execute(self, frame: Frame):
        stack = frame.operand_stack()
        v2 = stack.pop_float()
        v1 = stack.pop_float()
        stack.push_float(v1 / v2)
