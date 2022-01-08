from ..instruction import NoOperandsInstruction, Index8Instruction
from runtime.frame import Frame


class LLOAD(Index8Instruction):
    def execute(self, frame: Frame):
        _lload(frame, self.index)


class LLOAD_0(NoOperandsInstruction):
    def execute(self, frame: Frame):
        _lload(frame, 0)


class LLOAD_1(NoOperandsInstruction):
    def execute(self, frame: Frame):
        _lload(frame, 1)


class LLOAD_2(NoOperandsInstruction):
    def execute(self, frame: Frame):
        _lload(frame, 2)


class LLOAD_3(NoOperandsInstruction):
    def execute(self, frame: Frame):
        _lload(frame, 3)


def _lload(frame: Frame, index: int):
    val = frame.local_vars().get_long(index)
    frame.operand_stack().push_long(val)
