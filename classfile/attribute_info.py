from abc import ABCMeta, abstractmethod
from .class_reader import ClassReader


class AttributeInfo(metaclass=ABCMeta):

    @abstractmethod
    def read_info(self, reader: ClassReader):
        pass


from .constant_pool import ConstantPool


def read_attributes(reader: ClassReader, cp: ConstantPool) -> [AttributeInfo]:
    attr_count = reader.read_uint16()
    attrs: [AttributeInfo] = []
    for i in range(attr_count):
        attrs.append(__read_attribute(reader, cp))
    return attrs


def __read_attribute(reader: ClassReader, cp: ConstantPool) -> AttributeInfo:
    attr_name_index = reader.read_uint16()
    attr_name = cp.get_utf8(attr_name_index)
    attr_len = int(reader.read_uint32())
    attr_info = __new_attribute_info(attr_name, attr_len, cp)
    attr_info.read_info(reader)
    return attr_info


ATTR_NAMES_TO_ATTRS = {
    'Code': lambda cp: attr_code.CodeAttribute(cp),
    'ConstantValue': lambda: attr_constant_value.ConstantValueAttribute(),
    'Deprecated': lambda: attr_markers.DeprecatedAttribute(),
    'Exceptions': lambda: attr_exceptions.ExceptionsAttribute(),
    'LineNumberTable': lambda: attr_line_number_table.LineNumberTableAttribute(),
    'LocalVariableTable': lambda: attr_local_variable_table.LocalVariableTableAttribute(),
    'SourceFile': lambda cp: attr_source_file.SourceFileAttribute(cp),
    'Synthetic': lambda: attr_markers.SyntheticAttribute()
}


def __new_attribute_info(attr_name: str, attr_len: int, cp: ConstantPool) -> AttributeInfo:
    if attr_name in ATTR_NAMES_TO_ATTRS.keys():
        try:
            return ATTR_NAMES_TO_ATTRS[attr_name](cp)
        except Exception:
            try:
                return ATTR_NAMES_TO_ATTRS[attr_name]()
            except Exception as e:
                raise e
    else:
        return attr_unparsed.UnparsedAttribute(attr_name, attr_len)


from .attr import *
