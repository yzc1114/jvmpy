from ..instruction import Instruction
from ..bytecode_reader import ByteCodeReader
from runtime.frame import Frame
from ..base.branch_logic import branch
import numpy as np


class LOOKUP_SWITCH(Instruction):
    def __init__(self):
        self.default_offset: np.int32 = None
        self.npairs: np.int32 = None
        self.match_offsets: [np.int32] = None

    def fetch_operands(self, reader: ByteCodeReader):
        reader.skip_padding()
        self.default_offset = reader.read_int32()
        self.npairs = reader.read_int32()
        self.match_offsets = reader.read_int32s(self.npairs * 2)

    def execute(self, frame: Frame):
        key = frame.operand_stack().pop_int()
        i = 0
        while i < self.npairs * 2:
            if self.match_offsets[i] == key:
                offset = self.match_offsets[i + 1]
                branch(frame, offset)
                return
            i += 2
        branch(frame, int(self.default_offset))
