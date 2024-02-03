import os
import platform

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
else:
    from pybase16384.backends.cffi import (
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
