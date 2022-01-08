from ..instruction import NoOperandsInstruction
from runtime.frame import Frame
import numpy as np


class ISHL(NoOperandsInstruction):
    def execute(self, frame: Frame):
        stack = frame.operand_stack()
        v2 = stack.pop_int()
        v1 = stack.pop_int()
        s = np.uint32(v2) & 0x1f
        stack.push_int(v1 << s)


class ISHR(NoOperandsInstruction):
    def execute(self, frame: Frame):
        stack = frame.operand_stack()
        v2 = stack.pop_int()
        v1 = stack.pop_int()
        s = np.uint32(v2) & 0x1f
        stack.push_int(v1 >> s)


class IUSHR(NoOperandsInstruction):
    def execute(self, frame: Frame):
        stack = frame.operand_stack()
        v2 = stack.pop_int()
        v1 = stack.pop_int()
        s = np.uint32(v2) & 0x1f
        stack.push_int(np.int32(np.uint32(v1) >> s))


class LSHL(NoOperandsInstruction):
    def execute(self, frame: Frame):
        stack = frame.operand_stack()
        v2 = stack.pop_int()
        v1 = stack.pop_long()
        s = np.uint32(v2) & 0x3f
        stack.push_long(v1 << s)


class LSHR(NoOperandsInstruction):
    def execute(self, frame: Frame):
        stack = frame.operand_stack()
        v2 = stack.pop_int()
        v1 = stack.pop_long()
        s = np.uint32(v2) & 0x3f
        stack.push_long(v1 >> s)


class LUSHR(NoOperandsInstruction):
    def execute(self, frame: Frame):
        stack = frame.operand_stack()
        v2 = stack.pop_int()
        v1 = stack.pop_long()
        s = np.uint32(v2) & 0x3f
        stack.push_long(np.int64(np.uint64(v1) >> s))
