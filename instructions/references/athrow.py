from ..instruction import NoOperandsInstruction
from runtime.frame import Frame


class ATHROW(NoOperandsInstruction):
    def execute(self, frame: Frame):
        ex = frame.operand_stack().pop_ref()
        if ex is None:
            raise Exception("java.lang.NullPointerException")
        thread = frame.thread()

        if not self.__find_and_goto_exception_handler(thread, ex):
            self.__handle_uncaught_exception(thread, ex)

    def __find_and_goto_exception_handler(self, thread, ex):
        """
        遍历虚拟机栈，寻找可以处理异常的代码块
        :param thread:
        :param ex:
        :return:
        """
        while True:
            frame = thread.current_frame()
            pc = frame.next_pc() - 1

            handlerPc = frame.method().find_exception_handler(ex.cls, pc)
            if handlerPc > 0:
                stack = frame.operand_stack()
                stack.clear()
                stack.push_ref(ex)
                frame.set_next_pc(handlerPc)
                return True

            # 将栈帧pop出来，去上一层函数调用中寻找处理代码
            thread.pop_frame()
            if thread.is_stack_empty():
                break
        return False

    def __handle_uncaught_exception(self, thread, ex):
        """
        没有找到处理异常的代码，则打印出虚拟机栈信息
        :param thread:
        :param ex:
        :return:
        """
        thread.clear_stack()

        j_msg = ex.get_ref_var("detailMessage", "Ljava/lang/String")
        pystr = StringPool.py_str(j_msg)
        print(ex.cls.java_name() + ":" + pystr)

        stes = ex.extra
        for ste in stes:
            print(ste.to_string())


from runtime.heap.string_pool import StringPool
