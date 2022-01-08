from runtime.frame import Frame


def branch(frame: Frame, offset: int):
    frame.set_next_pc(frame.thread().pc() + offset)
