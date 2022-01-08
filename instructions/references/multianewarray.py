from ..instruction import Instruction
from runtime.frame import Frame
from ..bytecode_reader import ByteCodeReader
from runtime.heap.cp_classref import ClassRef
from runtime.heap.object import Object


class MULTI_ANEW_ARRAY(Instruction):
    def __init__(self):
        self.index: int = None
        self.dimensions: int = None

    def fetch_operands(self, reader: ByteCodeReader):
        self.index = reader.read_uint16()
        self.dimensions = reader.read_uint8()

    def execute(self, frame: Frame):
        cp = frame.method().class_.constantPool
        classRef = cp.get_constant(self.index)
        assert isinstance(classRef, ClassRef)
        # 使用该类引用可以解析出数组的类
        arr_class = classRef.resolved_class()

        stack = frame.operand_stack()
        # 将每个维度的维数检查出来
        counts = self.__pop_and_check_counts(stack, self.dimensions)

        arr = self.__new_multi_dimensional_array(counts, arr_class)


    @staticmethod
    def __pop_and_check_counts(stack, dimensions):
        counts = [0 for _ in range(dimensions)]
        for i in reversed(range(dimensions)):
            counts[i] = stack.pop_int()
            if counts[i] < 0:
                raise Exception("java.lang.NegativeArraySizeException")
        return counts

    def __new_multi_dimensional_array(self, counts, arr_class) -> Object:
        count = counts[0]
        arr = arr_class.new_array_object(count)

        if len(counts) > 1:
            refs = arr.refs()
            for i in range(len(refs)):
                refs[i] = self.__new_multi_dimensional_array(counts[1:], arr_class=arr_class.component_class())