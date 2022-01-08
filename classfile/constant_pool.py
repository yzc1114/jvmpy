import numpy as np


class ConstantPool(object):
    from .class_reader import ClassReader

    def __init__(self):
        self.constantInfos: [ConstantInfo] = []

    def __len__(self):
        return len(self.constantInfos)

    @staticmethod
    def read_constant_pool(reader: ClassReader):
        from classfile.constant_info_reader import read_constant_info
        cp_count = int(reader.read_uint16())
        cp = ConstantPool()
        cp.constantInfos.append(None)
        i = 1
        while i < cp_count:
            cp.constantInfos.append(read_constant_info(reader, cp))
            if isinstance(cp.constantInfos[-1], ConstantLongInfo) \
                    or isinstance(cp.constantInfos[-1], ConstantDoubleInfo):
                i += 2
                cp.constantInfos.append(None)
            else:
                i += 1

        return cp

    def get_constant_info(self, index: np.uint16):
        info = self.constantInfos[index]
        if info is None:
            raise Exception("无效的常量池索引: {}!".format(index))
        return info

    def get_class_name(self, index: np.uint16) -> str:
        class_info = self.constantInfos[index]
        assert isinstance(class_info, ConstantClassInfo)
        return self.get_utf8(class_info.nameIndex)

    def get_name_and_type(self, index: np.uint16) -> (str, str):
        nt_info = self.constantInfos[index]
        assert isinstance(nt_info, ConstantNameAndTypeInfo)
        name = self.get_utf8(nt_info.nameIndex)
        descriptor = self.get_utf8(nt_info.descriptorIndex)
        return name, descriptor

    def get_utf8(self, index: np.uint16) -> str:
        utf8_info = self.constantInfos[index]
        assert isinstance(utf8_info, ConstantUtf8Info)
        return utf8_info.string()

    def get_constant_infos(self) -> []:
        return self.constantInfos


from .cp.cp_numeric import *
from .cp.cp_name_and_type import *
from .cp.cp_utf8 import *
from .cp.cp_class import *
from .constant_info import ConstantInfo