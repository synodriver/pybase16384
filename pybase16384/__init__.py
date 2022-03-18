from io import BytesIO
from pybase16384._core import _encode, _decode, encode_file, decode_file

__version__ = "0.1.0"


def encode(data: bytes) -> bytes:
    inp = BytesIO(data)
    out = BytesIO()
    encode_file(inp, out, False, len(data) // 7)
    return out.getvalue()


def decode(data: bytes) -> bytes:
    inp = BytesIO(data)
    out = BytesIO()
    decode_file(inp, out, False, len(data) // 8)
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
