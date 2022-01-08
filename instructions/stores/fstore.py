from ..instruction import NoOperandsInstruction, Index8Instruction
from runtime.frame import Frame


class FSTORE(Index8Instruction):
    def execute(self, frame: Frame):
        _fstore(frame, self.index)


class FSTORE_0(NoOperandsInstruction):
    def execute(self, frame: Frame):
        _fstore(frame, 0)


class FSTORE_1(NoOperandsInstruction):
    def execute(self, frame: Frame):
        _fstore(frame, 1)


class FSTORE_2(NoOperandsInstruction):
    def execute(self, frame: Frame):
        _fstore(frame, 2)


class FSTORE_3(NoOperandsInstruction):
    def execute(self, frame: Frame):
        _fstore(frame, 3)


def _fstore(frame: Frame, index: int):
    val = frame.operand_stack().pop_float()
    frame.local_vars().set_float(index, val)
