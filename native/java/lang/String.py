from native.registry import NativeMethod
from runtime.frame import Frame
from runtime.heap.string_pool import StringPool
from runtime.heap.class_ import Class
from runtime.heap.object import Object


def init():
    NativeMethod.register("java/lang/String", "intern", "()Ljava/lang/String;", Intern())


class Intern(NativeMethod):
    def execute(self, frame: Frame):
        this = frame.local_vars().get_this()
        interned = StringPool.intern_string(this)
        frame.operand_stack().push_ref(interned)