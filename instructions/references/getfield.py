from runtime.frame import Frame
from ..instruction import Index16Instruction
from runtime.heap.cp_fieldref import FieldRef


class GETFIELD(Index16Instruction):
    def execute(self, frame: Frame):
        cp = frame.method().class_.constantPool
        fieldRef = cp.get_constant(self.index)
        assert isinstance(fieldRef, FieldRef)
        field = fieldRef.resolved_field()

        if field.is_static():
            raise Exception("java.lang.IncompatibleClassChangeError")


        # 获得字段的描述符
        descriptor = field.descriptor()
        # 获得字段的变量槽id
        slot_id = field.slotId
        stack = frame.operand_stack()
        ref = stack.pop_ref()
        if ref is None:
            raise Exception("java.lang.NullPointerException")

        slots = ref.data

        if descriptor[0] in ['Z', 'B', 'C', 'S', 'I']:
            stack.push_int(slots.get_int(slot_id))
        elif descriptor.startswith('F'):
            stack.push_float(slots.get_float(slot_id))
        elif descriptor.startswith('J'):
            stack.push_long(slots.get_long(slot_id))
        elif descriptor.startswith('D'):
            stack.push_double(slots.get_double(slot_id))
        elif descriptor[0] in ['L', '[']:
            stack.push_ref(slots.get_ref(slot_id))
