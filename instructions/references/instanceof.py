from runtime.frame import Frame
from ..instruction import Index16Instruction
from runtime.heap.cp_classref import ClassRef


class INSTANCE_OF(Index16Instruction):
    def execute(self, frame: Frame):
        stack = frame.operand_stack()
        ref = stack.pop_ref()
        if ref is None:
            stack.push_int(0)
            return

        cp = frame.method().class_.constantPool
        classRef = cp.get_constant(self.index)
        assert isinstance(classRef, ClassRef)
        cls = classRef.resolved_class()
        if ref.is_instance_of(cls):
            stack.push_int(1)
        else:
            stack.push_int(0)