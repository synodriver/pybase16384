# cython: language_level=3
# cython: cdivision=True
from libc.stdint cimport uint8_t, int32_t
cdef extern from "base14.h" nogil:
    ctypedef struct LENDAT:
        uint8_t * data
        int32_t len

    LENDAT * encode(const uint8_t * data, const int32_t len)
    LENDAT * decode(const uint8_t * data, const int32_t len)

cdef extern from * nogil:
    """
void LENDAT_Del(LENDAT** self)
{
    if(*self!=NULL)
    {
         free((*self)->data);
        (*self)->data = NULL;
        free(*self);
        *self = NULL;
    }
}

#define be16toh(x) __builtin_bswap16(x)
#define be32toh(x) __builtin_bswap32(x)
#define be64toh(x) __builtin_bswap64(x)
#define htobe16(x) __builtin_bswap16(x)
#define htobe32(x) __builtin_bswap32(x)
#define htobe64(x) __builtin_bswap64(x)
    """
    void LENDAT_Del(LENDAT** self)