from .class_member import ClassMember, Class
from classfile.member_info import MemberInfo
from classfile.attr.attr_line_number_table import LineNumberTableAttribute, LineNumberTableEntry
from .method_descriptor import MethodDescriptorParser, MethodDescriptor
from .access_flags import *
from .exception_table import ExceptionTable
from classfile.attr.attr_exceptions import ExceptionsAttribute
from .class_name_helper import to_class_name


class Method(ClassMember):
    def __init__(self):
        super().__init__()
        self.max_stack: int = 0
        self.max_locals: int = 0
        self.code: bytes = None
        self.arg_slot_count: int = 0
        self.exceptionTable: ExceptionTable = None
        self.exceptions: ExceptionsAttribute = None
        self.lineNumberTable: LineNumberTableAttribute = None
        self.parsedDescriptor: MethodDescriptor = None
        self.annotationData: bytes = None
        self.parameterAnnotationData: bytes = None
        self.annotationDefaultData: bytes = None

    @classmethod
    def new_methods(self_cls, cls: Class, cf_methods: [MemberInfo]) -> []:
        methods = [Method() for _ in range(len(cf_methods))]
        for i in range(len(cf_methods)):
            methods[i] = self_cls.__new_method(cls, cf_methods[i])
        return methods

    @classmethod
    def __new_method(self_cls, cls: Class, cf_method: MemberInfo):
        method = Method()
        method.class_ = cls
        method.copy_member_info(cf_method)
        method.__copy_attributes(cf_method)
        md = MethodDescriptorParser.parse(method.descriptor())
        method.parsedDescriptor = md
        method.__cal_arg_slot_count(md.parameterTypes)
        if method.is_native():
            method.__inject_code_attribute(md.returnType)
        return method

    def find_exception_handler(self, ex_class: Class, pc: int) -> int:
        """
        通过异常的类和当前代码所在的pc，获取该catch段的pc
        """
        handler = self.exceptionTable.find_exception_handler(ex_class, pc)
        return handler.handlerPc if handler is not None else -1

    def get_line_number(self, pc: int) -> int:
        for i in reversed(range(len(self.lineNumberTable))):
            entry = self.lineNumberTable[i]
            assert isinstance(entry, LineNumberTableEntry)
            if pc >= entry.startPc:
                return entry.lineNumber
        return -1

    def __copy_attributes(self, cf_method: MemberInfo):
        code_attr = cf_method.code_attribute()
        if code_attr is not None:
            self.max_stack = code_attr.max_stack()
            self.max_locals = code_attr.max_locals()
            self.code = code_attr.code()
            self.exceptionTable = ExceptionTable.new_exception_table(code_attr.exceptionTable, self.class_.constantPool)
            self.lineNumberTable = code_attr.line_number_table_attribute()
        self.exceptions = cf_method.exceptions_attribute()
        self.annotationData = cf_method.runtime_visible_annotations_attribute_data()
        self.parameterAnnotationData = cf_method.runtime_visible_parameter_annotations_attribute_data()
        self.annotationDefaultData = cf_method.annotation_default_attribute_data()

    def __cal_arg_slot_count(self, parameter_types):
        self.arg_slot_count = 0
        for paramType in parameter_types:
            self.arg_slot_count += 1
            if paramType == "J" or paramType == "D":
                self.arg_slot_count += 1
        if not self.is_static():
            self.arg_slot_count += 1

    def __inject_code_attribute(self, return_type: str):
        # 这里随意的使用了4个字节作为栈的大小
        self.max_stack = 4
        # max_locals可以直接用arg_slot_count来确定，以为该Frame中的本地变量仅仅用来存放传入本地方法的参数
        self.max_locals = self.arg_slot_count
        if return_type[0] == 'V':
            self.code = bytes([0xfe, 0xb1]) # RETURN
        elif return_type[0] == 'D':
            self.code = bytes([0xfe, 0xaf]) # DRETURN
        elif return_type[0] == 'F':
            self.code = bytes([0xfe, 0xae]) # FRETURN
        elif return_type[0] == 'J':
            self.code = bytes([0xfe, 0xad]) # LRETURN
        elif return_type[0] in ['L', '[']:
            self.code = bytes([0xfe, 0xb0]) # ARETURN
        else:
            self.code = bytes([0xfe, 0xac]) # IRETURN

    def is_abstract(self):
        return 0 != (self.access_flags() & ACC_ABSTRACT)

    def is_native(self):
        return 0 != (self.access_flags() & ACC_NATIVE)

    def return_type(self):
        return self.class_.loader.load_class(to_class_name(self.parsedDescriptor.returnType))

    def parameter_types(self):
        if self.arg_slot_count == 0:
            return []

        param_types = self.parsedDescriptor.parameterTypes
        param_classes = []
        for t in param_types:
            param_class_name = to_class_name(t)
            param_classes.append(self.class_.loader.load_class(param_class_name))

        return param_classes


    def exception_types(self):
        if self.exceptions is None:
            return []

        ex_index_table = self.exceptions.exceptionIndexTable
        ex_classes = []
        cp = self.class_.constantPool

        for ex_index in ex_index_table:
            class_ref = cp.get_constant(ex_index)
            assert isinstance(class_ref, ClassRef)
            ex_classes.append(class_ref.resolved_class())

        return ex_classes

from runtime.heap.cp_classref import ClassRef