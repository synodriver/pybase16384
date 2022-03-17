# cython: language_level=3
# cython: cdivision=True
from libc.stdint cimport uint8_t, int32_t

from cpython.object cimport PyObject_HasAttrString
from cpython.bytes cimport PyBytes_Check, PyBytes_AsString, PyBytes_Size

from pybase16384 cimport base16384

cdef uint8_t PyFile_Check(object file):
    if PyObject_HasAttrString(file, "read") and PyObject_HasAttrString(file, "write") and PyObject_HasAttrString(file,
                                                                                                                 "seek"):
        return 1
    return 0

cpdef bytes encode(bytes data):
    cdef base16384.LENDAT *cret = base16384.encode(<const uint8_t *> data, <const int32_t> PyBytes_Size(data))
    ret = <bytes> cret.data[:cret.len]
    base16384.LENDAT_Del(&cret)
    return ret

cpdef bytes decode(bytes data):
    cdef base16384.LENDAT *cret = base16384.decode(<const uint8_t *> data, <const int32_t> PyBytes_Size(data))
    ret = <bytes> cret.data[:cret.len]
    base16384.LENDAT_Del(&cret)
    return ret

cpdef void encode_file(object input,
                       object output,
                       bint write_head = False) with gil:
    if not PyFile_Check(input):
        raise TypeError("input except a file-like object, got %s" % type(input).__name__)
    if not PyFile_Check(output):
        raise TypeError("output except a file-like object, got %s" % type(output).__name__)

    if write_head:
        output.write(b'\xfe\xff')
    while True:
        chunk = input.read(7)
        if not PyBytes_Check(chunk):
            raise TypeError(f"input must be a file-like rb object, got {type(input).__name__}")
        ot = encode(chunk)  # type: bytes
        output.write(ot)
        if PyBytes_Size(chunk) < 7:
            break

cpdef void decode_file(object input,
                       object output) with gil:
    if not PyFile_Check(input):
        raise TypeError("input except a file-like object, got %s" % type(input).__name__)
    if not PyFile_Check(output):
        raise TypeError("output except a file-like object, got %s" % type(output).__name__)

    chunk = input.read(1)  # type: bytes
    if not PyBytes_Check(chunk):
        raise TypeError(f"input must be a file-like rb object, got {type(input).__name__}")
    if chunk == b"\xfe":
        input.read(1)
    else:
        input.seek(0, 0)  # 回到开头
    while True:
        chunk = input.read(2)  # type: bytes
        if chunk:
            if chunk[0] == 61:  # = stream完了
                output.write(chunk)
                break
            else:
                input.seek(-2, 1)
        else:
            break
        chunk = input.read(8)
        ot = decode(chunk)  # type: bytes
        output.write(ot)
        if PyBytes_Size(chunk) < 8:
            break
