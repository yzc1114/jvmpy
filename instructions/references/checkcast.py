from runtime.frame import Frame
from ..instruction import Index16Instruction
from runtime.heap.cp_classref import ClassRef


class CHECK_CAST(Index16Instruction):
    def execute(self, frame: Frame):
        stack = frame.operand_stack()
        ref = stack.pop_ref()
        stack.push_ref(ref)
        if ref is None:
            return

        cp = frame.method().class_.constantPool
        classRef = cp.get_constant(self.index)
        assert isinstance(classRef, ClassRef)
        cls = classRef.resolved_class()
        if not ref.is_instance_of(cls):
            raise Exception("java.lang.ClassCastException")