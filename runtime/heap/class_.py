from classfile.class_file import ClassFile
from .class_name_helper import get_array_class_name, get_component_class_name, PRIMTIVE_TYPES_DICT
import numpy as np

class Class(object):
    """
    表示方法区内的类
    """
    def __init__(self, cf: ClassFile = None):
        self.loader = None
        self.superClass: Class = None
        self.interfaces: [Class] = []
        self.instanceSlotCount: int = 0
        self.staticSlotCount: int = 0
        self.staticVars: Slots = Slots(max_locals=0)
        self.initStarted: bool = False
        self.jClass: Object = None
        self.source_file: str = "Unknown" if cf is None or cf.source_file_attribute() is None else cf.source_file_attribute().file_name()

        if cf is not None:
            self.accessFlags: int = cf.access_flags
            self.name: str = cf.class_name()
            self.superClassName: str = cf.super_class_name()
            self.interfaceNames: [str] = cf.interfaces_names()
            self.constantPool: ConstantPool = ConstantPool(self, cf.constant_pool)
            self.fields: [Field] = Field.new_fields(self, cf.fields)
            self.methods: [Method] = Method.new_methods(self, cf.methods)
            return

        self.accessFlags: int = None
        self.name: str = None
        self.superClassName: str = None
        self.interfaceNames: [str] = None
        self.constantPool: ConstantPool = None
        self.fields: [Field] = []
        self.methods: [Method] = []

    def java_name(self):
        return self.name.replace("/", ".")

    def is_accessible_to(self, cls):
        return self.is_public() or self.get_package_name() == cls.get_package_name()

    def is_public(self):
        return 0 != (self.accessFlags & ACC_PUBLIC)

    def is_interface(self):
        return 0 != (self.accessFlags & ACC_INTERFACE)

    def is_abstract(self):
        return 0 != (self.accessFlags & ACC_ABSTRACT)

    def is_super(self):
        return 0 != (self.accessFlags & ACC_SUPER)

    def is_array(self):
        return self.name[0] == '['

    def is_primitive(self):
        return self.name in PRIMTIVE_TYPES_DICT.keys()

    def is_jl_object(self):
        return self.name == "java/lang/Object"

    def is_jl_cloneable(self):
        return self.name == "java/lang/Cloneable"

    def is_jio_serializable(self):
        return self.name == "java/io/serializable"

    def get_package_name(self):
        if '/' in self.name:
            return "/".join(self.name.split("/")[:-1])
        return ""

    def start_init(self):
        self.initStarted = True

    def get_field(self, name: str, descriptor: str, is_static: bool):
        c = self
        while c is not None:
            for f in self.fields:
                assert isinstance(f, Field)
                if f.is_static() == is_static and f.name() == name and f.descriptor() == descriptor:
                    return f
            c = c.superClass
        return None

    def get_field_slot_id(self, name: str, descriptor: str, is_static: bool):
        c = self
        while c is not None:
            for f in self.fields:
                assert isinstance(f, Field)
                if f.is_static() == is_static and f.name() == name and f.descriptor() == descriptor:
                    return f.slotId
            c = c.superClass
        return -1

    def look_up_field(self, name: str, descriptor: str):
        for f in self.fields:
            if f.name() == name and f.descriptor() == descriptor:
                return f
        for i in self.interfaces:
            assert isinstance(i, Class)
            f = i.look_up_field(name, descriptor)
            if f is not None:
                return f
        if self.superClass is not None:
            return self.superClass.look_up_field(name, descriptor)
        return None

    def get_method(self, name: str, descriptor: str, is_static: bool):
        c = self
        while c is not None:
            for m in c.methods:
                assert isinstance(m, Method)
                if m.is_static() == is_static and m.name() == name and m.descriptor() == descriptor:
                    return m
            c = c.superClass
        return None

    def look_up_method(self, name: str, descriptor: str):
        m = self.__look_up_method_in_class(name, descriptor)
        if m is None:
            m = self.__look_up_method_in_interfaces(self.interfaces, name, descriptor)
        return m

    def look_up_interface_method(self, name: str, descriptor: str):
        for m in self.methods:
            if m.name() == name and m.descriptor() == descriptor:
                return m
        return self.__look_up_method_in_interfaces(self.interfaces, name, descriptor)

    def __look_up_method_in_class(self, name: str, descriptor: str):
        c = self
        while c is not None:
            for m in c.methods:
                if m.name() == name and m.descriptor() == descriptor:
                    return m
            c = c.superClass
        return None

    @classmethod
    def __look_up_method_in_interfaces(cls, interfaces, name: str, descriptor: str):
        for interface in interfaces:
            assert isinstance(interface, Class)
            assert interface.is_interface()
            for m in interface.methods:
                if m.name() == name and m.descriptor() == descriptor:
                    return m
            m = cls.__look_up_method_in_interfaces(interface.interfaces, name, descriptor)
            if m is not None:
                return m
        return None

    def new_object(self):
        return Object(self)

    array_object_dict = {
        '[Z': lambda cls, count: Object(cls, [np.int8(0) for _ in range(count)]),
        '[B': lambda cls, count: Object(cls, [np.int8(0) for _ in range(count)]),
        '[C': lambda cls, count: Object(cls, [np.uint16(0) for _ in range(count)]),
        '[S': lambda cls, count: Object(cls, [np.int16(0) for _ in range(count)]),
        '[I': lambda cls, count: Object(cls, [np.int32(0) for _ in range(count)]),
        '[J': lambda cls, count: Object(cls, [np.int64(0) for _ in range(count)]),
        '[F': lambda cls, count: Object(cls, [np.float32(0.0) for _ in range(count)]),
        '[D': lambda cls, count: Object(cls, [np.float64(0.0) for _ in range(count)]),
    }

    def new_array_object(self, count: int):
        assert count >= 0
        if not self.is_array():
            raise Exception("Not array class: " + self.name)
        if self.name in self.array_object_dict.keys():
            obj = self.array_object_dict[self.name](self, count)
        else:
            obj = Object(self, [None for _ in range(count)])
        return obj

    def is_assignable_from(self, cls) -> bool:
        s, t = cls, self
        if s == t:
            return True
        assert isinstance(s, Class) and isinstance(t, Class)
        if not s.is_array():
            if not s.is_interface():
                if not t.is_interface():
                    return s.is_sub_class_of(t)
                else:
                    return s.is_implements(t)
            else:
                if not t.is_interface():
                    return t.is_jl_object()
                else:
                    return t.is_super_interface_of(s)
        else:
            if not t.is_array():
                if not t.is_interface():
                    return t.is_jl_object()
                else:
                    return t.is_jl_cloneable() or t.is_jio_serializable()
            else:
                sc = s.component_class()
                tc = t.component_class()
                return sc == tc or tc.is_assignable_from(sc)

    def is_sub_class_of(self, cls) -> bool:
        if self == cls:
            return False
        c = self.superClass
        while c is not None:
            if c == cls:
                return True
            else:
                c = c.superClass
        return False

    def is_super_class_of(self, cls) -> bool:
        return cls.is_sub_class_of(self)

    def is_implements(self, cls) -> bool:
        assert isinstance(cls, Class)
        assert cls.is_interface()
        c = self
        while c is not None:
            for i in c.interfaces:
                if i == cls or i.is_sub_interface_of(cls):
                    return True
            c = c.superClass
        return False

    def is_sub_interface_of(self, cls) -> bool:
        assert isinstance(cls, Class)
        assert cls.is_interface()
        assert self.is_interface()
        for i in self.interfaces:
            if i == cls or i.is_sub_interface_of(cls):
                return True
        return False

    def is_super_interface_of(self, cls) -> bool:
        return cls.is_sub_interface_of(self)

    def get_main_method(self):
        return self.get_static_method('main', '([Ljava/lang/String;)V')

    def get_static_method(self, name: str, descriptor: str):
        return self.get_method(name, descriptor, True)

    def get_instance_method(self, name: str, descriptor: str):
        return self.get_method(name, descriptor, False)

    def get_clinit_method(self):
        return self.get_static_method("<clinit>", "()V")

    def array_class(self):
        """获得该类作为元素的数组类"""
        array_class_name = get_array_class_name(class_name=self.name)
        return self.loader.load_class(array_class_name)

    def component_class(self):
        """获得元素的类"""
        assert self.is_array()
        component_class_name = get_component_class_name(self.name)
        return self.loader.load_class(component_class_name)

    def get_static_ref_var(self, field_name: str, field_descriptor: str):
        """获得静态变量对象的值"""
        f = self.get_field(name=field_name, descriptor=field_descriptor, is_static=True)
        return self.staticVars.get_ref(f.slotId)

    def set_static_ref_var(self, field_name: str, field_descriptor: str, ref):
        """设置静态变量对象的值"""
        assert isinstance(ref, Object)
        f = self.get_field(name=field_name, descriptor=field_descriptor, is_static=True)
        self.staticVars.set_ref(f.slotId, ref)

    def get_fields(self, public_only: bool):
        if public_only:
            public_fields = []
            for f in self.fields:
                assert isinstance(f, Field)
                if f.is_public():
                    public_fields.append(f)
            return public_fields
        else:
            return self.fields

    def get_methods(self, public_only: bool):
        methods = []
        for m in self.methods:
            assert isinstance(m, Method)
            if not m.is_clinit() and not m.is_constructor():
                if not public_only or not m.is_public():
                    methods.append(m)
        return methods

    def get_constructor(self, descriptor: str):
        return self.get_instance_method(name="<init>", descriptor=descriptor)

    def get_constructors(self, public_only: bool):
        methods = []
        for m in self.methods:
            assert isinstance(m, Method)
            if m.is_constructor():
                if not public_only or not m.is_public():
                    methods.append(m)
        return methods


from .object import Object
from .constant_pool import ConstantPool
from .field import Field
from .method import Method
from .slots import Slots
from .access_flags import *