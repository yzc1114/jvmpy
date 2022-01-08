from abc import ABCMeta, abstractmethod
from .bytecode_reader import ByteCodeReader
from runtime.frame import Frame
import numpy as np


class Instruction(metaclass=ABCMeta):

    @abstractmethod
    def fetch_operands(self, reader: ByteCodeReader):
        pass

    @abstractmethod
    def execute(self, frame: Frame):
        pass


class NoOperandsInstruction(Instruction, metaclass=ABCMeta):
    def fetch_operands(self, reader: ByteCodeReader):
        pass

    @abstractmethod
    def execute(self, frame: Frame):
        pass


class Index8Instruction(Instruction, metaclass=ABCMeta):
    def __init__(self):
        self.index: np.uint = None

    def fetch_operands(self, reader: ByteCodeReader):
        self.index = np.uint(reader.read_uint8())

    @abstractmethod
    def execute(self, frame: Frame):
        pass


class Index16Instruction(Instruction, metaclass=ABCMeta):
    def __init__(self):
        self.index: np.uint = None

    def fetch_operands(self, reader: ByteCodeReader):
        self.index = np.uint(reader.read_uint16())

    @abstractmethod
    def execute(self, frame: Frame):
        pass


class BranchInstruction(Instruction, metaclass=ABCMeta):
    def __init__(self):
        self.offset: int = None

    def fetch_operands(self, reader: ByteCodeReader):
        self.offset = int(reader.read_int16())

    @abstractmethod
    def execute(self, frame: Frame):
        pass
