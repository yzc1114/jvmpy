from ..instruction import Instruction
from ..bytecode_reader import ByteCodeReader
from runtime.frame import Frame
from runtime.heap.cp_interface_methodref import InterfaceMethodRef
from ..base.method_invoke_logic import invoke_method


class INVOKE_INTERFACE(Instruction):
    def __init__(self):
        self.index: int = None

    def fetch_operands(self, reader: ByteCodeReader):
        self.index = reader.read_uint16()
        # 历史原因 这里后面有两个参数，分别是方法的参数数量，和给某些虚拟机使用的参数
        reader.read_uint8() # arg slot count
        reader.read_uint8() # must be 0

    def execute(self, frame: Frame):
        cp = frame.method().class_.constantPool
        methodRef = cp.get_constant(self.index)
        assert isinstance(methodRef, InterfaceMethodRef)
        resolved_method = methodRef.resolved_interface_method()
        # 如果解析得到的方法是静态的或者是私有的，则报错
        if resolved_method.is_static() or resolved_method.is_private():
            raise Exception("java.lang.IncompatibleClassChangeError")
        # 获得this引用
        ref = frame.operand_stack().get_ref_from_top(resolved_method.arg_slot_count - 1)
        if ref is None:
            raise Exception("java.lang.NullPointerException")
        # 需要检测该对象所属的类是否实现了该方法所属的接口类
        if not ref.cls.is_implements(methodRef.resolved_class()):
            raise Exception("java.lang.IncompatibleClassChangeError")

        method_to_be_invoked = ref.cls.look_up_method(methodRef.name, methodRef.descriptor)
        if method_to_be_invoked is None or method_to_be_invoked.is_abstract():
            raise Exception("java.lang.AbstractMethodError")
        if not method_to_be_invoked.is_public():
            raise Exception("java.lang.IllegalAccessError")

        invoke_method(frame, method_to_be_invoked)