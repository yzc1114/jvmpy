from native.registry import NativeMethod
from runtime.frame import Frame
from utils.bits_converter import *


def init():
    NativeMethod.register("java/lang/Float", "floatToRawIntBits", "(F)I", FloatToRawIntBits())
    NativeMethod.register("java/lang/Float", "IntBitsToFloat", "(I)F", IntBitsToFloat())


class FloatToRawIntBits(NativeMethod):
    def execute(self, frame: Frame):
        val = frame.local_vars().get_float(0)
        frame.operand_stack().push_int(bytes_to_int32(float32_to_bytes(val)))


class IntBitsToFloat(NativeMethod):
    def execute(self, frame: Frame):
        val = frame.local_vars().get_int(0)
        frame.operand_stack().push_int(bytes_to_float32(int32_to_bytes(val)))