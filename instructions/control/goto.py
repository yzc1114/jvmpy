from ..instruction import BranchInstruction
from runtime.frame import Frame
from ..base.branch_logic import branch


class GOTO(BranchInstruction):
    def execute(self, frame: Frame):
        branch(frame, self.offset)
