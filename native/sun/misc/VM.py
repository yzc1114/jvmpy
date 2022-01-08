from native.registry import NativeMethod
from runtime.frame import Frame
from runtime.heap.string_pool import StringPool
from runtime.heap.class_ import Class
from instructions.base.method_invoke_logic import invoke_method

def init():
    NativeMethod.register(class_name="sun/misc/VM", method_name="initialize", method_descriptor="()V", method=Initialize())

class Initialize(NativeMethod):
    def execute(self, frame: Frame):
        # vm_class = frame.method().class_
        # saved_props = vm_class.get_static_ref_var("savedProps", "Ljava/util/Properties;")
        # key = StringPool.java_string(vm_class.loader, "foo")
        # val = StringPool.java_string(vm_class.loader, "bar")
        #
        # frame.operand_stack().push_ref(saved_props)
        # frame.operand_stack().push_ref(key)
        # frame.operand_stack().push_ref(val)
        #
        # props_class = vm_class.loader.load_class("java/util/Properties")
        # assert isinstance(props_class, Class)
        # set_prop_method = props_class.get_instance_method(name="setProperty", descriptor="(Ljava/lang/String;Ljava/lang/String;)Ljava/lang/Object;")
        # invoke_method(frame, set_prop_method)
        class_loader = frame.method().class_.loader
        jlsys_class = class_loader.load_class("java/lang/System")
        assert isinstance(jlsys_class, Class)
        init_sys_class = jlsys_class.get_static_method(name="initializeSystemClass", descriptor="()V")
        invoke_method(frame, init_sys_class)
