from ..instruction import Instruction
from runtime.frame import Frame
from ..bytecode_reader import ByteCodeReader


class NEW_ARRAY(Instruction):

    CONST_AT_BOOLEAN = 4
    CONST_AT_CHAR = 5
    CONST_AT_FLOAT = 6
    CONST_AT_DOUBLE = 7
    CONST_AT_BYTE = 8
    CONST_AT_SHORT = 9
    CONST_AT_INT = 10
    CONST_AT_LONG = 11

    CONST_TO_NAME = {
        CONST_AT_BOOLEAN: "[Z",
        CONST_AT_BYTE: "[B",
        CONST_AT_CHAR: "[C",
        CONST_AT_SHORT: "[S",
        CONST_AT_INT: "[I",
        CONST_AT_LONG: "[J",
        CONST_AT_FLOAT: "[F",
        CONST_AT_DOUBLE: "[D",
    }

    def __init__(self):
        self.atype: int = None

    def fetch_operands(self, reader: ByteCodeReader):
        self.atype = int(reader.read_uint8())

    def execute(self, frame: Frame):
        stack = frame.operand_stack()
        count = stack.pop_int()
        if count < 0:
            raise Exception("java.lang.NegativeArraySizeException")
        class_loader = frame.method().class_.loader
        arr_class = self.__get_primitive_array_class(class_loader=class_loader, atype=self.atype)
        arr = arr_class.new_array_object(count)
        stack.push_ref(arr)

    def __get_primitive_array_class(self, class_loader, atype: int):
        if atype in self.CONST_TO_NAME.keys():
            return class_loader.load_class(self.CONST_TO_NAME[atype])
        else:
            raise Exception("Invalid atype!")
