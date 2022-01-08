from native.registry import NativeMethod
from runtime.frame import Frame
from runtime.heap.string_pool import StringPool
from instructions.base.method_invoke_logic import invoke_method
from runtime.heap.shim_frames import new_shim_frame
from runtime.operand_stack import OperandStack
import os
import sys
import platform
from runtime.heap.object import Object
import time

_jls = "java/lang/System"

def init():
    NativeMethod.register(_jls, "arraycopy", "(Ljava/lang/Object;ILjava/lang/Object;II)V", ArrayCopy())
    NativeMethod.register(_jls, "initProperties", "(Ljava/util/Properties;)Ljava/util/Properties;", InitProperties())
    NativeMethod.register(_jls, "setIn0", "(Ljava/io/InputStream;)V", SetIn0())
    NativeMethod.register(_jls, "setOut0", "(Ljava/io/PrintStream;)V", SetOut0())
    NativeMethod.register(_jls, "setErr0", "(Ljava/io/PrintStream;)V", SetErr0())
    NativeMethod.register(_jls, "currentTimeMillis", "()J", CurrentTimeMillis())


class ArrayCopy(NativeMethod):
    def execute(self, frame: Frame):
        vars = frame.local_vars()
        src = vars.get_ref(0)
        src_pos = vars.get_int(1)
        dest = vars.get_ref(2)
        dest_pos = vars.get_int(3)
        length = vars.get_int(4)
        assert isinstance(src, Object)
        assert isinstance(dest, Object)

        if src is None or dest is None:
            raise Exception("java.lang.NullPointerException")
        if not self.__check_array_copy(src, dest):
            raise Exception("java.lang.ArrayStoreException")

        if src_pos < 0 or dest_pos < 0 or length < 0 or \
            src_pos + length > src.array_length() or \
            dest_pos + length > dest.array_length():
            raise Exception("java.lang.IndexOutOfBoundsException")

        src.array_copy(dest, src_pos, dest_pos, length)

    @staticmethod
    def __check_array_copy(src: Object, dest: Object):
        """
        检查源数组和目标数组是否匹配
        :param src: java Object
        :param dest: java Object
        :return: bool
        """
        src_cls = src.cls
        des_cls = dest.cls
        if not src_cls.is_array() or not des_cls.is_array():
            return False
        if src_cls.component_class().is_primitive() or des_cls.component_class().is_primitive():
            return src_cls == des_cls
        return True


class InitProperties(NativeMethod):

    sys_props = {
        "java.version":         "1.8.0",
		"java.vendor":          "jvmpy",
		"java.vendor.url":      "https://github.com/yzchnb/jvmpy",
		"java.home":            "todo",
		"java.class.version":   "52.0",
		"java.class.path":      "todo",
		"java.awt.graphicsenv": "sun.awt.CGraphicsEnvironment",
		"os.name":              os.name,
		"os.arch":              platform.platform(),
		"os.version":           "",
		"file.separator":       os.sep,
		"path.separator":       os.pathsep,
		"line.separator":       os.linesep,
		"user.name":            "",
		"user.home":            "",
		"user.dir":             ".",
		"user.country":         "CN",
		"file.encoding":        "UTF-8",
		"sun.stdout.encoding":  "UTF-8",
		"sun.stderr.encoding":  "UTF-8",
    }

    def execute(self, frame: Frame):
        vars = frame.local_vars()
        props = vars.get_ref(0)

        stack = frame.operand_stack()
        stack.push_ref(props)

        set_prop_method = props.cls.get_instance_method(name="setProperty", descriptor="(Ljava/lang/String;Ljava/lang/String;)Ljava/lang/Object;")
        thread = frame.thread()
        for k, v in self.sys_props.items():
            key = StringPool.java_string(frame.method().class_.loader, k)
            value = StringPool.java_string(frame.method().class_.loader, v)
            ops = OperandStack(max_size=3)
            ops.push_ref(props)
            ops.push_ref(key)
            ops.push_ref(value)
            shim_frame = new_shim_frame(thread, ops)
            thread.push_frame(shim_frame)

            invoke_method(shim_frame, method=set_prop_method)


class SetIn0(NativeMethod):
    def execute(self, frame: Frame):
        vars = frame.local_vars()
        _in = vars.get_ref(0)

        sys_cls = frame.method().class_

        sys_cls.set_static_ref_var("in", "Ljava/io/InputStream;", _in)


class SetOut0(NativeMethod):
    def execute(self, frame: Frame):
        vars = frame.local_vars()
        out = vars.get_ref(0)

        sys_cls = frame.method().class_

        sys_cls.set_static_ref_var("out", "Ljava/io/PrintStream;", out)


class SetErr0(NativeMethod):
    def execute(self, frame: Frame):
        vars = frame.local_vars()
        err = vars.get_ref(0)

        sys_cls = frame.method().class_

        sys_cls.set_static_ref_var("err", "Ljava/io/PrintStream;", err)


class CurrentTimeMillis(NativeMethod):
    def execute(self, frame: Frame):
        frame.operand_stack().push_long(int(round(time.time() * 1000)))