import numpy as np


class MethodDescriptor(object):
    def __init__(self):
        self.parameterTypes: [str] = []
        self.returnType: [str] = []

    def add_parameter_type(self, t):
        self.parameterTypes.append(t)


class MethodDescriptorParser(object):
    def __init__(self):
        self.__raw: str = None
        self.__offset: int = 0
        self.__parsed: MethodDescriptor = None
    
    @staticmethod
    def parse(descriptor: str) -> MethodDescriptor:
        parser = MethodDescriptorParser()
        return parser.__parse(descriptor)
    
    def __parse(self, descriptor: str) -> MethodDescriptor:
        self.__raw = descriptor
        self.__parsed = MethodDescriptor()
        self.__start_params()
        self.__parse_param_types()
        self.__end_params()
        self.__parse_return_type()
        self.__finish()
        return self.__parsed

    def __raise_exception(self):
        raise Exception("BAD descriptor: " + self.__raw)

    def __start_params(self):
        if self.__read_uint8() != '(':
            self.__raise_exception()

    def __end_params(self):
        if self.__read_uint8() != ')':
            self.__raise_exception()

    def __finish(self):
        if self.__offset != len(self.__raw):
            self.__raise_exception()


    def __read_uint8(self) -> str:
        b = self.__raw[self.__offset]
        self.__offset += 1
        return b

    def __unread_uint8(self):
        self.__offset -= 1

    def __parse_param_types(self):
        while True:
            t = self.__parse_field_type()
            if t != '':
                self.__parsed.add_parameter_type(t)
            else:
                break

    def __parse_return_type(self):
        if self.__read_uint8() == 'V':
            self.__parsed.returnType = 'V'
            return

        self.__unread_uint8()
        t = self.__parse_field_type()
        if t != '':
            self.__parsed.returnType = t
            return

        self.__raise_exception()

    def __parse_field_type(self):
        c = self.__read_uint8()
        if c in ['B', 'C', 'D', 'F', 'I', 'J', 'S', 'Z']:
            return c
        elif c == 'L':
            return self.__parse_object_type()
        elif c == '[':
            return self.__parse_array_type()
        else:
            self.__unread_uint8()
            return ""

    def __parse_object_type(self):
        unread = self.__raw[self.__offset:]
        semicolon_index = unread.index(';')
        if semicolon_index == -1:
            self.__raise_exception()
            return ""
        else:
            obj_start = self.__offset - 1
            obj_end = obj_start + semicolon_index + 2
            self.__offset = obj_end
            descriptor = self.__raw[obj_start: obj_end]
            return descriptor

    def __parse_array_type(self):
        arr_start = self.__offset - 1
        self.__parse_field_type()
        arr_end = self.__offset
        descriptor = self.__raw[arr_start:arr_end]
        return descriptor