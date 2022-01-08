from ..instruction import NoOperandsInstruction, Index8Instruction
from runtime.frame import Frame


class LSTORE(Index8Instruction):
    def execute(self, frame: Frame):
        _lstore(frame, self.index)


class LSTORE_0(NoOperandsInstruction):
    def execute(self, frame: Frame):
        _lstore(frame, 0)


class LSTORE_1(NoOperandsInstruction):
    def execute(self, frame: Frame):
        _lstore(frame, 1)


class LSTORE_2(NoOperandsInstruction):
    def execute(self, frame: Frame):
        _lstore(frame, 2)


class LSTORE_3(NoOperandsInstruction):
    def execute(self, frame: Frame):
        _lstore(frame, 3)


def _lstore(frame: Frame, index: int):
    val = frame.operand_stack().pop_long()
    frame.local_vars().set_long(index, val)
