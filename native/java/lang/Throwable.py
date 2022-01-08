from native.registry import NativeMethod
from runtime.frame import Frame


def init():
    NativeMethod.register("java/lang/Throwable", "fillInStackTrace", "(I)Ljava/lang/Throwable;", FillInStackTrace())


class StackTraceElement(object):
    def __init__(self, frame: Frame):
        method = frame.method()
        cls = method.class_
        self.fileName: str = cls.source_file
        self.className: str = cls.java_name()
        self.methodName: str = method.name()
        self.lineNumber: int = method.get_line_number(frame.next_pc() - 1)

    def __str__(self):
        return "{}.{}({}.{})".format(self.className, self.methodName, self.fileName, self.lineNumber)


class FillInStackTrace(NativeMethod):
    def execute(self, frame: Frame):
        this = frame.local_vars().get_this()
        frame.operand_stack().push_ref(this)

        stes = self.__create_stack_trace_elements(tobj=this, thread=frame.thread())
        this.extra = stes

    def __create_stack_trace_elements(self, tobj, thread):
        skip = self.__distance_to_object(tobj.cls) + 2
        frames = thread.get_frames()[skip:]
        return [StackTraceElement(frame) for frame in frames]

    @staticmethod
    def __distance_to_object(cls):
        distance = 0
        c = cls
        while c is not None:
            distance += 1
            c = c.superClass
        return distance
