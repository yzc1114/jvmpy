from cmd import Cmd
from runtime.heap.class_loader import ClassLoader
from runtime.thread import Thread
from runtime.heap.object import Object
from runtime.heap.string_pool import StringPool
from instructions.base import class_init_logic
from interpreter import Interpreter
from classpath.classpath import Classpath


class JVM(object):
    def __init__(self, cmd: Cmd):
        cp: Classpath = Classpath.parse(jre_option=cmd.Xjre, cp_option=cmd.classpath)
        self.cmd: Cmd = cmd
        self.classLoader: ClassLoader = ClassLoader(cp=cp, verbose_class=cmd.verbose_class)
        self.mainThread: Thread = Thread()

    def start(self):
        self.__init_vm()
        self.__exec_main()

    def __init_vm(self):
        vm_class = self.classLoader.load_class("sun/misc/VM")
        class_init_logic.init_class(self.mainThread, vm_class)

    def __exec_main(self):
        class_name = self.cmd.className.replace(".", "/")
        main_class = self.classLoader.load_class(class_name)
        main_method = main_class.get_main_method()
        if main_method is None:
            print("没有找到main方法:" + self.cmd.className)
            return

        args_arr = self.__create_args_arr()
        frame = self.mainThread.new_frame(main_method)
        frame.local_vars().set_ref(0, args_arr)
        self.mainThread.push_frame(frame)
        Interpreter.interpret(self.mainThread, self.cmd.verbose_inst)

    def __create_args_arr(self):
        string_class = self.classLoader.load_class("java/lang/String")
        args_len = len(self.cmd.args)
        args_arr = string_class.array_class().new_array_object(args_len)
        assert isinstance(args_arr, Object)
        j_args = args_arr.refs()
        for i, arg in enumerate(self.cmd.args):
            j_args[i] = StringPool.java_string(self.classLoader, arg)
        return args_arr