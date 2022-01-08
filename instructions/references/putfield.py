from runtime.frame import Frame
from ..instruction import Index16Instruction
from runtime.heap.cp_fieldref import FieldRef


class PUTFIELD(Index16Instruction):
    def execute(self, frame: Frame):
        curr_method = frame.method()
        curr_cls = curr_method.class_
        cp = frame.method().class_.constantPool
        fieldRef = cp.get_constant(self.index)
        assert isinstance(fieldRef, FieldRef)
        field = fieldRef.resolved_field()

        if field.is_static():
            raise Exception("java.lang.IncompatibleClassChangeError")

        if field.is_final():
            # 对象中的final变量初始化必须在<init>方法中
            if curr_cls != field.class_ or curr_method.name() != "<init>":
                raise Exception("java.lang.IllegalAccessError")

        # 获得字段的描述符
        descriptor = field.descriptor()
        # 获得字段的变量槽id
        slot_id = field.slotId

        stack = frame.operand_stack()

        if descriptor[0] in ['Z', 'B', 'C', 'S', 'I']:
            # val为要被put的值
            val = stack.pop_int()
            # ref为被put的值所属的对象
            ref = stack.pop_ref()
            # 需要检查是否为空指针
            self.__raise_exception_if_none(ref)
            # 在此处将值真正的设置上
            ref.data.set_int(slot_id, val)
        elif descriptor.startswith('F'):
            val = stack.pop_float()
            ref = stack.pop_ref()
            self.__raise_exception_if_none(ref)
            ref.data.set_float(slot_id, val)
        elif descriptor.startswith('J'):
            val = stack.pop_long()
            ref = stack.pop_ref()
            self.__raise_exception_if_none(ref)
            ref.data.set_long(slot_id, val)
        elif descriptor.startswith('D'):
            val = stack.pop_double()
            ref = stack.pop_ref()
            self.__raise_exception_if_none(ref)
            ref.data.set_double(slot_id, val)
        elif descriptor[0] in ['L', '[']:
            val = stack.pop_ref()
            ref = stack.pop_ref()
            self.__raise_exception_if_none(ref)
            ref.data.set_ref(slot_id, val)


    @staticmethod
    def __raise_exception_if_none(ref):
        if ref is None:
            raise Exception("java.lang.NullPointerException")