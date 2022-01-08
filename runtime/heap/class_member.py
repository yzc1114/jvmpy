from classfile import class_file
from .class_ import Class
from .access_flags import *

class ClassMember(object):
    def __init__(self):
        self.accessFlags: int = None
        self.name_: str = None
        self.descriptor_: str = None
        self.signature: str = None
        self.cls: Class = None
        self.annotationData: bytes = bytes()

    def copy_member_info(self, member_info: class_file.MemberInfo):
        self.accessFlags = member_info.access_flags()
        self.name_ = member_info.name()
        self.descriptor_ = member_info.descriptor()

    def access_flags(self):
        return self.accessFlags

    def name(self):
        return self.name_

    def descriptor(self):
        return self.descriptor_

    def is_public(self):
        return 0 != (ACC_PUBLIC & self.access_flags())

    def is_protected(self):
        return 0 != (ACC_PROTECTED & self.access_flags())

    def is_private(self):
        return 0 != (ACC_PRIVATE & self.access_flags())

    def is_static(self):
        return 0 != (ACC_STATIC & self.access_flags())

    def is_clinit(self):
        return self.name() == "<clinit>" and self.is_static()

    def is_constructor(self):
        return self.name() == "<init>" and self.is_static()

    def is_accessible_to(self, cls: Class):
        if self.is_public():
            return True
        c = self.class_
        if self.is_protected():
            return cls == c or cls.is_sub_class_of(c) or c.get_package_name() == cls.get_package_name()
        if not self.is_private():
            return c.get_package_name() == cls.get_package_name()
        return c == cls or c.name == cls.name

    @property
    def class_(self):
        return self.cls

    @class_.setter
    def class_(self, cls):
        assert isinstance(cls, Class)
        self.cls = cls