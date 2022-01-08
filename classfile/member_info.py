from .class_reader import ClassReader
import numpy as np


class MemberInfo(object):
    from .constant_pool import ConstantPool

    def __init__(self, cp: ConstantPool):
        self.cp: ConstantPool = cp
        self.accessFlags: np.uint16 = None
        self.nameIndex: np.uint16 = None
        self.descriptorIndex: np.uint16 = None
        self.attributes: [AttributeInfo] = None

    @classmethod
    def read_members(cls, reader: ClassReader, cp: ConstantPool) -> []:
        members_length = reader.read_uint16()
        members = []
        for i in range(members_length):
            members.append(cls.__read_member(reader, cp))
        return members

    @staticmethod
    def __read_member(reader: ClassReader, cp: ConstantPool):
        member = MemberInfo(cp)
        member.accessFlags = reader.read_uint16()
        member.nameIndex = reader.read_uint16()
        member.descriptorIndex = reader.read_uint16()
        member.attributes = read_attributes(reader, cp)
        return member

    def access_flags(self):
        return self.accessFlags

    def name(self):
        return self.cp.get_utf8(self.nameIndex)

    def descriptor(self):
        return self.cp.get_utf8(self.descriptorIndex)

    def code_attribute(self):
        for a in self.attributes:
            assert isinstance(a, AttributeInfo)
            if isinstance(a, CodeAttribute):
                return a
        return None

    def constant_value_attribute(self):
        for a in self.attributes:
            assert isinstance(a, AttributeInfo)
            if isinstance(a, ConstantValueAttribute):
                return a
        return None

    def exceptions_attribute(self):
        for attr_info in self.attributes:
            if isinstance(attr_info, ExceptionsAttribute):
                return attr_info
        return None

    def runtime_visible_annotations_attribute_data(self, ):
        return self.get_unparsed_attribute_data("RuntimeVisibleAnnotations")

    def runtime_visible_parameter_annotations_attribute_data(self):
        return self.get_unparsed_attribute_data("RuntimeVisibleParameterAnnotationsAttribute")

    def annotation_default_attribute_data(self):
        return self.get_unparsed_attribute_data("AnnotationDefault")

    def get_unparsed_attribute_data(self, name):
        for attr_info in self.attributes:
            if isinstance(attr_info, UnparsedAttribute):
                if attr_info.name == name:
                    return attr_info.info

        return None


from .constant_pool import ConstantPool
from .attribute_info import AttributeInfo, read_attributes
from .attr.attr_code import CodeAttribute
from .attr.attr_constant_value import ConstantValueAttribute
from .attr.attr_exceptions import ExceptionsAttribute
from .attr.attr_unparsed import UnparsedAttribute