import numpy as np
from ..class_reader import ClassReader
from ..attribute_info import AttributeInfo


class UnparsedAttribute(AttributeInfo):
    def __init__(self, name: str, length: int):
        self.name: str = name
        self.length: int = length
        self.info: bytes = None

    def read_info(self, reader: ClassReader):
        self.info = reader.read_bytes(self.length)

    def info(self) -> bytes:
        return self.info
