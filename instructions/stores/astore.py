from ..instruction import NoOperandsInstruction, Index8Instruction
from runtime.frame import Frame


class ASTORE(Index8Instruction):
    def execute(self, frame: Frame):
        _astore(frame, self.index)


class ASTORE_0(NoOperandsInstruction):
    def execute(self, frame: Frame):
        _astore(frame, 0)


class ASTORE_1(NoOperandsInstruction):
    def execute(self, frame: Frame):
        _astore(frame, 1)


class ASTORE_2(NoOperandsInstruction):
    def execute(self, frame: Frame):
        _astore(frame, 2)


class ASTORE_3(NoOperandsInstruction):
    def execute(self, frame: Frame):
        _astore(frame, 3)


def _astore(frame: Frame, index: int):
    ref = frame.operand_stack().pop_ref()
    frame.local_vars().set_ref(index, ref)
