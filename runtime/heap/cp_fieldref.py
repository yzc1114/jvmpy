from .cp_memberref import MemberRef
from .field import Field
from .constant_pool import ConstantPool
from .class_ import Class
from classfile.cp.cp_member_ref import ConstantFieldrefInfo


class FieldRef(MemberRef):
    def __init__(self):
        super().__init__()
        self.field: Field = None # 缓存解析后的字段指针

    @staticmethod
    def new_field_ref(cp: ConstantPool, ref_info: ConstantFieldrefInfo):
        ref = FieldRef()
        ref.copy_member_ref_info(ref_info)
        ref.cp = cp
        return ref

    def resolved_field(self):
        if self.field is None:
            self.__resolve_field_ref()
        return self.field

    def __resolve_field_ref(self):
        d = self.cp.cls
        c = self.resolved_class()
        f = c.look_up_field(self.name, self.descriptor)
        if f is None:
            raise Exception("java.lang.NoSuchFieldError")
        if not f.is_accessible_to(d):
            raise Exception("java.lang.IllegalAccessError")
        self.field = f
