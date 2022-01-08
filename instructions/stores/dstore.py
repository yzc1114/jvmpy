from ..instruction import NoOperandsInstruction, Index8Instruction
from runtime.frame import Frame


class DSTORE(Index8Instruction):
    def execute(self, frame: Frame):
        _dstore(frame, self.index)


class DSTORE_0(NoOperandsInstruction):
    def execute(self, frame: Frame):
        _dstore(frame, 0)


class DSTORE_1(NoOperandsInstruction):
    def execute(self, frame: Frame):
        _dstore(frame, 1)


class DSTORE_2(NoOperandsInstruction):
    def execute(self, frame: Frame):
        _dstore(frame, 2)


class DSTORE_3(NoOperandsInstruction):
    def execute(self, frame: Frame):
        _dstore(frame, 3)


def _dstore(frame: Frame, index: int):
    val = frame.operand_stack().pop_double()
    frame.local_vars().set_double(index, val)
