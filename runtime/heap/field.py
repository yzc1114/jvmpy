from .class_member import ClassMember, Class
from classfile.member_info import MemberInfo
from .access_flags import *
from .class_name_helper import to_class_name


class Field(ClassMember):
    def __init__(self):
        super().__init__()
        self.constValueIndex: int = 0
        self.slotId: int = None

    @staticmethod
    def new_fields(cls: Class, cf_fields: [MemberInfo]) -> []:
        fields = [Field() for _ in range(len(cf_fields))]
        for i in range(len(cf_fields)):
            f = fields[i]
            f.class_ = cls
            f.copy_member_info(cf_fields[i])
            f.copy_attributes(cf_fields[i])
        return fields

    def copy_attributes(self, cf_field: MemberInfo):
        val_attr = cf_field.constant_value_attribute()
        if val_attr is not None:
            self.constValueIndex = int(val_attr.constant_value_index())

    def is_long_or_double(self):
        return self.descriptor() == 'J' or self.descriptor() == 'D'

    def is_static(self) -> bool:
        return 0 != (ACC_STATIC & self.access_flags())

    def is_final(self) -> bool:
        return 0 != (ACC_FINAL & self.access_flags())

    def type(self):
        return self.class_.loader.load_class(to_class_name(self.descriptor()))
