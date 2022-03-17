# cython: language_level=3
# cython: cdivision=True
from libc.stdint cimport uint8_t, int32_t

from cpython.bytes cimport PyBytes_Size

from pybase16384 cimport base16384

cpdef encode(bytes data):
    cdef base16384.LENDAT *cret = base16384.encode(<const uint8_t *> data, <const int32_t> PyBytes_Size(data))

    ret = <bytes> cret.data[:cret.len]
    base16384.LENDAT_Del(&cret)
    return ret

cpdef decode(bytes data):
    cdef base16384.LENDAT *cret = base16384.decode(<const uint8_t *> data, <const int32_t> PyBytes_Size(data))

    ret = <bytes> cret.data[:cret.len]
    base16384.LENDAT_Del(&cret)
    return ret
