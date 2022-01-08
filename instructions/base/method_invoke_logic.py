from runtime.frame import Frame
from runtime.heap.method import Method


def invoke_method(invoker_frame: Frame, method: Method):
    thread = invoker_frame.thread()
    new_frame = thread.new_frame(method)
    thread.push_frame(new_frame)

    arg_slot_count = int(method.arg_slot_count)
    if arg_slot_count > 0:
        for i in reversed(range(arg_slot_count)):
            slot = invoker_frame.operand_stack().pop_slot()
            new_frame.local_vars().set_slot(i, slot)

    # if method.is_native():
    #     if method.name() == "registerNatives":
    #         thread.pop_frame()
    # else:
    #     raise Exception("native method: {}.{}{}".format(method.class_.name, method.name(), method.descriptor()))