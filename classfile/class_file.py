import numpy as np


class ClassFile(object):
    from .class_reader import ClassReader
    from .member_info import MemberInfo

    def __init__(self):
        self.__minor_version: np.uint8 = 0
        self.__major_version: np.uint8 = 0
        self.__constant_pool: ConstantPool = None
        self.__access_flags: np.uint16 = 0
        self.__this_class: np.uint16 = 0
        self.__super_class: np.uint16 = 0
        self.__interfaces: [np.uint16] = []
        self.__fields: [MemberInfo] = []
        self.__methods: [MemberInfo] = []
        self.__attributes: [AttributeInfo] = []

    def read(self, reader: ClassReader):
        self.read_and_check_magic(reader)
        self.read_and_check_version(reader)
        self.__constant_pool = ConstantPool.read_constant_pool(reader)
        self.__access_flags = reader.read_uint16()
        self.__this_class = reader.read_uint16()
        self.__super_class = reader.read_uint16()
        self.__interfaces = reader.read_uint16s()
        self.__fields = MemberInfo.read_members(reader, cp=self.__constant_pool)
        self.__methods = MemberInfo.read_members(reader, cp=self.__constant_pool)
        self.__attributes = read_attributes(reader, cp=self.__constant_pool)

    @staticmethod
    def read_and_check_magic(reader: ClassReader):
        val = reader.read_uint32()
        if val != 0xCAFEBABE:
            raise Exception('java.lang.ClassFormatError: magic!')

    def read_and_check_version(self, reader: ClassReader):
        self.__minor_version = reader.read_uint16()
        self.__major_version = reader.read_uint16()
        if self.major_version == 45:
            return
        elif self.major_version in [46, 47, 48, 49, 50, 51, 52]:
            if self.minor_version == 0:
                return
        raise Exception("java.lang.UnsupportedClassVersionError!")

    def class_name(self) -> str:
        return self.constant_pool.get_class_name(self.this_class)

    def super_class_name(self) -> str:
        if self.super_class > 0:
            return self.constant_pool.get_class_name(self.super_class)
        return ""

    def interfaces_names(self) -> [str]:
        inames = []
        for i in self.interfaces:
            inames.append(self.constant_pool.get_class_name(i))
        return inames

    def source_file_attribute(self):
        for attr in self.attributes:
            if isinstance(attr, SourceFileAttribute):
                return attr
        return None


    @property
    def minor_version(self):
        return self.__minor_version
    
    @minor_version.setter
    def minor_version(self, val):
        self.__minor_version = val

    @property
    def major_version(self):
        return self.__major_version

    @major_version.setter
    def major_version(self, val):
        self.__major_version = val

    @property
    def constant_pool(self):
        return self.__constant_pool

    @constant_pool.setter
    def constant_pool(self, val):
        self.__constant_pool = val

    @property
    def access_flags(self):
        return self.__access_flags

    @access_flags.setter
    def access_flags(self, val):
        self.__access_flags = val

    @property
    def this_class(self):
        return self.__this_class

    @this_class.setter
    def this_class(self, val):
        self.__this_class = val

    @property
    def super_class(self):
        return self.__super_class

    @super_class.setter
    def super_class(self, val):
        self.__super_class = val

    @property
    def interfaces(self):
        return self.__interfaces

    @interfaces.setter
    def interfaces(self, val):
        self.__interfaces = val

    @property
    def fields(self) -> [MemberInfo]:
        return self.__fields

    @fields.setter
    def fields(self, val):
        self.__fields = val

    @property
    def methods(self):
        return self.__methods

    @methods.setter
    def methods(self, val):
        self.__methods = val

    @property
    def attributes(self):
        return self.__attributes

    @attributes.setter
    def attributes(self, val):
        self.__attributes = val


def parse(class_data: bytes) -> ClassFile:
    class_reader = ClassReader(class_data)
    class_file = ClassFile()
    class_file.read(class_reader)
    return class_file


from .constant_pool import ConstantPool
from .attribute_info import AttributeInfo, read_attributes
from .class_reader import ClassReader
from .member_info import MemberInfo
from .attr.attr_source_file import SourceFileAttribute