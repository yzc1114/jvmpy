from abc import ABCMeta, abstractmethod
from .class_reader import ClassReader


class ConstantInfo(metaclass=ABCMeta):

    @abstractmethod
    def read_info(self, reader: ClassReader):
        pass

