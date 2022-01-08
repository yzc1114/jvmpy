from runtime.frame import Frame
from ..instruction import NoOperandsInstruction


class POP(NoOperandsInstruction):
    def execute(self, frame: Frame):
        frame.operand_stack().pop_slot()


class POP2(NoOperandsInstruction):
    def execute(self, frame: Frame):
        frame.operand_stack().pop_slot()
        frame.operand_stack().pop_slot()
