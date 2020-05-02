import struct

def encode_msg_size(size: int) -> bytes:
    return struct.pack(">L", size)

def decode_msg_size(size_bytes: bytes) -> int:
    return struct.unpack(">L", size_bytes)[0]

def create_msg(content: bytes) -> bytes:
    size = len(content)
    return encode_msg_size(size) + content