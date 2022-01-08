from .cp_memberref import MemberRef
from .method import Method
from .constant_pool import ConstantPool
from classfile.cp.cp_member_ref import ConstantMethodrefInfo


class MethodRef(MemberRef):
    def __init__(self):
        super().__init__()
        self.method: Method = None # 缓存解析后的方法指针

    @staticmethod
    def new_method_ref(cp: ConstantPool, ref_info: ConstantMethodrefInfo):
        ref = MethodRef()
        ref.copy_member_ref_info(ref_info)
        ref.cp = cp
        return ref

    def resolved_method(self):
        if self.method is None:
            self.__resolve_method()
        return self.method

    def __resolve_method(self):
        # d 为调用该方法所在的类
        d = self.cp.cls
        # c 为this指针所属的类
        c = self.resolved_class()
        # 若定义该方法的为接口，则该引用类型不正确。不应出现在此处，应该出现在cp_interface_methodref处
        if c.is_interface():
            raise Exception("java.lang.IncompatibleClassChangeError")

        method = c.look_up_method(self.name, self.descriptor)
        if method is None:
            raise Exception("java.lang.NoSuchMethodError")
        if not method.is_accessible_to(d):
            raise Exception("java.lang.IllegalAccessError")
        self.method = method