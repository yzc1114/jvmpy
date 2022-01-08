from .class_ import Class
from classfile import *
from classfile.cp import cp_numeric, cp_class, cp_utf8, cp_name_and_type, cp_string, cp_member_ref, cp_invoke_dynamic


Constant = object

class ConstantPool(object):

    def __init__(self, cls: Class, cf_cp: constant_pool.ConstantPool):
        self.cls: Class = None
        self.consts: [Constant] = None
        self.__new_constant_pool(cls, cf_cp)

    def get_constant(self, index: int) -> object:
        return self.consts[index]

    def __new_constant_pool(self, cls: Class, cf_cp: constant_pool.ConstantPool):
        cp_count = len(cf_cp)
        consts = [Constant() for _ in range(cp_count)]
        self.cls = cls
        self.consts = consts

        i = 0
        while i < cp_count:
            cp_info = cf_cp.get_constant_infos()[i]
            if isinstance(cp_info, cp_numeric.ConstantIntegerInfo) \
                or isinstance(cp_info, cp_numeric.ConstantFloatInfo):
                consts[i] = cp_info.value()
            elif isinstance(cp_info, cp_numeric.ConstantDoubleInfo) \
                or isinstance(cp_info, cp_numeric.ConstantLongInfo):
                consts[i] = cp_info.value()
                i += 1
            elif isinstance(cp_info, cp_string.ConstantStringInfo):
                consts[i] = cp_info.string()
            elif isinstance(cp_info, cp_class.ConstantClassInfo):
                consts[i] = ClassRef.new_class_ref(self, cp_info)
            elif isinstance(cp_info, cp_member_ref.ConstantFieldrefInfo):
                consts[i] = FieldRef.new_field_ref(self, cp_info)
            elif isinstance(cp_info, cp_member_ref.ConstantMethodrefInfo):
                consts[i] = MethodRef.new_method_ref(self, cp_info)
            elif isinstance(cp_info, cp_member_ref.ConstantInterfaceMethodrefInfo):
                consts[i] = InterfaceMethodRef.new_interface_method_ref(self, cp_info)
            i += 1

from .cp_classref import ClassRef
from .cp_fieldref import FieldRef
from .cp_methodref import MethodRef
from .cp_interface_methodref import InterfaceMethodRef