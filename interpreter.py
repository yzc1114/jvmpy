from instructions.instruction import Instruction
from instructions.bytecode_reader import ByteCodeReader
from instructions.inst_factory import InstructionFactory
from runtime.frame import Frame
from runtime.thread import Thread


class Interpreter(object):

    @classmethod
    def interpret(cls, thread: Thread, log_inst: bool):
        try:
            cls.__loop(thread, log_inst)
        except Exception as e:
            print("TraceBack:")
            cls.__log_frames(thread)
            raise e

    @classmethod
    def __loop(cls, thread, log_inst: bool):
        reader = ByteCodeReader()

        while True:
            frame = thread.current_frame()
            pc = frame.next_pc()
            thread.set_pc(pc)

            reader.reset(frame.method().code, pc)
            opcode = reader.read_uint8()
            inst = InstructionFactory.new_instruction(opcode=opcode)
            inst.fetch_operands(reader=reader)
            frame.set_next_pc(reader.pc())

            if log_inst:
                cls.__log_instruction(frame, inst)

            inst.execute(frame)
            if thread.is_stack_empty():
                break

    @classmethod
    def __create_args_array(cls, loader, args):
        string_class = loader.load_class("java/lang/String")
        assert isinstance(string_class, Class)
        args_arr = string_class.array_class().new_array_object(len(args))
        j_args = args_arr.refs()
        for i, arg in enumerate(args):
            j_args[i] = StringPool.java_string(loader, arg)
        return args_arr


    @classmethod
    def __log_frames(cls, thread: Thread):
        while not thread.is_stack_empty():
            frame = thread.pop_frame()
            method = frame.method()
            class_name = method.class_.name
            print(" >> pc: {} {}.{} {}".format(frame.next_pc(), class_name, method.name(), method.descriptor()))

    @classmethod
    def __log_instruction(cls, frame: Frame, inst: Instruction):
        m = frame.method()
        class_name = m.class_.name
        method_name = m.name()
        pc = frame.thread().pc()
        print("{}.{} #pc: {} {}".format(class_name, method_name, pc, inst.__class__.__name__))


from runtime.heap.class_ import Class
from runtime.heap.string_pool import StringPool