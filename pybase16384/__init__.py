from io import BytesIO

from pybase16384.backends import (
    _decode,
    _decode_into,
    _decode_parallel,
    _encode,
    _encode_into,
    _encode_parallel,
    decode_fd,
    decode_file,
    decode_len,
    decode_local_file,
    encode_fd,
    encode_file,
    encode_len,
    encode_local_file,
    is_64bits,
)

__version__ = "0.3.4"


def encode(data: bytes) -> bytes:
    inp = BytesIO(data)
    out = BytesIO()
    encode_file(inp, out, False, len(data) // 7)
    return out.getvalue()


def decode(data: bytes) -> bytes:
    inp = BytesIO(data)
    out = BytesIO()
    decode_file(inp, out, len(data) // 8)
    return out.getvalue()


def encode_from_string(data: str, write_head: bool = False) -> bytes:
    bt = data.encode()
    inp = BytesIO(bt)
    out = BytesIO()
    encode_file(inp, out, write_head, len(bt) // 7)
    return out.getvalue()


def encode_to_string(data: bytes) -> str:
    inp = BytesIO(data)
    out = BytesIO()
    encode_file(inp, out, False, len(data) // 7)
    return out.getvalue().decode("utf-16-be")


def encode_string(data: str) -> str:
    data = data.encode()
    inp = BytesIO(data)
    out = BytesIO()
    encode_file(inp, out, False, len(data) // 7)
    return out.getvalue().decode("utf-16-be")


def decode_from_bytes(data: bytes) -> str:
    inp = BytesIO(data)
    out = BytesIO()
    decode_file(inp, out, len(data) // 8)
    return out.getvalue().decode()


def decode_from_string(data: str) -> bytes:
    bt = data.encode("utf-16-be")
    inp = BytesIO(bt)
    out = BytesIO()
    decode_file(inp, out, len(bt) // 8)
    return out.getvalue()


def decode_string(data: str) -> str:
    bt = data.encode("utf-16-be")
    inp = BytesIO(bt)
    out = BytesIO()
    decode_file(inp, out, len(bt) // 8)
    return out.getvalue().decode()
