from runtime.frame import Frame
from abc import ABCMeta, abstractmethod


class NativeMethod(metaclass=ABCMeta):

    registry: dict = {}

    @abstractmethod
    def execute(self, frame: Frame):
        pass

    @classmethod
    def register(cls, class_name: str, method_name: str, method_descriptor: str, method):
        assert isinstance(method, NativeMethod)
        key = class_name + "~" + method_name + "~" + method_descriptor
        cls.registry[key] = method

    @classmethod
    def find_native_method(cls, class_name: str, method_name: str, method_descriptor: str):
        key = class_name + "~" + method_name + "~" + method_descriptor
        if key in cls.registry.keys():
            return cls.registry[key]
        # TODO hack here
        if method_name == "registerNatives" or method_name == "initIDs":
            return cls.empty_native_method()
        return None

    @classmethod
    def empty_native_method(cls):
        class EmptyNativeMethod(NativeMethod):
            def execute(self, frame: Frame):
                pass
        return EmptyNativeMethod()


from native.java.lang import *
from native.sun.misc import *
from native.sun.reflect import *
from native.java.security import *
from native.java.util.concurrent.atomic import *