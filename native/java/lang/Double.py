from native.registry import NativeMethod
from runtime.frame import Frame
from utils.bits_converter import *


def init():
    NativeMethod.register("java/lang/Double", "doubleToRawLongBits", "(D)J", DoubleToRawIntBits())
    NativeMethod.register("java/lang/Double", "longBitsToDouble", "(J)D", LongBitsToDouble())


class DoubleToRawIntBits(NativeMethod):
    def execute(self, frame: Frame):
        val = frame.local_vars().get_double(0)
        frame.operand_stack().push_long(bytes_to_int64(float64_to_bytes(val)))

class LongBitsToDouble(NativeMethod):
    def execute(self, frame: Frame):
        val = frame.local_vars().get_long(0)
        frame.operand_stack().push_double(bytes_to_float64(int64_to_bytes(val)))
