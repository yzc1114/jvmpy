from ..instruction import Instruction
from ..bytecode_reader import ByteCodeReader
from ..loads import iload, lload, aload, dload, fload
from ..stores import astore, istore, lstore, dstore, fstore
from ..math import iinc
import numpy as np
from runtime.frame import Frame


class WIDE(Instruction):
    modified_map = {
        0x15: lambda: iload.ILOAD(),
        0x16: lambda: lload.LLOAD(),
        0x17: lambda: fload.FLOAD(),
        0x18: lambda: dload.DLOAD(),
        0x19: lambda: aload.ALOAD(),
        0x36: lambda: istore.ISTORE(),
        0x37: lambda: lstore.LSTORE(),
        0x38: lambda: fstore.FSTORE(),
        0x39: lambda: dstore.DSTORE(),
        0x3a: lambda: astore.ASTORE(),
        0x84: lambda: iinc.IINC()
    }

    def __init__(self):
        self.modified_inst: Instruction = None

    def fetch_operands(self, reader: ByteCodeReader):
        opcode = reader.read_uint8()
        if opcode in self.modified_map.keys():
            inst = self.modified_map[opcode]()
            if isinstance(inst, iinc.IINC):
                inst.index = np.uint(reader.read_uint16())
                inst.const = np.int32(reader.read_int16())
            else:
                inst.index = np.uint(reader.read_uint16())
            self.modified_inst = inst
        else:
            raise Exception("Unsupported opcode: 0x%x!" % opcode)

    def execute(self, frame: Frame):
        self.modified_inst.execute(frame)
