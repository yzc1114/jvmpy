from runtime.frame import Frame
from ..instruction import Index16Instruction
from runtime.heap.cp_fieldref import FieldRef
from ..base.class_init_logic import init_class


class PUTSTATIC(Index16Instruction):
    descriptor_to_behavior = {
        'Z': lambda slots, slot_id, stack: slots.set_int(slot_id, stack.pop_int()),
        'B': lambda slots, slot_id, stack: slots.set_int(slot_id, stack.pop_int()),
        'C': lambda slots, slot_id, stack: slots.set_int(slot_id, stack.pop_int()),
        'S': lambda slots, slot_id, stack: slots.set_int(slot_id, stack.pop_int()),
        'I': lambda slots, slot_id, stack: slots.set_int(slot_id, stack.pop_int()),
        'F': lambda slots, slot_id, stack: slots.set_float(slot_id, stack.pop_float()),
        'J': lambda slots, slot_id, stack: slots.set_long(slot_id, stack.pop_long()),
        'D': lambda slots, slot_id, stack: slots.set_double(slot_id, stack.pop_double()),
        'L': lambda slots, slot_id, stack: slots.set_ref(slot_id, stack.pop_ref()),
        '[': lambda slots, slot_id, stack: slots.set_ref(slot_id, stack.pop_ref())
    }

    def execute(self, frame: Frame):
        # 调用该指令的方法
        curr_method = frame.method()
        # 调用该指令的方法所在的类
        curr_cls = frame.method().class_
        # 该类的常量池
        cp = curr_cls.constantPool
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
        if field.is_final():
            # 若字段是final字段，则只有当该字段属于当前类，并且当前方法名为<clinit>时，才可以被设置。
            if curr_cls != cls or curr_method.name() != "<clinit>":
                raise Exception("java.lang.IllegalAccessError")

        descriptor = field.descriptor()
        slot_id = field.slotId
        slots = cls.staticVars
        stack = frame.operand_stack()
        # 根据字段的描述符确定数据类型，从而设置正确的数据类型
        if descriptor[0] in self.descriptor_to_behavior.keys():
            self.descriptor_to_behavior[descriptor[0]](slots, slot_id, stack)
