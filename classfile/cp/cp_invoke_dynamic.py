from classfile.class_reader import ClassReader
from ..constant_info import ConstantInfo
import numpy as np


class ConstantMethodHandleInfo(ConstantInfo):

    def __init__(self):
        self.referenceKind: np.uint8 = None
        self.referenceIndex: np.uint16 = None

    def read_info(self, reader: ClassReader):
        self.referenceKind = reader.read_uint8()
        self.referenceIndex = reader.read_uint16()


class ConstantMethodTypeInfo(ConstantInfo):

    def __init__(self):
        self.descriptorIndex: np.uint16 = None

    def read_info(self, reader: ClassReader):
        self.descriptorIndex = reader.read_uint16()


class ConstantInvokeDynamicInfo(ConstantInfo):

    def __init__(self):
        self.bootstrapMethodAttrIndex: np.uint16 = None
        self.nameAndTypeIndex: np.uint16 = None

    def read_info(self, reader: ClassReader):
        self.bootstrapMethodAttrIndex = reader.read_uint16()
        self.nameAndTypeIndex = reader.read_uint16()
