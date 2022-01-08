import numpy as np


class ClassReader(object):

    def __init__(self, data: bytes):
        self.data = data

    def read_uint8(self) -> np.uint8:
        val = np.uint8(self.data[0])
        self.data = self.data[1:]
        return val

    def read_uint16(self) -> np.uint16:
        bs = self.data[:2]
        self.data = self.data[2:]
        return np.uint16(int.from_bytes(bs, byteorder='big', signed=False))

    def read_uint32(self) -> np.uint32:
        bs = self.data[:4]
        self.data = self.data[4:]
        return np.uint32(int.from_bytes(bs, byteorder='big', signed=False))

    def read_uint64(self) -> np.uint64:
        bs = self.data[:8]
        self.data = self.data[8:]
        return np.uint64(int.from_bytes(bs, byteorder='big', signed=False))

    def read_uint16s(self) -> [np.uint16]:
        n = self.read_uint16()
        res: [np.uint16] = []
        for i in range(n):
            res.append(self.read_uint16())
        return res

    def read_bytes(self, n) -> bytes:
        res = self.data[:n]
        self.data = self.data[n:]
        return bytes(res)
