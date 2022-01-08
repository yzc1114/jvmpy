from runtime.frame import Frame
from ..instruction import NoOperandsInstruction


class SWAP(NoOperandsInstruction):
    def execute(self, frame: Frame):
        stack = frame.operand_stack()
        s1 = stack.pop_slot()
        s2 = stack.pop_slot()
        stack.push_slot(s1)
        stack.push_slot(s2)
