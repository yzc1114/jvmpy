# 对象比较跳转指令
from runtime.frame import Frame
from ..instruction import BranchInstruction
from ..base.branch_logic import branch


class IF_ACMPEQ(BranchInstruction):
    def execute(self, frame: Frame):
        if _acmp(frame):
            branch(frame, self.offset)


class IF_ACMPNE(BranchInstruction):
    def execute(self, frame: Frame):
        if not _acmp(frame):
            branch(frame, self.offset)


def _acmp(frame: Frame) -> bool:
    stack = frame.operand_stack()
    ref2 = stack.pop_ref()
    ref1 = stack.pop_ref()
    return ref1 == ref2
