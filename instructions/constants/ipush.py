from ..instruction import Instruction
from ..bytecode_reader import ByteCodeReader
from runtime.frame import Frame
import numpy as np


class BIPUSH(Instruction):
    """
    向栈中推入字节Byte
    """
    def __init__(self):
        self.val: np.int8 = None

    def fetch_operands(self, reader: ByteCodeReader):
        self.val = reader.read_int8()

    def execute(self, frame: Frame):
        frame.operand_stack().push_int(int(self.val))


class SIPUSH(Instruction):
    """
    向栈中压入short
    """
    def __init__(self):
        self.val: np.int16 = None

    def fetch_operands(self, reader: ByteCodeReader):
        self.val = reader.read_int16()

    def execute(self, frame: Frame):
        frame.operand_stack().push_int(int(self.val))
