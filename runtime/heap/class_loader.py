from classpath.classpath import Classpath
from classpath.entry import Entry
from classfile.class_file import parse
from .class_ import Class
from .access_flags import *
from .string_pool import StringPool
from .class_name_helper import PRIMTIVE_TYPES_DICT


class ClassLoader(object):
    def __init__(self, cp: Classpath, verbose_class: bool):
        self.cp: Classpath =  cp
        self.class_map: {str: Class} = {} #  class map存储类名到类信息的映射，可以看做方法区的具体实现
        self.verbose_class = verbose_class
        self.__load_basic_classes()
        self.__load_primitive_classes()

    def load_class(self, name: str) -> Class:
        if name in self.class_map.keys():
            return self.class_map[name]
        if name[0] == '[':
            cls = self.__load_array_class(name)
        else:
            cls = self.__load_non_array_class(name)

        if "java/lang/Class" in self.class_map.keys():
            cls.jClass = self.class_map["java/lang/Class"].new_object()
            cls.jClass.extra = cls

        return cls

    def __load_non_array_class(self, name: str) -> Class:
        data, entry = self.__read_class(name)
        cls = self.__define_class(data)
        self.__link(cls)
        if not self.verbose_class:
            print("[Loaded {} from {}]".format(name, entry))
        return cls

    def __load_array_class(self, name: str) -> Class:
        cls = Class()
        cls.accessFlags = ACC_PUBLIC
        cls.name = name
        cls.loader = self
        cls.initStarted = True
        cls.superClass = self.load_class("java/lang/Object")
        cls.interfaces = [
            self.load_class("java/lang/Cloneable"),
            self.load_class("java/io/Serializable"),
        ]
        self.class_map[name] = cls
        return cls

    def __load_basic_classes(self):
        jl_class_class = self.load_class("java/lang/Class")
        for cls in self.class_map.values():
            assert isinstance(cls, Class)
            if cls.jClass is None:
                cls.jClass = jl_class_class.new_object()
                cls.jClass.extra = cls

    def __load_primitive_classes(self):
        for t in PRIMTIVE_TYPES_DICT.keys():
            self.__load_primitive_class(t)

    def __load_primitive_class(self, t: str):
        cls = Class()
        cls.accessFlags = ACC_PUBLIC
        cls.name = t
        cls.loader = self
        cls.initStarted = True
        cls.jClass = self.class_map["java/lang/Class"].new_object()
        cls.jClass.extra = cls
        self.class_map[cls.name] = cls

    def __read_class(self, name: str) -> (bytes, Entry):
        data, entry, err = self.cp.read_class(name)
        if err is not None:
            raise Exception("java.lang.ClassNotFoundException: " + name)
        return data, entry

    def __define_class(self, data: bytes) -> Class:
        cls = self.__parse_class(data)
        cls.loader = self
        self.__resolve_super_class(cls)
        self.__resolve_interfaces(cls)
        self.class_map[cls.name] = cls
        return cls

    @staticmethod
    def __parse_class(data: bytes) -> Class:
        cls = parse(data)
        return Class(cls)

    @staticmethod
    def __resolve_super_class(cls: Class):
        if cls.name != "java/lang/Object":
            cls.superClass = cls.loader.load_class(cls.superClassName)

    @staticmethod
    def __resolve_interfaces(cls: Class):
        interface_count = len(cls.interfaceNames)
        cls.interfaces = []
        if interface_count > 0:
            for interface_name in cls.interfaceNames:
                cls.interfaces.append(cls.loader.load_class(interface_name))

    def __link(self, cls: Class):
        self.__verify(cls)
        self.__prepare(cls)

    def __verify(self, cls: Class):
        pass

    def __prepare(self, cls: Class):
        self.__cal_instance_field_slot_ids(cls)
        self.__cal_static_field_slot_ids(cls)
        self.__alloc_and_init_static_vars(cls)

    @staticmethod
    def __cal_instance_field_slot_ids(cls: Class):
        slot_id = 0
        if cls.superClass is not None:
            slot_id = cls.superClass.instanceSlotCount
        for f in cls.fields:
            if not f.is_static():
                f.slotId = slot_id
                slot_id += 1
                if f.is_long_or_double():
                    slot_id += 1
        cls.instanceSlotCount = slot_id

    @staticmethod
    def __cal_static_field_slot_ids(cls: Class):
        slot_id = 0
        for f in cls.fields:
            if f.is_static():
                f.slotId = slot_id
                slot_id += 1
                if f.is_long_or_double():
                    slot_id += 1
        cls.staticSlotCount = slot_id

    @classmethod
    def __alloc_and_init_static_vars(cls, cls_: Class):
        cls_.staticVars = Slots(cls_.staticSlotCount)
        for f in cls_.fields:
            if f.is_static() and f.is_final():
                cls.__init_static_final_var(cls_, f)

    @staticmethod
    def __init_static_final_var(cls: Class, f):
        vars = cls.staticVars
        cp = cls.constantPool
        cp_index = f.constValueIndex
        slot_id = f.slotId

        if cp_index > 0:
            if f.descriptor() in ["Z", "B", "C", "B", "I"]:
                val = int(cp.get_constant(cp_index))
                vars.set_int(slot_id, val=val)
            elif f.descriptor() == "J":
                val = int(cp.get_constant(cp_index))
                vars.set_long(slot_id, val=val)
            elif f.descriptor() == "F":
                val = float(cp.get_constant(cp_index))
                vars.set_float(slot_id, val)
            elif f.descriptor() == "D":
                val = float(cp.get_constant(cp_index))
                vars.set_double(slot_id, val)
            elif f.descriptor() == "Ljava/lang/String;":
                pystr = cp.get_constant(cp_index)
                assert isinstance(pystr, str)
                java_str = StringPool.java_string(cls.loader, pystr)
                vars.set_ref(slot_id, java_str)

from .slots import Slots