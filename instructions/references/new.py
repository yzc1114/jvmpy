from runtime.frame import Frame
from ..instruction import Index16Instruction
from runtime.heap.cp_classref import ClassRef
from ..base.class_init_logic import init_class


class NEW(Index16Instruction):
    """
    new对象指令
    """
    def execute(self, frame: Frame):
        # 首先找到当前调用栈的方法的类的运行时常量池
        cp = frame.method().class_.constantPool
        # 操作数可以从该运行时常量池中获得需要被new的类的符号引用
        classRef = cp.get_constant(self.index)
        assert isinstance(classRef, ClassRef)
        # 从符号引用获得实例的类
        cls = classRef.resolved_class()
        # 如果类没有初始化，则需要将下一pc回调到执行该命令之前，然后调用clinit方法进行类的初始化
        if not cls.initStarted:
            frame.revert_next_pc()
            init_class(thread=frame.thread(), cls=cls)
            return

        # 若此类是接口或者是抽象类则报错
        if cls.is_interface() or cls.is_abstract():
            raise Exception("java.lang.InstantiationError")
        # 使用Class类中的方法new到该对象
        ref = cls.new_object()
        # 将该对象引用push到操作栈中
        frame.operand_stack().push_ref(ref)