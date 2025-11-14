import os
import platform
from io import BytesIO

impl = platform.python_implementation()


def _should_use_cffi() -> bool:
    ev = os.getenv("B14_USE_CFFI")
    if ev is not None:
        return True
    if impl == "CPython":
        return False
    else:
        return True


if not _should_use_cffi():
    from pybase16384.backends.cython import (
        DECBUFSZ,
        ENCBUFSZ,
        FLAG_DO_SUM_CHECK_FORCELY,
        FLAG_NOHEADER,
        FLAG_SUM_CHECK_ON_REMAIN,
        _decode,
        _decode_into,
        _decode_into_safe,
        _decode_safe,
        _encode,
        _encode_into,
        _encode_into_safe,
        _encode_safe,
        decode_fd,
        decode_fd_detailed,
        decode_file,
        decode_file_safe,
        decode_len,
        decode_local_file,
        decode_local_file_detailed,
        decode_stream_detailed,
        encode_fd,
        encode_fd_detailed,
        encode_file,
        encode_file_safe,
        encode_len,
        encode_local_file,
        encode_local_file_detailed,
        encode_stream_detailed,
        is_64bits,
    )
else:
    from pybase16384.backends.cffi import (
        DECBUFSZ,
        ENCBUFSZ,
        FLAG_DO_SUM_CHECK_FORCELY,
        FLAG_NOHEADER,
        FLAG_SUM_CHECK_ON_REMAIN,
        _decode,
        _decode_into,
        _decode_into_safe,
        _decode_safe,
        _encode,
        _encode_into,
        _encode_into_safe,
        _encode_safe,
        decode_fd,
        decode_fd_detailed,
        decode_file,
        decode_file_safe,
        decode_len,
        decode_local_file,
        decode_local_file_detailed,
        decode_stream_detailed,
        encode_fd,
        encode_fd_detailed,
        encode_file,
        encode_file_safe,
        encode_len,
        encode_local_file,
        encode_local_file_detailed,
        encode_stream_detailed,
        is_64bits,
    )

__version__ = "0.3.9"


def encode(data: bytes) -> bytes:
    inp = BytesIO(data)
    out = BytesIO()
    encode_file(inp, out, False, len(data) // 7)
    return out.getvalue()


def encode_safe(data: bytes) -> bytes:
    inp = BytesIO(data)
    out = BytesIO()
    encode_file_safe(inp, out, False, len(data) // 7)
    return out.getvalue()


def decode(data: bytes) -> bytes:
    inp = BytesIO(data)
    out = BytesIO()
    decode_file(inp, out, len(data) // 8)
    return out.getvalue()


def decode_safe(data: bytes) -> bytes:
    inp = BytesIO(data)
    out = BytesIO()
    decode_file_safe(inp, out, len(data) // 8)
    return out.getvalue()


def encode_from_string(data: str, write_head: bool = False) -> bytes:
    bt = data.encode()
    inp = BytesIO(bt)
    out = BytesIO()
    encode_file(inp, out, write_head, len(bt) // 7)
    return out.getvalue()


def encode_from_string_safe(data: str, write_head: bool = False) -> bytes:
    bt = data.encode()
    inp = BytesIO(bt)
    out = BytesIO()
    encode_file_safe(inp, out, write_head, len(bt) // 7)
    return out.getvalue()


def encode_to_string(data: bytes) -> str:
    inp = BytesIO(data)
    out = BytesIO()
    encode_file(inp, out, False, len(data) // 7)
    return out.getvalue().decode("utf-16-be")


def encode_to_string_safe(data: bytes) -> str:
    inp = BytesIO(data)
    out = BytesIO()
    encode_file_safe(inp, out, False, len(data) // 7)
    return out.getvalue().decode("utf-16-be")


def encode_string(data: str) -> str:
    data = data.encode()
    inp = BytesIO(data)
    out = BytesIO()
    encode_file(inp, out, False, len(data) // 7)
    return out.getvalue().decode("utf-16-be")


def encode_string_safe(data: str) -> str:
    data = data.encode()
    inp = BytesIO(data)
    out = BytesIO()
    encode_file_safe(inp, out, False, len(data) // 7)
    return out.getvalue().decode("utf-16-be")


def decode_from_bytes(data: bytes) -> str:
    inp = BytesIO(data)
    out = BytesIO()
    decode_file(inp, out, len(data) // 8)
    return out.getvalue().decode()


def decode_from_bytes_safe(data: bytes) -> str:
    inp = BytesIO(data)
    out = BytesIO()
    decode_file_safe(inp, out, len(data) // 8)
    return out.getvalue().decode()


def decode_from_string(data: str) -> bytes:
    bt = data.encode("utf-16-be")
    inp = BytesIO(bt)
    out = BytesIO()
    decode_file(inp, out, len(bt) // 8)
    return out.getvalue()


def decode_from_string_safe(data: str) -> bytes:
    bt = data.encode("utf-16-be")
    inp = BytesIO(bt)
    out = BytesIO()
    decode_file_safe(inp, out, len(bt) // 8)
    return out.getvalue()


def decode_string(data: str) -> str:
    bt = data.encode("utf-16-be")
    inp = BytesIO(bt)
    out = BytesIO()
    decode_file(inp, out, len(bt) // 8)
    return out.getvalue().decode()


def decode_string_safe(data: str) -> str:
    bt = data.encode("utf-16-be")
    inp = BytesIO(bt)
    out = BytesIO()
    decode_file_safe(inp, out, len(bt) // 8)
    return out.getvalue().decode()
