from runtime.frame import Frame
from native.registry import NativeMethod
from runtime.heap.slots import Slots


unsafe = "sun/misc/Unsafe"


def init():
    NativeMethod.register(class_name=unsafe, method_name="arrayBaseOffset", method_descriptor="(Ljava/lang/Class;)I", method=ArrayBaseOffset())
    NativeMethod.register(class_name=unsafe, method_name="arrayIndexScale", method_descriptor="(Ljava/lang/Class;)I", method=ArrayIndexScale())
    NativeMethod.register(class_name=unsafe, method_name="addressSize",     method_descriptor="()I",                  method=AddressSize())
    NativeMethod.register(class_name=unsafe, method_name="objectFieldOffset", method_descriptor="(Ljava/lang/reflect/Field;)J", method=ObjectFieldOffset())
    NativeMethod.register(class_name=unsafe, method_name="compareAndSwapObject", method_descriptor="(Ljava/lang/Object;JLjava/lang/Object;Ljava/lang/Object;)Z", method=CompareAndSwapObject())
    NativeMethod.register(class_name=unsafe, method_name="getIntVolatile", method_descriptor="(Ljava/lang/Object;J)I", method=GetIntVolatile())
    NativeMethod.register(class_name=unsafe, method_name="getObjectVolatile", method_descriptor="(Ljava/lang/Object;J)Ljava/lang/Object;", method=GetObjectVolatile())
    NativeMethod.register(class_name=unsafe, method_name="compareAndSwapInt", method_descriptor="(Ljava/lang/Object;JII)Z", method=CompareAndSwapInt())
    NativeMethod.register(class_name=unsafe, method_name="compareAndSwapLong", method_descriptor="(Ljava/lang/Object;JJJ)Z", method=CompareAndSwapLong())

class ArrayBaseOffset(NativeMethod):
    """获得数组类的第一个元素与数组起始位置的偏移量"""
    def execute(self, frame: Frame):
        frame.operand_stack().push_int(0)


class ArrayIndexScale(NativeMethod):
    """获得数组每个元素的大小，单位字节，不需实现"""
    def execute(self, frame: Frame):
        frame.operand_stack().push_int(1)

class AddressSize(NativeMethod):
    """获得地址的字节大小"""
    def execute(self, frame: Frame):
        frame.operand_stack().push_int(8)

class ObjectFieldOffset(NativeMethod):
    """(Ljava/lang/reflect/Field;)J 获得Field对于对象首地址的偏移量，可以使用slotId来表示"""
    def execute(self, frame: Frame):
        vars = frame.local_vars()
        # java/reflect/Field
        java_field_obj = vars.get_ref(1)
        offset = java_field_obj.get_int_var("slot", "I")
        frame.operand_stack().push_long(offset)


class  CompareAndSwapObject(NativeMethod):
    """
    (Ljava/lang/Object;JLjava/lang/Object;Ljava/lang/Object;)Z
    模拟原子操作，比较并交换对象
    """
    def execute(self, frame: Frame):
        vars = frame.local_vars()
        obj = vars.get_ref(1)
        data = obj.data
        offset = vars.get_long(2)
        expected = vars.get_ref(3)
        new_val = vars.get_ref(4)

        if isinstance(data, Slots):
            # obj is not array
            curr = data.get_ref(offset)
            if curr == expected:
                data.set_ref(offset, new_val)
            swapped = curr == expected
        elif isinstance(data, list):
            # obj is object array
            curr = data[offset]
            if curr == expected:
                data[offset] = new_val
            swapped = curr == expected
        else:
            raise NotImplemented

        frame.operand_stack().push_boolean(swapped)


class GetIntVolatile(NativeMethod):
    def execute(self, frame: Frame):
        vars = frame.local_vars()
        data = vars.get_ref(1).data
        offset = vars.get_long(2)

        stack = frame.operand_stack()
        if isinstance(data, Slots):
            stack.push_int(data.get_int(offset))
        elif isinstance(data, list):
            stack.push_int(data[offset])
        else:
            raise NotImplemented


class GetObjectVolatile(NativeMethod):
    def execute(self, frame: Frame):
        vars = frame.local_vars()
        data = vars.get_ref(1).data
        offset = vars.get_long(2)

        stack = frame.operand_stack()
        if isinstance(data, Slots):
            stack.push_ref(data.get_ref(offset))
        elif isinstance(data, list):
            stack.push_ref(data[offset])
        else:
            raise NotImplemented


class CompareAndSwapInt(NativeMethod):
    """比较并交换整数"""
    def execute(self, frame: Frame):
        vars = frame.local_vars()
        obj = vars.get_ref(1)
        data = obj.data
        offset = vars.get_long(2)
        expected = vars.get_int(3)
        new_val = vars.get_int(4)

        if isinstance(data, Slots):
            # obj is not array
            curr = data.get_int(offset)
            if curr == expected:
                data.set_int(offset, new_val)
            swapped = curr == expected
        elif isinstance(data, list):
            # obj is object array
            curr = data[offset]
            if curr == expected:
                data[offset] = new_val
            swapped = curr == expected
        else:
            raise NotImplemented

        frame.operand_stack().push_boolean(swapped)


class CompareAndSwapLong(NativeMethod):
    """比较并交换长整形整数"""
    def execute(self, frame: Frame):
        vars = frame.local_vars()
        obj = vars.get_ref(1)
        data = obj.data
        offset = vars.get_long(2)
        expected = vars.get_long(3)
        new_val = vars.get_long(4)

        if isinstance(data, Slots):
            # obj is not array
            curr = data.get_int(offset)
            if curr == expected:
                data.set_long(offset, new_val)
            swapped = curr == expected
        elif isinstance(data, list):
            # obj is object array
            curr = data[offset]
            if curr == expected:
                data[offset] = new_val
            swapped = curr == expected
        else:
            raise NotImplemented

        frame.operand_stack().push_boolean(swapped)
