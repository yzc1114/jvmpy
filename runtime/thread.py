from .frame import Frame


class Thread(object):
    def __init__(self):
        # pc，当前执行代码的
        self.__pc: int = None
        self.__stack: Stack = Stack(2 ** 20)

    def pc(self):
        return self.__pc

    def set_pc(self, pc: int):
        self.__pc = pc

    def push_frame(self, frame: Frame):
        self.__stack.push(frame)

    def pop_frame(self) -> Frame:
        return self.__stack.pop()

    def current_frame(self) -> Frame:
        return self.__stack.top()

    def top_frame(self) -> Frame:
        return self.__stack.top()

    def new_frame(self, method) -> Frame:
        return Frame(thread=self, method=method)

    def is_stack_empty(self) -> bool:
        return self.__stack.size == 0

    def clear_stack(self):
        while self.__stack.size > 0:
            self.__stack.pop()

    def get_frames(self):
        return self.__stack.get_frames()

from .jvm_stack import Stack
