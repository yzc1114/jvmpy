from native.registry import NativeMethod
from runtime.frame import Frame
from runtime.heap.method import Method, Class


def init():
    NativeMethod.register(class_name="sun/reflect/Reflection", method_name="getCallerClass", method_descriptor="()Ljava/lang/Class;", method=GetCallerClass())
    NativeMethod.register(class_name="sun/reflect/Reflection", method_name="getClassAccessFlags", method_descriptor="(Ljava/lang/Class;)I", method=GetClassAccessFlags())


class GetCallerClass(NativeMethod):
    """
    public static native Class<?> getCallerClass();
    获取调用该函数的函数的类
    """
    def execute(self, frame: Frame):
        # 获取第三个栈帧，即为调用该native method外的函数栈帧
        f = frame.thread().get_frames()[2]
        m = f.method()
        assert isinstance(m, Method)
        frame.operand_stack().push_ref(m.class_.jClass)


class GetClassAccessFlags(NativeMethod):
    """
    public static native int getClassAccessFlags(Class<?> type);
    获取类的访问权限
    """
    def execute(self, frame: Frame):
        _type = frame.local_vars().get_ref(0)
        # _type为类对象，其中extra指向其py中的类对象
        cls = _type.extra
        assert isinstance(cls, Class)
        frame.operand_stack().push_int(cls.accessFlags)