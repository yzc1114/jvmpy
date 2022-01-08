from ..instruction import Index8Instruction, Index16Instruction
from runtime.frame import Frame
from runtime.heap.cp_classref import ClassRef
from runtime.heap.string_pool import StringPool
import numpy as np


class LDC(Index8Instruction):
    def execute(self, frame: Frame):
        _ldc(frame, self.index)


class LDC_W(Index16Instruction):
    def execute(self, frame: Frame):
        _ldc(frame, self.index)

class LDC2_W(Index16Instruction):
    def execute(self, frame: Frame):
        stack = frame.operand_stack()
        cp = frame.method().class_.constantPool
        c = cp.get_constant(self.index)

        if isinstance(c, np.int64):
            stack.push_long(int(c))
        elif isinstance(c, np.float64):
            stack.push_double(float(c))
        else:
            raise Exception("java.lang.ClassFormatError")


def _ldc(frame: Frame, index: int):
    stack = frame.operand_stack()
    cp = frame.method().class_.constantPool
    cls = frame.method().class_
    c = cp.get_constant(index)
    if isinstance(c, np.int32):
        stack.push_int(int(c))
    elif isinstance(c, np.float32):
        stack.push_float(float(c))
    elif isinstance(c, str):
        interned_str = StringPool.java_string(cls.loader, c)
        stack.push_ref(interned_str)
    elif isinstance(c, ClassRef):
        class_obj = c.resolved_class().jClass
        stack.push_ref(class_obj)
    else:
        raise Exception("java.lang.ClassFormatError")
