'''
整数比较跳转指令
'''
from runtime.frame import Frame
from ..instruction import BranchInstruction
from ..base.branch_logic import branch


class IF_ICMPEQ(BranchInstruction):
    def execute(self, frame: Frame):
        v1, v2 = _icmp_pop(frame)
        if v1 == v2:
            branch(frame, self.offset)


class IF_ICMPNE(BranchInstruction):
    def execute(self, frame: Frame):
        v1, v2 = _icmp_pop(frame)
        if v1 != v2:
            branch(frame, self.offset)


class IF_ICMPLT(BranchInstruction):
    def execute(self, frame: Frame):
        v1, v2 = _icmp_pop(frame)
        if v1 < v2:
            branch(frame, self.offset)


class IF_ICMPLE(BranchInstruction):
    def execute(self, frame: Frame):
        v1, v2 = _icmp_pop(frame)
        if v1 <= v2:
            branch(frame, self.offset)


class IF_ICMPGT(BranchInstruction):
    def execute(self, frame: Frame):
        v1, v2 = _icmp_pop(frame)
        if v1 > v2:
            branch(frame, self.offset)


class IF_ICMPGE(BranchInstruction):
    def execute(self, frame: Frame):
        v1, v2 = _icmp_pop(frame)
        if v1 >= v2:
            branch(frame, self.offset)


def _icmp_pop(frame: Frame):
    stack = frame.operand_stack()
    v2 = stack.pop_int()
    v1 = stack.pop_int()
    return v1, v2
