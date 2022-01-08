from ..instruction import NoOperandsInstruction
from runtime.frame import Frame
import numpy as np


class I2B(NoOperandsInstruction):
    def execute(self, frame: Frame):
        stack = frame.operand_stack()
        d = stack.pop_int()
        stack.push_int(int(np.int8(d)))


class I2C(NoOperandsInstruction):
    def execute(self, frame: Frame):
        stack = frame.operand_stack()
        d = stack.pop_int()
        stack.push_int(int(np.uint16(d)))


class I2S(NoOperandsInstruction):
    def execute(self, frame: Frame):
        stack = frame.operand_stack()
        d = stack.pop_int()
        stack.push_int(int(np.int16(d)))


class I2L(NoOperandsInstruction):
    def execute(self, frame: Frame):
        stack = frame.operand_stack()
        d = stack.pop_int()
        stack.push_long(int(d))


class I2D(NoOperandsInstruction):
    def execute(self, frame: Frame):
        stack = frame.operand_stack()
        d = stack.pop_int()
        stack.push_double(float(d))


class I2F(NoOperandsInstruction):
    def execute(self, frame: Frame):
        stack = frame.operand_stack()
        d = stack.pop_int()
        stack.push_float(float(d))
