"""
符号引用共同祖先
"""
from .constant_pool import ConstantPool
from .class_ import Class

class SymRef(object):
    def __init__(self):
        self.cp: ConstantPool = None  # 该符号引用所在的运行时常量池
        self.class_name: str = None   # 该符号引用所指的类名，对于字段引用和方法引用，也指的是所在的类的类名
        self.cls: Class = None        # 用来缓存已经解析后的类类指针，所以类符号引用只需要解析一次

    def resolved_class(self) -> Class:
        if self.cls is None:
            self.__resolve_class_ref()
        return self.cls

    def __resolve_class_ref(self):
        d = self.cp.cls # 该符号引用所在的运行时常量池所属于的类
        c = d.loader.load_class(self.class_name) # 该符号引用所在的类
        if not c.is_accessible_to(d):
            raise Exception("java.lang.IllegalAccessError")
        self.cls = c