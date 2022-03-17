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
        PyMem_Free((*self)->data);
        (*self)->data = NULL;
        PyMem_Free(*self);
        *self = NULL;
    }
}
    """
    void LENDAT_Del(LENDAT** self)
