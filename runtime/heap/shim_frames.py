from ..frame import Frame
from ..thread import Thread
from ..operand_stack import OperandStack
from .class_ import Class
from .method import Method
from .access_flags import *


def new_shim_frame(thread: Thread, ops: OperandStack) -> Frame:
    return Frame(thread, method=_return_method, ops=ops)


_shim_class = Class()
_shim_class.name = "~shim"
_return_code = bytes([0xb1]) # return
_athrow_code = bytes([0xbf]) # athrow

_return_method = Method()
_return_method.accessFlags = ACC_STATIC
_return_method.name_ = "<return>"
_return_method.cls = _shim_class
_return_method.code = _return_code

_athrow_method = Method()
_athrow_method.accessFlags = ACC_STATIC
_athrow_method.name_ = "<athrow>"
_athrow_method.cls = _shim_class
_athrow_method.code = _athrow_code
