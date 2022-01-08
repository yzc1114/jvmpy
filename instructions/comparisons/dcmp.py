from ..instruction import NoOperandsInstruction
from runtime.frame import Frame


class DCMPG(NoOperandsInstruction):
    def execute(self, frame: Frame):
        _dcmp(frame, True)


class DCMPL(NoOperandsInstruction):
    def execute(self, frame: Frame):
        _dcmp(frame, True)


def _dcmp(frame: Frame, g_flag: bool):
    stack = frame.operand_stack()
    v2 = stack.pop_double()
    v1 = stack.pop_double()
    if v1 > v2:
        stack.push_int(1)
    elif v1 == v2:
        stack.push_int(0)
    elif v1 < v2:
        stack.push_int(-1)
    elif g_flag:
        stack.push_int(1)
    else:
        stack.push_int(-1)
