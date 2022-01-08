from ..instruction import Instruction
from runtime.frame import Frame
from ..base.branch_logic import branch
from ..bytecode_reader import ByteCodeReader


class GOTO_W(Instruction):
    def __init__(self):
        self.offset: int = None

    def fetch_operands(self, reader: ByteCodeReader):
        self.offset = int(reader.read_int32())

    def execute(self, frame: Frame):
        branch(frame, self.offset)
