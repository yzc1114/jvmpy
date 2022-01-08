from ..instruction import Index16Instruction
from runtime.frame import Frame
from runtime.heap.cp_classref import ClassRef


class ANEW_ARRAY(Index16Instruction):
    def execute(self, frame: Frame):
        cp = frame.method().class_.constantPool
        classRef = cp.get_constant(self.index)
        assert isinstance(classRef, ClassRef)
        # component_class 为元素的类型
        component_class = classRef.resolved_class()

        stack = frame.operand_stack()
        count = stack.pop_int()
        if count < 0:
            raise Exception("java.lang.NegativeArraySizeException")

        arr_class = component_class.array_class()
        arr = arr_class.new_array_object(count)
        stack.push_ref(arr)