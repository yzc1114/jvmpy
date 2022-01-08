from ..instruction import Instruction
from ..bytecode_reader import ByteCodeReader
from runtime.frame import Frame
from ..base.branch_logic import branch
import numpy as np


class TABLE_SWITCH(Instruction):
    def __init__(self):
        self.default_offset: np.int32 = None
        self.low: np.int32 = None
        self.high: np.int32 = None
        self.jump_offsets: [np.int32] = None

    def fetch_operands(self, reader: ByteCodeReader):
        reader.skip_padding()
        self.default_offset = reader.read_int32()
        self.low = reader.read_int32()
        self.high = reader.read_int32()
        jump_offsets_length = self.high - self.low + 1
        self.jump_offsets = reader.read_int32s(jump_offsets_length)

    def execute(self, frame: Frame):
        index = frame.operand_stack().pop_int()
        if self.low <= index <= self.high:
            offset = int(self.jump_offsets[index - self.low])
        else:
            offset = self.default_offset
        branch(frame, offset)
