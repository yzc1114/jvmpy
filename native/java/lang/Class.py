from native.registry import NativeMethod
from runtime.frame import Frame
from runtime.heap.string_pool import StringPool
from runtime.heap.class_ import Class
from runtime.heap.class_loader import ClassLoader
from runtime.heap.shim_frames import new_shim_frame
from instructions.base import class_init_logic, method_invoke_logic


jlc = "java/lang/Class"


def init():
    NativeMethod.register(jlc, "getPrimitiveClass", "(Ljava/lang/String;)Ljava/lang/Class;", GetPrimitiveClass())
    NativeMethod.register(jlc, "getName0", "()Ljava/lang/String;", GetName0())
    NativeMethod.register(jlc, "desiredAssertionStatus0", "(Ljava/lang/Class;)Z", DesiredAssertionStatus0())
    NativeMethod.register(jlc, "isInterface", "()Z", IsInterface())
    NativeMethod.register(jlc, "isPrimitive", "()Z", IsPrimitive())
    NativeMethod.register(jlc, "getDeclaredFields0", "(Z)[Ljava/lang/reflect/Field;", GetDeclaredFields0())
    NativeMethod.register(jlc, "getDeclaredConstructors0", "(Z)[Ljava/lang/reflect/Constructor;", GetDeclaredConstructors0())
    NativeMethod.register(jlc, "forName0", "(Ljava/lang/String;ZLjava/lang/ClassLoader;Ljava/lang/Class;)Ljava/lang/Class;", ForName0())
    NativeMethod.register(jlc, "getModifiers", "()I", GetModifiers())
    NativeMethod.register(jlc, "getSuperclass", "()Ljava/lang/Class;", GetSuperClass())
    NativeMethod.register(jlc, "getInterfaces0", "()[Ljava/lang/Class;", GetInterfaces0())
    NativeMethod.register(jlc, "isArray", "()Z", IsArray())
    NativeMethod.register(jlc, "getDeclaredMethods0", "(Z)[Ljava/lang/reflect/Method;", GetDeclaredMethods0())
    NativeMethod.register(jlc, "getComponentType", "()Ljava/lang/Class;", GetComponentType())
    NativeMethod.register(jlc, "isAssignableFrom", "(Ljava/lang/Class;)Z", IsAssignableFrom())

# static native Class<?> getPrimitiveClass(String name)
class GetPrimitiveClass(NativeMethod):
    def execute(self, frame: Frame):
        name_obj = frame.local_vars().get_ref(0)
        name = StringPool.py_str(name_obj)

        loader = frame.method().class_.loader
        cls = loader.load_class(name).jClass

        frame.operand_stack().push_ref(cls)


# private native String getName0();
class GetName0(NativeMethod):
    def execute(self, frame: Frame):
        this = frame.local_vars().get_this()
        cls = this.extra
        assert isinstance(cls, Class)
        name = cls.java_name()
        name_obj = StringPool.java_string(cls.loader, name)

        frame.operand_stack().push_ref(name_obj)


class DesiredAssertionStatus0(NativeMethod):
    def execute(self, frame: Frame):
        frame.operand_stack().push_boolean(False)


class IsInterface(NativeMethod):
    """
    public native boolean isInterface();
    """
    def execute(self, frame: Frame):
        vars = frame.local_vars()
        this = vars.get_this()
        cls = this.extra
        assert isinstance(cls, Class)
        frame.operand_stack().push_boolean(cls.is_interface())


class IsPrimitive(NativeMethod):
    """
    public native boolean isPrimitive();
    """
    def execute(self, frame: Frame):
        vars = frame.local_vars()
        this = vars.get_this()
        cls = this.extra
        assert isinstance(cls, Class)
        frame.operand_stack().push_boolean(cls.is_primitive())


class ForName0(NativeMethod):
    """
    private static native Class<?> forName0(String name, boolean initialize,
                                            ClassLoader loader,
                                            Class<?> caller)
    """
    def execute(self, frame: Frame):
        vars = frame.local_vars()
        name = vars.get_ref(0)
        initialize = vars.get_boolean(1)
        loader = vars.get_ref(2)
        caller = vars.get_ref(3)

        py_class_name = StringPool.py_str(name)
        py_class_name = py_class_name.replace(".", "/")

        cls = frame.method().class_.loader.load_class(py_class_name)
        assert isinstance(cls, Class)
        j_cls = cls.jClass
        if initialize and not cls.initStarted:
            thread = frame.thread()
            frame.set_next_pc(thread.pc())
            class_init_logic.init_class(thread, cls)
        else:
            stack = frame.operand_stack()
            stack.push_ref(j_cls)


class GetModifiers(NativeMethod):
    """
    public native int getModifiers();
    ()I
    """
    def execute(self, frame: Frame):
        vars = frame.local_vars()
        this = vars.get_this()
        cls = this.extra
        assert isinstance(cls, Class)
        frame.operand_stack().push_int(cls.accessFlags)


class GetSuperClass(NativeMethod):
    """
    public native Class<? super T> getSuperclass();
    ()Ljava/lang/Class;
    """
    def execute(self, frame: Frame):
        vars = frame.local_vars()
        this = vars.get_this()
        clscls = this.extra
        assert isinstance(clscls, Class)
        frame.operand_stack().push_ref(clscls.superClass.jClass if clscls.superClass is not None else None)


class GetInterfaces0(NativeMethod):
    """
    private native Class<?>[] getInterfaces0();
    ()[Ljava/lang/Class;
    """
    def execute(self, frame: Frame):
        vars = frame.local_vars()
        this = vars.get_this()
        cls = this.extra
        assert isinstance(cls, Class)
        interfaces = cls.interfaces
        class_arr = _to_class_arr(cls.loader, interfaces)
        frame.operand_stack().push_ref(class_arr)


class IsArray(NativeMethod):
    """
    public native boolean isArray();
    ()Z
    """
    def execute(self, frame: Frame):
        vars = frame.local_vars()
        this = vars.get_this()
        clscls = this.extra
        assert isinstance(clscls, Class)
        frame.operand_stack().push_boolean(clscls.is_array())


class GetComponentType(NativeMethod):
    """
    public native Class<?> getComponentType();
    ()Ljava/lang/Class;
    """
    def execute(self, frame: Frame):
        vars = frame.local_vars()
        this = vars.get_this()
        cls = this.extra
        assert isinstance(cls, Class)
        frame.operand_stack().push_ref(cls.component_class().jClass)


class IsAssignableFrom(NativeMethod):
    """
    public native boolean isAssignableFrom(Class<?> cls);
    (Ljava/lang/Class;)Z
    """
    def execute(self, frame: Frame):
        vars = frame.local_vars()
        this = vars.get_this()
        cls = vars.get_ref(1)

        this_class = this.extra
        cls_class = cls.extra
        assert isinstance(this_class, Class) and isinstance(cls_class, Class)
        frame.operand_stack().push_boolean(this_class.is_assignable_from(cls_class))



def _to_class_arr(loader: ClassLoader, classes: list):
    arr_len = len(classes)

    cls_arr_cls = loader.load_class("java/lang/Class").array_class()
    cls_arr = cls_arr_cls.new_array_object(arr_len)

    if arr_len > 0:
        cls_objs = cls_arr.refs()
        for i in range(arr_len):
            cls_objs[i] = classes[i]

    return cls_arr


def _to_byte_arr(loader: ClassLoader, _bytes: bytes):
    byte_cls = loader.load_class("[B")
    return Object(byte_cls, data=list(bytes_to_int8_list(_bytes)))


field_constructor_descriptor = "(Ljava/lang/Class;Ljava/lang/String;Ljava/lang/Class;IILjava/lang/String;[B)V"


class GetDeclaredFields0(NativeMethod):
    """
    private native Field[] getDeclaredFields0(boolean publicOnly);
    (Z)[Ljava/lang/reflect/Field;
    """
    def execute(self, frame: Frame):
        vars = frame.local_vars()
        cls_obj = vars.get_this()
        public_only = vars.get_boolean(1)

        cls = cls_obj.extra
        assert isinstance(cls, Class)
        fields = cls.get_fields(public_only)
        fields_count = len(fields)

        class_loader = frame.method().class_.loader
        field_class = class_loader.load_class("java/lang/reflect/Field")
        assert isinstance(field_class, Class)
        field_arr = field_class.array_class().new_array_object()
        assert isinstance(field_arr, Object)
        stack = frame.operand_stack()
        stack.push_ref(field_arr)

        if fields_count > 0:
            thread = frame.thread()
            field_objs = field_arr.refs()
            field_constructor = field_class.get_constructor(descriptor=field_constructor_descriptor)
            for i, py_field in enumerate(fields):
                obj = field_class.new_object()
                obj.extra = py_field
                field_objs[i] = obj

                ops = OperandStack(8)
                ops.push_ref(obj) # this
                ops.push_ref(cls_obj) # declaringClass
                ops.push_ref(StringPool.java_string(class_loader, py_field.name())) # name
                ops.push_ref(py_field.type()) # type
                ops.push_int(py_field.accessFlags) # modifiers
                ops.push_int(py_field.slotId) # slot
                ops.push_ref(_get_signature_str(class_loader, py_field.signature)) # signature
                ops.push_ref(_to_byte_arr(class_loader, py_field.annotations)) # annotations

                shim_frame = new_shim_frame(thread, ops)
                thread.push_frame(shim_frame)

                method_invoke_logic.invoke_method(shim_frame, field_constructor)


method_constructor_descriptor = "(Ljava/lang/Class;" + \
	"Ljava/lang/String;" + \
	"[Ljava/lang/Class;" + \
	"Ljava/lang/Class;" + \
	"[Ljava/lang/Class;" + \
	"II" + \
	"Ljava/lang/String;" + \
	"[B[B[B)V"


class GetDeclaredMethods0(NativeMethod):
    """
    private native Field[] getDeclaredFields0(boolean publicOnly);
    (Z)[Ljava/lang/reflect/Field;
    """
    def execute(self, frame: Frame):
        vars = frame.local_vars()
        cls_obj = vars.get_this()
        public_only = vars.get_boolean(1)

        cls = cls_obj.extra
        assert isinstance(cls, Class)
        methods = cls.get_methods(public_only)
        methods_count = len(methods)

        class_loader = frame.method().class_.loader
        method_class = class_loader.load_class("java/lang/reflect/Field")
        assert isinstance(method_class, Class)
        method_arr = method_class.array_class().new_array_object()
        assert isinstance(method_arr, Object)
        stack = frame.operand_stack()
        stack.push_ref(method_arr)

        if methods_count > 0:
            thread = frame.thread()
            method_objs = method_arr.refs()
            method_constructor = method_class.get_constructor(descriptor=method_constructor_descriptor)
            for i, py_method in enumerate(methods):
                obj = method_class.new_object()
                obj.extra = py_method
                method_objs[i] = obj

                ops = OperandStack(8)
                ops.push_ref(obj) # this
                ops.push_ref(cls_obj) # declaringClass
                ops.push_ref(StringPool.java_string(class_loader, py_method.name())) # name
                ops.push_ref(py_method.return_type().JClass()) # returnType
                ops.push_ref(_to_class_arr(class_loader, py_method.exception_types())) # checkedExceptions
                ops.push_int(py_method.accessFlags) # modifiers
                ops.push_int(0) # todo: slot
                ops.push_ref(_get_signature_str(class_loader, py_method.signature)) # signature
                ops.push_ref(_to_byte_arr(class_loader, py_method.annotationData)) # annotations
                ops.push_ref(_to_byte_arr(class_loader, py_method.ParameterAnnotationData())) # parameterAnnotations
                ops.push_ref(_to_byte_arr(class_loader, py_method.AnnotationDefaultData())) # annotationDefault

                shim_frame = new_shim_frame(thread, ops)
                thread.push_frame(shim_frame)

                method_invoke_logic.invoke_method(shim_frame, method_constructor)


constructor_constructor_descriptor = \
    "(Ljava/lang/Class;" + \
    "[Ljava/lang/Class;" + \
	"[Ljava/lang/Class;" + \
	"II" + \
	"Ljava/lang/String;" + \
	"[B[B)V"

class GetDeclaredConstructors0(NativeMethod):
    """
    private native Constructor<T>[] getDeclaredConstructors0(boolean publicOnly);
    (Z)[Ljava/lang/reflect/Constructor;
    """
    def execute(self, frame: Frame):
        vars = frame.local_vars()
        cls_obj = vars.get_this()
        public_only = vars.get_boolean(1)

        cls = cls_obj.extra
        assert isinstance(cls, Class)
        constructors = cls.get_constructors(public_only)
        constructors_count = len(constructors)

        class_loader = frame.method().class_.loader
        constructor_class = class_loader.load_class("java/lang/reflect/Field")
        assert isinstance(constructor_class, Class)
        constructor_arr = constructor_class.array_class().new_array_object()
        assert isinstance(constructor_arr, Object)
        stack = frame.operand_stack()
        stack.push_ref(constructor_arr)

        if constructors_count > 0:
            thread = frame.thread()
            constructor_objs = constructor_arr.refs()
            constructor_constructor = constructor_class.get_constructor(descriptor=constructor_constructor_descriptor)
            for i, py_constructor in enumerate(constructors):
                obj = constructor_class.new_object()
                obj.extra = py_constructor
                constructor_objs[i] = obj

                ops = OperandStack(8)
                ops.push_ref(obj) # this
                ops.push_ref(cls_obj) # declaringClass
                ops.push_ref(StringPool.java_string(class_loader, py_constructor.name())) # name
                ops.push_ref(_to_class_arr(class_loader, py_constructor.parameter_types())) # parameterTypes
                ops.push_ref(_to_class_arr(class_loader, py_constructor.exception_types())) # checkedExceptions
                ops.push_int(py_constructor.accessFlags) # modifiers
                ops.push_int(0) # todo slot
                ops.push_ref(_get_signature_str(class_loader, py_constructor.signature)) # signature
                ops.push_ref(_to_byte_arr(class_loader, py_constructor.annotationData)) # annotations
                ops.push_ref(_to_byte_arr(class_loader, py_constructor.parameterAnnotationData)) # parameterAnnotations

                shim_frame = new_shim_frame(thread, ops)
                thread.push_frame(shim_frame)

                method_invoke_logic.invoke_method(shim_frame, constructor_constructor)


def _get_signature_str(loader, signature):
    if signature != "":
        return StringPool.java_string(loader, signature)
    return None


from runtime.heap.object import Object
from runtime.operand_stack import OperandStack
from utils.bits_converter import *