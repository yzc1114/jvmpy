from runtime.thread import Thread
from runtime.heap.class_ import Class


def init_class(thread: Thread, cls: Class):
    cls.start_init()
    _schedule_cl_init(thread, cls)
    _init_super_class(thread, cls)

def _schedule_cl_init(thread: Thread, cls: Class):
    clinit = cls.get_clinit_method()
    if clinit is not None:
        new_frame = thread.new_frame(clinit)
        thread.push_frame(new_frame)

def _init_super_class(thread: Thread, cls: Class):
    if not cls.is_interface():
        super_class = cls.superClass
        if super_class is not None and not super_class.initStarted:
            init_class(thread, super_class)