from native.registry import NativeMethod
from runtime.frame import Frame

jlt = "java/lang/Thread"

def init():
    NativeMethod.register(class_name=jlt, method_name="currentThread", method_descriptor="()Ljava/lang/Thread;", method=CurrentThread())
    NativeMethod.register(class_name=jlt, method_name="setPriority0", method_descriptor="(I)V", method=SetPriority0())
    NativeMethod.register(class_name=jlt, method_name="isAlive", method_descriptor="()Z", method=IsAlive())
    NativeMethod.register(class_name=jlt, method_name="start0", method_descriptor="()V", method=Start0())


class CurrentThread(NativeMethod):
    """
    public static native Thread currentThread();
    ()Ljava/lang/Thread;
    """
    def execute(self, frame: Frame):
        # TODO
        class_loader = frame.method().class_.loader
        thread_class = class_loader.load_class("java/lang/Thread")
        j_thread = thread_class.new_object()

        thread_group_class = class_loader.load_class("java/lang/ThreadGroup")
        j_group = thread_group_class.new_object()

        j_thread.set_ref_var("group", "Ljava/lang/ThreadGroup;", j_group)
        j_thread.set_int_var("priority", "I", 1)

        frame.operand_stack().push_ref(j_thread)


class SetPriority0(NativeMethod):
    """
    private native void setPriority0(int newPriority);
    (I)V
    """
    def execute(self, frame: Frame):
        # TODO
        pass


class IsAlive(NativeMethod):
    """
    public final native boolean isAlive();
    ()Z
    """
    def execute(self, frame: Frame):
        # TODO
        stack = frame.operand_stack()
        stack.push_boolean(False)


class Start0(NativeMethod):
    """
    private native void start0();
    ()V
    """
    def execute(self, frame: Frame):
        # TODO
        pass