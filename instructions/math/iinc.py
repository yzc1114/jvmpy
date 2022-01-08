from ..instruction import Instruction
from ..bytecode_reader import ByteCodeReader
from runtime.frame import Frame
import numpy as np


class IINC(Instruction):
    def __init__(self):
        self.index: np.uint = None
        self.const: np.int32 = None

    def fetch_operands(self, reader: ByteCodeReader):
        self.index = np.uint(reader.read_uint8())
        self.const = np.int32(reader.read_int8())

    def execute(self, frame: Frame):
        local_vars = frame.local_vars()
        local_vars.set_int(self.index, local_vars.get_int(self.index) + self.const)
