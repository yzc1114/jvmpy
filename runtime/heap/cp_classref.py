from .cp_symref import SymRef
from .constant_pool import ConstantPool
from classfile.cp.cp_class import ConstantClassInfo


class ClassRef(SymRef):
    def __init__(self):
        super().__init__()

    @staticmethod
    def new_class_ref(cp: ConstantPool, class_info: ConstantClassInfo):
        ref = ClassRef()
        ref.cp = cp
        ref.class_name = class_info.name()
        return ref