from .frame import Frame


class Stack(object):
    def __init__(self, max_size: int):
        self.maxSize: int = max_size
        self.size: int = 0
        self.__top: Frame = None  # 使用单向链表的栈

    def push(self, frame: Frame):
        if self.size >= self.maxSize:
            raise Exception("java.lang.StackOverflowError")
        if self.__top is not None:
            frame.set_lower(self.__top)
        self.__top = frame
        self.size += 1

    def pop(self) -> Frame:
        if self.__top is None:
            raise Exception("jvm stack is empty!")
        top = self.__top
        self.__top = top.lower
        top.set_lower(None)
        self.size -= 1
        return top

    def top(self) -> Frame:
        if self.__top is None:
            raise Exception("jvm stack is empty!")
        return self.__top

    def get_frames(self) -> [Frame]:
        frames = []
        curr_f = self.top()
        while curr_f is not None:
            frames.append(curr_f)
            curr_f = curr_f.lower
        return frames
