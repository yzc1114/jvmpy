from runtime.frame import Frame
from ..instruction import NoOperandsInstruction
from native.registry import NativeMethod


class INVOKE_NATIVE(NoOperandsInstruction):
    def execute(self, frame: Frame):
        method = frame.method()
        class_name = method.class_.name
        method_name = method.name()
        method_descriptor = method.descriptor()

        native_method = NativeMethod.find_native_method(class_name, method_name, method_descriptor)
        if native_method is None:
            method_info = class_name + "." + method_name + "." + method_descriptor
            raise Exception("java.lang.UnsatisfiedLinkError: " + method_info)

        native_method.execute(frame)