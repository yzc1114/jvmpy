from runtime.frame import Frame
from ..base.method_invoke_logic import invoke_method
from runtime.heap.cp_methodref import MethodRef
from ..instruction import Index16Instruction
from ..base.class_init_logic import init_class


class INVOKE_STATIC(Index16Instruction):
    def execute(self, frame: Frame):
        cp = frame.method().class_.constantPool
        methodRef = cp.get_constant(self.index)
        assert isinstance(methodRef, MethodRef)
        m = methodRef.resolved_method()
        # 必须为静态方法
        if not m.is_static():
            raise Exception("java.lang.IncompatibleClassChangeError")

        cls = methodRef.resolved_class()
        # 如果类没有初始化，则需要将下一pc回调到执行该命令之前，然后调用clinit方法进行类的初始化
        if not cls.initStarted:
            frame.revert_next_pc()
            init_class(thread=frame.thread(), cls=cls)
            return

        invoke_method(frame, m)