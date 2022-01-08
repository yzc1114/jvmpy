from runtime.frame import Frame
from ..instruction import Index16Instruction
from runtime.heap.cp_fieldref import FieldRef
from ..base.class_init_logic import init_class

class GETSTATIC(Index16Instruction):
    descriptor_to_behavior = {
        'Z': lambda slots, slot_id, stack: stack.push_int(slots.get_int(slot_id)),
        'B': lambda slots, slot_id, stack: stack.push_int(slots.get_int(slot_id)),
        'C': lambda slots, slot_id, stack: stack.push_int(slots.get_int(slot_id)),
        'S': lambda slots, slot_id, stack: stack.push_int(slots.get_int(slot_id)),
        'I': lambda slots, slot_id, stack: stack.push_int(slots.get_int(slot_id)),
        'F': lambda slots, slot_id, stack: stack.push_float(slots.get_float(slot_id)),
        'J': lambda slots, slot_id, stack: stack.push_long(slots.get_long(slot_id)),
        'D': lambda slots, slot_id, stack: stack.push_double(slots.get_double(slot_id)),
        'L': lambda slots, slot_id, stack: stack.push_ref(slots.get_ref(slot_id)),
        '[': lambda slots, slot_id, stack: stack.push_ref(slots.get_ref(slot_id)),
    }

    def execute(self, frame: Frame):
        # 该类的常量池
        cp = frame.method().class_.constantPool
        # 通过操作数获得字段的符号引用
        fieldRef = cp.get_constant(self.index)
        assert isinstance(fieldRef, FieldRef)
        # 通过符号引用得到直接引用
        field = fieldRef.resolved_field()
        # 通过直接引用获得该字段所在的类的直接饮用
        cls = field.class_
        # 如果类没有初始化，则需要将下一pc回调到执行该命令之前，然后调用clinit方法进行类的初始化
        if not cls.initStarted:
            frame.revert_next_pc()
            init_class(thread=frame.thread(), cls=cls)
            return

        if not field.is_static():
            # 若字段不是静态的，则报错。指令只针对静态常量
            raise Exception("java.lang.IncompatibleClassChangeError")

        descriptor = field.descriptor()
        slot_id = field.slotId
        slots = cls.staticVars
        stack = frame.operand_stack()
        # 根据字段的描述符确定数据类型，从而设置正确的数据类型
        if descriptor[0] in self.descriptor_to_behavior.keys():
            self.descriptor_to_behavior[descriptor[0]](slots, slot_id, stack)