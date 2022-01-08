import numpy as np
from ..class_reader import ClassReader
from ..attribute_info import AttributeInfo


class ConstantValueAttribute(AttributeInfo):

    def __init__(self):
        self.constantValueIndex: np.uint16 = None

    def read_info(self, reader: ClassReader):
        self.constantValueIndex = reader.read_uint16()

    def constant_value_index(self) -> np.uint16:
        return self.constantValueIndex
