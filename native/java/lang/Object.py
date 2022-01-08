from native.registry import NativeMethod
from runtime.frame import Frame

def init():
    NativeMethod.register("java/lang/Object", "getClass", "()Ljava/lang/Class;", GetClass())
    NativeMethod.register("java/lang/Object", "hashCode", "()I", HashCode())
    NativeMethod.register("java/lang/Object", "clone", "()Ljava/lang/Object;", Clone())

class GetClass(NativeMethod):
    def execute(self, frame: Frame):
        this = frame.local_vars().get_this()
        # 获得该对象的类对象
        cls = this.cls.jClass
        frame.operand_stack().push_ref(cls)


class HashCode(NativeMethod):
    def execute(self, frame: Frame):
        this = frame.local_vars().get_this()
        hash = id(this)
        frame.operand_stack().push_int(hash)


class Clone(NativeMethod):
    def execute(self, frame: Frame):
        this = frame.local_vars().get_this()
        cloneable = this.cls.loader.load_class("java/lang/Cloneable")
        if not this.cls.is_implements(cloneable):
            raise Exception("java.lang.CloneNotSupportedException")

        frame.operand_stack().push_ref(this.clone())