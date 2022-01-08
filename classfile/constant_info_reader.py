from .class_reader import ClassReader
from .cp.cp_class import ConstantClassInfo
from .cp.cp_invoke_dynamic import ConstantInvokeDynamicInfo, ConstantMethodHandleInfo, ConstantMethodTypeInfo
from .cp.cp_member_ref import ConstantFieldrefInfo, ConstantInterfaceMethodrefInfo, ConstantMethodrefInfo
from .cp.cp_name_and_type import ConstantNameAndTypeInfo
from .cp.cp_numeric import ConstantDoubleInfo, ConstantFloatInfo, ConstantIntegerInfo, ConstantLongInfo
from .cp.cp_string import ConstantStringInfo
from .cp.cp_utf8 import ConstantUtf8Info

CONSTANT_Class = 7
CONSTANT_Fieldref = 9
CONSTANT_Methodref = 10
CONSTANT_InterfaceMethodref = 11
CONSTANT_String = 8
CONSTANT_Integer = 3
CONSTANT_Float = 4
CONSTANT_Long = 5
CONSTANT_Double = 6
CONSTANT_NameAndType = 12
CONSTANT_Utf8 = 1
CONSTANT_MethodHandle = 15
CONSTANT_MethodType = 16
CONSTANT_InvokeDynamic = 18

CONST_DICT = {
        CONSTANT_Class: lambda cp: ConstantClassInfo(cp),
        CONSTANT_Double: lambda: ConstantDoubleInfo(),
        CONSTANT_Float: lambda: ConstantFloatInfo(),
        CONSTANT_Integer: lambda: ConstantIntegerInfo(),
        CONSTANT_Fieldref: lambda cp: ConstantFieldrefInfo(cp),
        CONSTANT_InterfaceMethodref: lambda cp: ConstantInterfaceMethodrefInfo(cp),
        CONSTANT_InvokeDynamic: lambda: ConstantInvokeDynamicInfo(),
        CONSTANT_String: lambda cp: ConstantStringInfo(cp),
        CONSTANT_Utf8: lambda: ConstantUtf8Info(),
        CONSTANT_Long: lambda: ConstantLongInfo(),
        CONSTANT_MethodHandle: lambda: ConstantMethodHandleInfo(),
        CONSTANT_NameAndType: lambda: ConstantNameAndTypeInfo(),
        CONSTANT_MethodType: lambda: ConstantMethodTypeInfo(),
        CONSTANT_Methodref: lambda cp: ConstantMethodrefInfo(cp)
}


from .constant_pool import ConstantPool
from .constant_info import ConstantInfo


def read_constant_info(reader: ClassReader, cp: ConstantPool) -> ConstantInfo:
    tag = reader.read_uint8()
    c = __new_constant_info(tag, cp=cp)
    c.read_info(reader)
    return c


def __new_constant_info(tag, cp: ConstantPool):
    try:
        return CONST_DICT[tag](cp)
    except Exception:
        try:
            return CONST_DICT[tag]()
        except Exception as e:
            raise e
