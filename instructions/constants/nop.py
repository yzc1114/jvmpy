from ..instruction import NoOperandsInstruction
from runtime.frame import Frame


class NOP(NoOperandsInstruction):
    def execute(self, frame: Frame):
        pass
