from ..instruction import Index16Instruction
from runtime.frame import Frame
from runtime.heap.cp_methodref import MethodRef
from ..base.method_invoke_logic import invoke_method


class INVOKE_SPECIAL(Index16Instruction):
    """
    执行实例方法；对超类，私有方法，实例初始化方法等做特殊处理；
    """
    def execute(self, frame: Frame):
        curr_class = frame.method().class_
        cp = curr_class.constantPool
        methodRef = cp.get_constant(self.index)
        assert isinstance(methodRef, MethodRef)
        resolved_class = methodRef.resolved_class()
        resolved_method = methodRef.resolved_method()
        # 如果是对象初始化的方法，则定义方法的类和该符号引用解析出来的类必须是同一个类
        if resolved_method.name() == "<init>" and resolved_method.class_ != resolved_class:
            raise Exception("java.lang.NoSuchMethodError")
        # 解析出来的类不能是静态类
        if resolved_method.is_static():
            raise Exception("java.lang.IncompatibleClassChangeError")

        # 弹出this引用
        ref = frame.operand_stack().get_ref_from_top(resolved_method.arg_slot_count - 1)
        if ref is None:
            raise Exception("java.lang.NullPointerException")

        if resolved_method.is_protected() and \
            resolved_method.class_.is_super_class_of(curr_class) and \
            resolved_method.class_.get_package_name() != curr_class.get_package_name() and \
            ref.cls != curr_class and \
            not ref.cls.is_sub_class_of(curr_class):
            raise Exception("java.lang.IllegalAccessError")
        method_to_be_invoked = resolved_method
        if curr_class.is_super() and \
            resolved_class.is_super_class_of(curr_class) and \
            resolved_method.name() != "<init>":
            # 调用超类中的函数，则需要去超类中寻找该函数
            super_class = curr_class.superClass
            if super_class is None:
                raise Exception("java.lang.AbstractMethodError")
            method_to_be_invoked = super_class.look_up_method(methodRef.name, methodRef.descriptor)

        if method_to_be_invoked is None or method_to_be_invoked.is_abstract():
            raise Exception("java.lang.AbstractMethodError")

        invoke_method(frame, method_to_be_invoked)