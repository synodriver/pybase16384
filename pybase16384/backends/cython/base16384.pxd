# cython: language_level=3
# cython: cdivision=True
from libc.stdint cimport int32_t


cdef extern from "base16384.h" nogil:
    # encode_len calc min buf size to fill encode result
    int b14_encode_len "encode_len" (int dlen)
# decode_len calc min buf size to fill decode result
    int b14_decode_len "decode_len" (int dlen, int offset)

# encode data and write result into buf
    int b14_encode "encode" (const char* data, int dlen, char* buf, int blen)
# decode data and write result into buf
    int b14_decode "decode" (const char* data, int dlen, char* buf, int blen)

cdef extern from * nogil:
    """
#ifdef CPUBIT32
#define pybase16384_64bits() 0
#else
#define pybase16384_64bits() 1
#endif
    """
    int32_t pybase16384_64bits()
