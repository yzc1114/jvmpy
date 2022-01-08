import numpy as np
from ..class_reader import ClassReader
from ..attribute_info import AttributeInfo


class MarkerAttribute(AttributeInfo):
    def read_info(self, reader: ClassReader):
        pass


class DeprecatedAttribute(MarkerAttribute):
    pass


class SyntheticAttribute(MarkerAttribute):
    pass
