from .local_vars import LocalVars
from .operand_stack import OperandStack
from .heap.method import Method


class Frame(object):

    def __init__(self, thread, method, ops = None):
        assert isinstance(method, Method)
        self.lower: Frame = None
        self.__localVars = LocalVars(max_locals=method.max_locals)
        self.__operandStack = ops if ops is not None else OperandStack(max_size=method.max_stack)
        self.__thread = thread
        self.__method = method
        self.nextPC = 0

    def set_lower(self, frame):
        self.lower = frame

    def local_vars(self) -> LocalVars:
        return self.__localVars

    def operand_stack(self) -> OperandStack:
        return self.__operandStack

    def set_next_pc(self, next_pc: int):
        self.nextPC = next_pc

    def next_pc(self) -> int:
        return self.nextPC

    def thread(self):
        return self.__thread

    def method(self) -> Method:
        return self.__method

    def revert_next_pc(self):
        self.nextPC = self.__thread.pc()