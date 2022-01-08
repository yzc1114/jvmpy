from runtime.frame import Frame
from ..instruction import NoOperandsInstruction


class DUP(NoOperandsInstruction):
    def execute(self, frame: Frame):
        stack = frame.operand_stack()
        s = stack.pop_slot()
        stack.push_slot(s)
        stack.push_slot(Slot(s.num, s.ref))


class DUP_X1(NoOperandsInstruction):
    def execute(self, frame: Frame):
        stack = frame.operand_stack()
        s1 = stack.pop_slot()
        s2 = stack.pop_slot()
        stack.push_slot(s1)
        stack.push_slot(s2)
        stack.push_slot(Slot(s1.num, s1.ref))


class DUP_X2(NoOperandsInstruction):
    def execute(self, frame: Frame):
        stack = frame.operand_stack()
        s1 = stack.pop_slot()
        s2 = stack.pop_slot()
        s3 = stack.pop_slot()
        stack.push_slot(s1)
        stack.push_slot(s3)
        stack.push_slot(s2)
        stack.push_slot(Slot(s1.num, s1.ref))


class DUP2(NoOperandsInstruction):
    def execute(self, frame: Frame):
        stack = frame.operand_stack()
        s1 = stack.pop_slot()
        s2 = stack.pop_slot()
        stack.push_slot(s2)
        stack.push_slot(s1)
        stack.push_slot(Slot(s2.num, s2.ref))
        stack.push_slot(Slot(s1.num, s1.ref))


class DUP2_X1(NoOperandsInstruction):
    def execute(self, frame: Frame):
        stack = frame.operand_stack()
        s1 = stack.pop_slot()
        s2 = stack.pop_slot()
        s3 = stack.pop_slot()
        stack.push_slot(s2)
        stack.push_slot(s1)
        stack.push_slot(s3)
        stack.push_slot(Slot(s2.num, s2.ref))
        stack.push_slot(Slot(s1.num, s1.ref))


class DUP2_X2(NoOperandsInstruction):
    def execute(self, frame: Frame):
        stack = frame.operand_stack()
        s1 = stack.pop_slot()
        s2 = stack.pop_slot()
        s3 = stack.pop_slot()
        s4 = stack.pop_slot()
        stack.push_slot(s2)
        stack.push_slot(s1)
        stack.push_slot(s4)
        stack.push_slot(s3)
        stack.push_slot(Slot(s2.num, s2.ref))
        stack.push_slot(Slot(s1.num, s2.ref))


from runtime.slot import Slot