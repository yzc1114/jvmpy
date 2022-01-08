'''
向栈中push常数的指令
'''
from runtime.frame import Frame
from ..instruction import NoOperandsInstruction


class ACONST_NULL(NoOperandsInstruction):
    def execute(self, frame: Frame):
        frame.operand_stack().push_ref(None)


class DCONST_0(NoOperandsInstruction):
    def execute(self, frame: Frame):
        frame.operand_stack().push_double(0.0)


class DCONST_1(NoOperandsInstruction):
    def execute(self, frame: Frame):
        frame.operand_stack().push_double(1.0)


class FCONST_0(NoOperandsInstruction):
    def execute(self, frame: Frame):
        frame.operand_stack().push_float(0.0)


class FCONST_1(NoOperandsInstruction):
    def execute(self, frame: Frame):
        frame.operand_stack().push_float(1.0)


class FCONST_2(NoOperandsInstruction):
    def execute(self, frame: Frame):
        frame.operand_stack().push_float(2.0)


class ICONST_M1(NoOperandsInstruction):
    def execute(self, frame: Frame):
        frame.operand_stack().push_int(-1)


class ICONST_0(NoOperandsInstruction):
    def execute(self, frame: Frame):
        frame.operand_stack().push_int(0)


class ICONST_1(NoOperandsInstruction):
    def execute(self, frame: Frame):
        frame.operand_stack().push_int(1)


class ICONST_2(NoOperandsInstruction):
    def execute(self, frame: Frame):
        frame.operand_stack().push_int(2)


class ICONST_3(NoOperandsInstruction):
    def execute(self, frame: Frame):
        frame.operand_stack().push_int(3)


class ICONST_4(NoOperandsInstruction):
    def execute(self, frame: Frame):
        frame.operand_stack().push_int(4)


class ICONST_5(NoOperandsInstruction):
    def execute(self, frame: Frame):
        frame.operand_stack().push_int(5)


class LCONST_0(NoOperandsInstruction):
    def execute(self, frame: Frame):
        frame.operand_stack().push_long(0)


class LCONST_1(NoOperandsInstruction):
    def execute(self, frame: Frame):
        frame.operand_stack().push_long(1)