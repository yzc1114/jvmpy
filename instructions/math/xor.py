from ..instruction import NoOperandsInstruction
from runtime.frame import Frame


class IOR(NoOperandsInstruction):
    def execute(self, frame: Frame):
        stack = frame.operand_stack()
        v2 = stack.pop_int()
        v1 = stack.pop_int()
        stack.push_int(v1 ^ v2)


class LOR(NoOperandsInstruction):
    def execute(self, frame: Frame):
        stack = frame.operand_stack()
        v2 = stack.pop_long()
        v1 = stack.pop_long()
        stack.push_long(v1 ^ v2)
