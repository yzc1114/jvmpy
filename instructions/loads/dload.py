from ..instruction import NoOperandsInstruction, Index8Instruction
from runtime.frame import Frame


class DLOAD(Index8Instruction):
    def execute(self, frame: Frame):
        _dload(frame, self.index)


class DLOAD_0(NoOperandsInstruction):
    def execute(self, frame: Frame):
        _dload(frame, 0)


class DLOAD_1(NoOperandsInstruction):
    def execute(self, frame: Frame):
        _dload(frame, 1)


class DLOAD_2(NoOperandsInstruction):
    def execute(self, frame: Frame):
        _dload(frame, 2)


class DLOAD_3(NoOperandsInstruction):
    def execute(self, frame: Frame):
        _dload(frame, 3)


def _dload(frame: Frame, index: int):
    val = frame.local_vars().get_double(index)
    frame.operand_stack().push_double(val)
