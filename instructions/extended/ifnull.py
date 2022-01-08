from runtime.frame import Frame
from ..instruction import BranchInstruction
from ..base.branch_logic import branch


class IFNULL(BranchInstruction):
    def execute(self, frame: Frame):
        stack = frame.operand_stack()
        if stack.pop_ref() is None:
            branch(frame, self.offset)


class IFNONNULL(BranchInstruction):
    def execute(self, frame: Frame):
        stack = frame.operand_stack()
        if stack.pop_ref() is not None:
            branch(frame, self.offset)

