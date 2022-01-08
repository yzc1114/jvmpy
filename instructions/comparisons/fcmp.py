from ..instruction import NoOperandsInstruction
from runtime.frame import Frame


class FCMPG(NoOperandsInstruction):
    def execute(self, frame: Frame):
        _fcmp(frame, True)


class FCMPL(NoOperandsInstruction):
    def execute(self, frame: Frame):
        _fcmp(frame, True)


def _fcmp(frame: Frame, g_flag: bool):
    stack = frame.operand_stack()
    v2 = stack.pop_float()
    v1 = stack.pop_float()
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
