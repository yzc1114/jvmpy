from classfile.class_reader import ClassReader
from ..constant_info import ConstantInfo
from ..constant_pool import ConstantPool
import numpy as np


class ConstantMemberrefInfo(ConstantInfo):

    def __init__(self, cp: ConstantPool):
        self.cp: ConstantPool = cp
        self.classIndex: np.uint16 = None
        self.nameAndTypeIndex: np.uint16 = None

    def read_info(self, reader: ClassReader):
        self.classIndex = reader.read_uint16()
        self.nameAndTypeIndex = reader.read_uint16()

    def class_name(self) -> str:
        return self.cp.get_class_name(self.classIndex)

    def name_and_descriptor(self) -> (str, str):
        return self.cp.get_name_and_type(self.nameAndTypeIndex)


class ConstantFieldrefInfo(ConstantMemberrefInfo):
    pass


class ConstantMethodrefInfo(ConstantMemberrefInfo):
    pass


class ConstantInterfaceMethodrefInfo(ConstantMemberrefInfo):
    pass
