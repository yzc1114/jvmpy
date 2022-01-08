import struct
import numpy as np


def bytes_to_uint8(bs: bytes) -> np.uint8:
    assert len(bs) == 1
    return np.uint8(int.from_bytes(bytes=bs, byteorder='big', signed=False))


def bytes_to_int8(bs: bytes) -> np.int8:
    assert len(bs) == 1
    return np.int8(int.from_bytes(bytes=bs, byteorder='big', signed=True))


def bytes_to_uint16(bs: bytes) -> np.uint16:
    assert len(bs) == 2
    return np.uint16(int.from_bytes(bytes=bs, byteorder='big', signed=False))


def bytes_to_int16(bs: bytes) -> np.int16:
    assert len(bs) == 2
    return np.int16(int.from_bytes(bytes=bs, byteorder='big', signed=True))


def bytes_to_uint32(bs: bytes) -> np.uint32:
    assert len(bs) == 4
    return np.uint32(int.from_bytes(bytes=bs, byteorder='big', signed=False))


def bytes_to_int32(bs: bytes) -> np.int32:
    assert len(bs) == 4
    return np.int32(int.from_bytes(bytes=bs, byteorder='big', signed=True))


def bytes_to_uint64(bs: bytes) -> np.uint64:
    assert len(bs) == 8
    return np.uint64(int.from_bytes(bytes=bs, byteorder='big', signed=False))


def bytes_to_int64(bs: bytes) -> np.int64:
    assert len(bs) == 8
    return np.int64(int.from_bytes(bytes=bs, byteorder='big', signed=True))


def bytes_to_float32(bs: bytes) -> np.float32:
    assert len(bs) == 4
    return np.float32(struct.unpack('>f', struct.pack('4B', *bs))[0])


def bytes_to_float64(bs: bytes) -> np.float64:
    assert len(bs) == 8
    return np.float64(struct.unpack('>d', struct.pack('8B', *bs))[0])


def uint8_to_bytes(val: np.uint8) -> bytes:
    return int.to_bytes(int(val), 1, byteorder='big', signed=False)


def int8_to_bytes(val: np.int8) -> bytes:
    return int.to_bytes(int(val), 1, byteorder='big', signed=True)


def uint16_to_bytes(val: np.uint16) -> bytes:
    return int.to_bytes(int(val), 2, byteorder='big', signed=False)


def int16_to_bytes(val: np.int16) -> bytes:
    return int.to_bytes(int(val), 2, byteorder='big', signed=True)


def uint32_to_bytes(val: np.uint32) -> bytes:
    return int.to_bytes(int(val), 4, byteorder='big', signed=False)


def int32_to_bytes(val: np.int32) -> bytes:
    return int.to_bytes(int(val), 4, byteorder='big', signed=True)


def uint64_to_bytes(val: np.uint64) -> bytes:
    return int.to_bytes(int(val), 8, byteorder='big', signed=False)


def int64_to_bytes(val: np.int64) -> bytes:
    return int.to_bytes(int(val), 8, byteorder='big', signed=True)


def float32_to_bytes(val: np.float32) -> bytes:
    return struct.pack('>f', val)


def float64_to_bytes(val: np.float64) -> bytes:
    return struct.pack('>d', val)

def bytes_to_uint16_list(bs: bytes) -> [np.uint16]:
    assert len(bs) % 2 == 0
    i = 0
    l: [np.uint16] = [np.uint16() for _ in range(int(len(bs) / 2))]
    while i < len(bs):
        b1 = bs[i]
        b2 = bs[i+1]
        l[int(i / 2)] = bytes_to_uint16(bytes([b1, b2]))
        i += 2
    return l

def bytes_to_int8_list(bs: bytes) -> [np.uint16]:
    i = 0
    l: [np.int8] = [np.uint8 for _ in range(len(bs))]
    while i < len(bs):
        b1 = bs[i]
        l[i] = bytes_to_int8(bytes(b1))
        i += 1
    return l

def uint16_list_to_bytes(l: [np.uint16]) -> bytes:
    bs = bytes()
    for index, uint16 in enumerate(l):
        t = uint16_to_bytes(uint16)
        bs += t
    return bs


if __name__ == '__main__':
    s = "Hello, World"
    bs = bytes(s, encoding="utf-16")
    print("first bs", bs)
    # s2 = bs.decode(encoding="utf-16")
    # print(s2)
    uint16_list = bytes_to_uint16_list(bs)
    print(uint16_list)
    bs2 = uint16_list_to_bytes(uint16_list)
    print("second bs", bs2)
    print(bs2.decode(encoding="utf-16"))
