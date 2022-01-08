from .cp_classref import ClassRef
from classfile.attr.attr_code import CodeAttribute
from .constant_pool import ConstantPool


class ExceptionHandler(object):
    def __init__(self):
        self.startPc: int = None
        self.endPc: int = None
        self.handlerPc: int = None
        self.catchType: ClassRef = None


class ExceptionTable(object):
    def __init__(self, table):
        self.table: [ExceptionHandler] = table

    def __getitem__(self, item):
        return self.table[item]

    @classmethod
    def new_exception_table(cls, entries: [CodeAttribute.ExceptionEntry], cp: ConstantPool):
        """
        从classfile中的code attribute中的ExceptionTable中提取出信息到[ExceptionHandler]中
        :param entries: classfile中的异常表
        :param cp: 运行时常量池
        :return:
        """
        table = [ExceptionHandler() for _ in range(len(entries))]

        for i, entry in enumerate(entries):
            assert isinstance(entry, CodeAttribute.ExceptionEntry)
            table[i].startPc = entry.start_pc()
            table[i].endPc = entry.end_pc()
            table[i].catchType = None if entry.catchType == 0 else cp.get_constant(entry.catchType)
            table[i].handlerPc = entry.handler_pc()
        return ExceptionTable(table)

    def find_exception_handler(self, ex_class, pc: int) -> ExceptionHandler:
        for handler in self.table:
            assert isinstance(handler, ExceptionHandler)
            if handler.startPc <= pc < handler.endPc:
                if handler.catchType is None:
                    # 若catchType是None，那么意味着该handler可以处理所有的异常
                    return handler
                catch_class = handler.catchType.resolved_class()
                if catch_class == ex_class or catch_class.is_super_class_of(ex_class):
                    return handler
        return None
