from native.registry import NativeMethod
from runtime.frame import Frame


def init():
    NativeMethod.register(class_name="java/util/concurrent/atomic/AtomicLong", method_name="VMSupportsCS8", method_descriptor="()Z", method=VMSupportsCS8())


class VMSupportsCS8(NativeMethod):
    def execute(self, frame: Frame):
        frame.operand_stack().push_boolean(False)
