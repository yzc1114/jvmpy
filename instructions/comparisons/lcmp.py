'''
两个long的比较指令
'''
from runtime.frame import Frame
from ..instruction import NoOperandsInstruction


class LCMP(NoOperandsInstruction):
    def execute(self, frame: Frame):
        stack = frame.operand_stack()
        v2 = stack.pop_long()
        v1 = stack.pop_long()
        if v1 > v2:
            stack.push_int(1)
        elif v1 == v2:
            stack.push_int(0)
        else:
            stack.push_int(-1)
