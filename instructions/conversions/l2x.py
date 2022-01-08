from ..instruction import NoOperandsInstruction
from runtime.frame import Frame
import numpy as np


class L2I(NoOperandsInstruction):
    def execute(self, frame: Frame):
        stack = frame.operand_stack()
        l = stack.pop_long()
        stack.push_int(int(l))


class L2F(NoOperandsInstruction):
    def execute(self, frame: Frame):
        stack = frame.operand_stack()
        l = stack.pop_long()
        stack.push_float(float(l))


class L2D(NoOperandsInstruction):
    def execute(self, frame: Frame):
        stack = frame.operand_stack()
        l = stack.pop_long()
        stack.push_double(float(l))
