from classfile.class_reader import ClassReader
from ..constant_info import ConstantInfo
import numpy as np


class ConstantNameAndTypeInfo(ConstantInfo):

    def __init__(self):
        self.nameIndex: np.uint16 = None
        self.descriptorIndex: np.uint16 = None

    def read_info(self, reader: ClassReader):
        self.nameIndex = reader.read_uint16()
        self.descriptorIndex = reader.read_uint16()
