import numpy as np
from ..class_reader import ClassReader
from ..attribute_info import AttributeInfo


class LineNumberTableAttribute(AttributeInfo):
    def __init__(self):
        self.lineNumberTable: [LineNumberTableEntry] = None

    def read_info(self, reader: ClassReader):
        self.lineNumberTable = []
        line_number_table_length = reader.read_uint16()
        for i in range(line_number_table_length):
            entry = LineNumberTableEntry()
            entry.startPc = reader.read_uint16()
            entry.lineNumber = reader.read_uint16()
            self.lineNumberTable.append(entry)

    def get_line_number(self, pc: int):
        for e in reversed(self.lineNumberTable):
            assert isinstance(e, LineNumberTableEntry)
            if pc >= int(e.startPc):
                return int(e.lineNumber)
        return -1

    def __getitem__(self, item):
        return self.lineNumberTable[item]

    def __len__(self):
        return len(self.lineNumberTable)


class LineNumberTableEntry(object):
    def __init__(self):
        self.startPc: np.uint16 = None
        self.lineNumber: np.uint16 = None
