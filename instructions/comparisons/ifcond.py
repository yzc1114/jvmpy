'''
整数与0的比较跳转指令
'''
from runtime.frame import Frame
from ..instruction import BranchInstruction
from ..base.branch_logic import branch


class IFEQ(BranchInstruction):
    def execute(self, frame: Frame):
        if frame.operand_stack().pop_int() == 0:
            branch(frame, offset=self.offset)


class IFNE(BranchInstruction):
    def execute(self, frame: Frame):
        if frame.operand_stack().pop_int() != 0:
            branch(frame, offset=self.offset)


class IFLT(BranchInstruction):
    def execute(self, frame: Frame):
        if frame.operand_stack().pop_int() < 0:
            branch(frame, offset=self.offset)


class IFLE(BranchInstruction):
    def execute(self, frame: Frame):
        if frame.operand_stack().pop_int() <= 0:
            branch(frame, offset=self.offset)


class IFGT(BranchInstruction):
    def execute(self, frame: Frame):
        val = frame.operand_stack().pop_int()
        if val > 0:
            branch(frame, offset=self.offset)


class IFGE(BranchInstruction):
    def execute(self, frame: Frame):
        if frame.operand_stack().pop_int() >= 0:
            branch(frame, offset=self.offset)
