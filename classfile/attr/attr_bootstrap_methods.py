import numpy as np
from ..class_reader import ClassReader
from ..attribute_info import AttributeInfo


class BootstrapMethodsAttribute(AttributeInfo):

    def __init__(self):
        self.bootstrapMethods: [BootstrapMethod] = None

    def read_info(self, reader: ClassReader):
        num_boot_strap_methods = reader.read_uint16()
        self.bootstrapMethods = []
        for i in range(num_boot_strap_methods):
            boot_strap_method = BootstrapMethod()
            boot_strap_method.bootstrapMethodRef = reader.read_uint16()
            boot_strap_method.bootstrapArguments = reader.read_uint16s()
            self.bootstrapMethods.append(boot_strap_method)


class BootstrapMethod(object):
    def __init__(self):
        self.bootstrapMethodRef: np.uint16 = None
        self.bootstrapArguments: [np.uint16] = None
