from native.registry import NativeMethod
from runtime.frame import Frame
from instructions.base.method_invoke_logic import invoke_method


def init():
    NativeMethod.register(class_name="java/security/AccessController", method_name="doPrivileged", method_descriptor="(Ljava/security/PrivilegedExceptionAction;)Ljava/lang/Object;", method=DoPrivileged())
    NativeMethod.register(class_name="java/security/AccessController", method_name="doPrivileged", method_descriptor="(Ljava/security/PrivilegedAction;)Ljava/lang/Object;", method=DoPrivileged())
    NativeMethod.register(class_name="java/security/AccessController", method_name="getStackAccessControlContext", method_descriptor="()Ljava/security/AccessControlContext;", method=GetStackAccessControlContext())


class DoPrivileged(NativeMethod):
    """
    @CallerSensitive
    public static native <T> T doPrivileged(PrivilegedAction<T> action);
    (Ljava/security/PrivilegedAction;)Ljava/lang/Object;
    """
    def execute(self, frame: Frame):
        vars = frame.local_vars()
        action = vars.get_ref(0)

        stack = frame.operand_stack()
        stack.push_ref(action)

        method = action.cls.get_instance_method("run", "()Ljava/lang/Object;")
        invoke_method(frame, method)


class GetStackAccessControlContext(NativeMethod):
    """
    private static native AccessControlContext getStackAccessControlContext();
    ()Ljava/security/AccessControlContext;
    """
    def execute(self, frame: Frame):
        # TODO
        frame.operand_stack().push_ref(None)