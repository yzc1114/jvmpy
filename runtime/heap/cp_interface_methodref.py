from .cp_memberref import MemberRef
from .method import Method
from .constant_pool import ConstantPool
from classfile.cp.cp_member_ref import ConstantInterfaceMethodrefInfo


class InterfaceMethodRef(MemberRef):
    def __init__(self):
        super().__init__()
        self.method: Method = None # 缓存解析后的方法指针

    @staticmethod
    def new_interface_method_ref(cp: ConstantPool, ref_info: ConstantInterfaceMethodrefInfo):
        ref = InterfaceMethodRef()
        ref.copy_member_ref_info(ref_info)
        ref.cp = cp
        return ref

    def resolved_interface_method(self):
        if self.method is None:
            self.__resolve_interface_method()
        return self.method

    def __resolve_interface_method(self):
        # 调用该方法所在的类
        d = self.cp.cls
        # 定义该方法的接口类
        c = self.resolved_class()
        if not c.is_interface():
            raise Exception("java.lang.IncompatibleClassChangeError")
        m = c.look_up_interface_method(self.name, self.descriptor)
        if m is None:
            raise Exception("java.lang.NoSuchMethodException")
        assert isinstance(m, Method)
        if not m.is_accessible_to(d):
            raise Exception("java.lang.IllegalAccessError")
        self.method = m