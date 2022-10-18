"""
Copyright (c) 2008-2021 synodriver <synodriver@gmail.com>
"""
from pathlib import Path
from typing import IO

from pybase16384.backends.cffi._core_cffi import ffi, lib

__version__ = "0.1.0"

encode_len = lib.base16384_encode_len
decode_len = lib.base16384_decode_len


# -----------------low level api------------------------------
def _encode(data: bytes) -> bytes:
    length = len(data)
    output_size = encode_len(length) + 16
    output_buf = ffi.new(f"char[{output_size}]")
    if output_buf == ffi.NULL:
        raise MemoryError
    count = lib.base16384_encode(ffi.from_buffer(data), length, output_buf, output_size)
    return ffi.unpack(output_buf, count)


def _encode_into(data: bytes, out: bytearray) -> int:
    return lib.base16384_encode(
        ffi.from_buffer(data), len(data), ffi.from_buffer(out), len(out)
    )


def _decode(data: bytes) -> bytes:
    length = len(data)
    output_size = decode_len(length, 0) + 16
    output_buf = ffi.new(f"char[{output_size}]")
    if output_buf == ffi.NULL:
        raise MemoryError
    count = lib.base16384_decode(ffi.from_buffer(data), length, output_buf, output_size)
    return ffi.unpack(output_buf, count)


def _decode_into(data: bytes, out: bytearray) -> int:
    return lib.base16384_decode(
        ffi.from_buffer(data), len(data), ffi.from_buffer(out), len(out)
    )


def is_64bits() -> bool:
    return bool(lib.pybase16384_64bits())


# ----------------------------
def _check_file(file) -> bool:
    if hasattr(file, "read") and hasattr(file, "write") and hasattr(file, "seek"):
        return True
    return False


def encode_file(input: IO, output: IO, write_head: bool = False, buf_rate: int = 10):
    if not _check_file(input):
        raise TypeError(
            "input except a file-like object, got %s" % type(input).__name__
        )
    if not _check_file(output):
        raise TypeError(
            "output except a file-like object, got %s" % type(input).__name__
        )
    if buf_rate <= 0:
        buf_rate = 1
    if write_head:
        output.write(b"\xfe\xff")

    current_buf_len: int = buf_rate * 7  # 一次读取这么多字节
    output_size: int = encode_len(current_buf_len) + 16  # 因为encode_len不是单调的 这16备用
    output_buf = ffi.new(f"char[{output_size}]")
    if output_buf == ffi.NULL:
        raise MemoryError
    first_check: int = 1  # 检查一次就行了 怎么可能出现第一次读出来是bytes 以后又变卦了的对象呢 不会吧不会吧
    while True:
        chunk = input.read(current_buf_len)
        if first_check:
            first_check = 0
            if not isinstance(chunk, bytes):
                raise TypeError(
                    f"input must be a file-like rb object, got {type(input).__name__}"
                )
        size = len(chunk)
        if size < current_buf_len:  # 数据不够了 要减小一次读取的量
            if buf_rate > 1:  # 重新设置一次读取的大小 重新设置流的位置 当然要是已经是一次读取7字节了 那就不能再变小了 直接encode吧
                buf_rate = buf_rate // 2
                current_buf_len = buf_rate * 7
                input.seek(-size, 1)
                continue

        count = lib.base16384_encode(
            ffi.from_buffer(chunk), size, output_buf, output_size
        )
        output.write(ffi.unpack(output_buf, count))
        if size < 7:
            break


def decode_file(input: IO, output: IO, buf_rate: int = 10):
    if not _check_file(input):
        raise TypeError(
            "input except a file-like object, got %s" % type(input).__name__
        )
    if not _check_file(output):
        raise TypeError(
            "output except a file-like object, got %s" % type(output).__name__
        )
    if buf_rate <= 0:
        buf_rate = 1

    chunk = input.read(1)  # type: bytes
    if not isinstance(chunk, bytes):
        raise TypeError(
            f"input must be a file-like rb object, got {type(input).__name__}"
        )
    if chunk == b"\xfe":  # 去头
        input.read(1)
    else:
        input.seek(0, 0)  # 没有头 回到开头

    current_buf_len: int = buf_rate * 8
    output_size: int = decode_len(current_buf_len, 0) + 16
    output_buf = ffi.new(f"char[{output_size}]")
    if output_buf == ffi.NULL:
        raise MemoryError
    while True:
        chunk = input.read(current_buf_len)  # 8的倍数
        size = len(chunk)
        if size == 0:
            break
        if size < current_buf_len:  # 长度不够了
            if buf_rate > 1:  # 还能继续变小
                buf_rate = buf_rate // 2  # 重新设置一次读取的大小
                current_buf_len = buf_rate * 8
                input.seek(-size, 1)
                continue
        tmp = input.read(2)  # type: bytes
        if len(tmp) == 2:
            if tmp[0] == 61:  # = stream完了   一次解码8n+2个字节
                chunk += tmp
                size += 2
            else:
                input.seek(-2, 1)

        count = lib.base16384_decode(
            ffi.from_buffer(chunk), size, output_buf, output_size
        )
        output.write(ffi.unpack(output_buf, count))


def ensure_bytes(inp) -> bytes:
    if isinstance(inp, str):
        return inp.encode()
    elif isinstance(inp, bytes):
        return inp
    elif isinstance(inp, Path):
        return str(inp).encode()
    else:
        return bytes(inp)


def err_to_str(ret) -> str:
    if ret == lib.base16384_err_get_file_size:
        return "base16384_err_get_file_size"
    elif ret == lib.base16384_err_fopen_output_file:
        return "base16384_err_fopen_output_file"
    elif ret == lib.base16384_err_fopen_input_file:
        return "base16384_err_fopen_input_file"
    elif ret == lib.base16384_err_write_file:
        return "base16384_err_write_file"
    elif ret == lib.base16384_err_open_input_file:
        return "base16384_err_open_input_file"
    elif ret == lib.base16384_err_map_input_file:
        return "base16384_err_map_input_file"


def encode_local_file(inp, out) -> None:
    inp_name: bytes = ensure_bytes(inp)
    out_name: bytes = ensure_bytes(out)
    encbuf = ffi.new(f"char[{lib.get_encsize()}]")
    decbuf = ffi.new(f"char[{lib.get_decsize()}]")
    ret = lib.base16384_encode_file(
        ffi.from_buffer(inp_name), ffi.from_buffer(out_name), encbuf, decbuf
    )
    if ret != lib.base16384_err_ok:
        raise ValueError(err_to_str(ret))


def decode_local_file(inp, out) -> None:
    inp_name: bytes = ensure_bytes(inp)
    out_name: bytes = ensure_bytes(out)
    encbuf = ffi.new(f"char[{lib.get_encsize()}]")
    decbuf = ffi.new(f"char[{lib.get_decsize()}]")
    ret = lib.base16384_decode_file(
        ffi.from_buffer(inp_name), ffi.from_buffer(out_name), encbuf, decbuf
    )
    if ret != lib.base16384_err_ok:
        raise ValueError(err_to_str(ret))


def encode_fd(inp: int, out: int) -> None:
    encbuf = ffi.new(f"char[{lib.get_encsize()}]")
    decbuf = ffi.new(f"char[{lib.get_decsize()}]")
    ret = lib.base16384_encode_fd(inp, out, encbuf, decbuf)
    if ret != lib.base16384_err_ok:
        raise ValueError(err_to_str(ret))


def decode_fd(inp: int, out: int) -> None:
    encbuf = ffi.new(f"char[{lib.get_encsize()}]")
    decbuf = ffi.new(f"char[{lib.get_decsize()}]")
    ret = lib.base16384_decode_fd(inp, out, encbuf, decbuf)
    if ret != lib.base16384_err_ok:
        raise ValueError(err_to_str(ret))
