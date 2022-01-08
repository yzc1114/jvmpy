import numpy as np
from runtime.heap.object import Object


class Slot(object):
    def __init__(self, num, ref):
        self.num: np.uint32 = num
        self.ref: Object = ref

    def __repr__(self):
        if self.ref is not None:
            return repr(self.ref)
        else:
            return str(self.num)

    def __deepcopy__(self, memodict):
        return Slot(self.num, self.ref)
