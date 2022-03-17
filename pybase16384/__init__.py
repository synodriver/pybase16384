from io import BytesIO
from ._core import *

__version__ = "0.1.0rc1"


def encode_from_string(data: str, write_head: bool = False) -> bytes:
    inp = BytesIO(data.encode())
    out = BytesIO()
    encode_file(inp, out, write_head)
    return out.getvalue()


def decode_from_bytes(data: bytes) -> str:
    inp = BytesIO(data)
    out = BytesIO()
    decode_file(inp, out)
    return out.getvalue().decode()
