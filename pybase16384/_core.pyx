# cython: language_level=3
# cython: cdivision=True
from libc.stdint cimport uint8_t, int32_t

from cpython.object cimport PyObject_HasAttrString
from cpython.bytes cimport PyBytes_Check, PyBytes_AsString, PyBytes_Size
from cpython.mem cimport PyMem_Malloc, PyMem_Free
from cython.parallel cimport prange
from openmp cimport omp_get_num_procs

from pybase16384 cimport base16384

cdef inline uint8_t PyFile_Check(object file):
    if PyObject_HasAttrString(file, "read") and PyObject_HasAttrString(file, "write") and PyObject_HasAttrString(file,
                                                                                                                 "seek"):
        return 1
    return 0

cpdef inline int encode_len(int dlen):
    return base16384.encode_len(dlen)

cpdef inline int decode_len(int dlen, int offset):
    return base16384.decode_len(dlen, offset)

cpdef inline bytes _encode(const uint8_t[:] data):
    cdef size_t length = data.shape[0]
    cdef size_t output_size = <size_t>base16384.encode_len(<int>length) + 16
    cdef char *output_buf = <char*>PyMem_Malloc(output_size)
    if output_buf == NULL:
        raise MemoryError
    cdef int count = base16384.encode(<const char*> &data[0],
                                      <int>length,
                                      output_buf,
                                      <int>output_size) # encode 整数倍的那个
    ret = <bytes>output_buf[:count]
    PyMem_Free(output_buf)
    return ret

cpdef inline bytes _decode(const uint8_t[::1] data):
    cdef size_t length = data.shape[0]
    cdef size_t output_size = <size_t>base16384.decode_len(<int>length, 0) + 16
    cdef char *output_buf = <char *> PyMem_Malloc(output_size)
    if output_buf == NULL:
        raise MemoryError
    cdef int count = base16384.decode(<const char *> &data[0],
                                      <int> length,
                                      output_buf,
                                      <int> output_size)  # decode
    ret = <bytes> output_buf[:count]
    PyMem_Free(output_buf)
    return ret

cpdef inline int _encode_into(const uint8_t[::1] data, uint8_t[::1] dest):
    cdef size_t input_size = data.shape[0]
    cdef size_t output_size = <size_t> base16384.encode_len(<int> input_size)
    cdef size_t output_buf_size = dest.shape[0]
    if output_buf_size < output_size:
        raise ValueError("Buffer is too small to hold result")
    return base16384.encode(<const char *> &data[0],
                                      <int> input_size,
                                      <char *> &dest[0],
                                      <int> output_buf_size)

cpdef inline int _decode_into(const uint8_t[::1] data, uint8_t[::1] dest):
    cdef size_t input_size = data.shape[0]
    cdef size_t output_size = <size_t> base16384.decode_len(<int> input_size, 0)
    cdef size_t output_buf_size = dest.shape[0]
    if output_buf_size < output_size:
        raise ValueError("Buffer is too small to hold result")
    return base16384.decode(<const char *> &data[0],
                                      <int> input_size,
                                      <char *> &dest[0],
                                      <int> output_buf_size)

cpdef inline bytes _encode_parallel(const uint8_t[::1] data):
    cdef int threads = omp_get_num_procs()
    cdef size_t length = data.shape[0]
    cdef size_t chunk_size = length / threads / 7 * 7 # 有几个线程分成几块 还要保证是7的倍数
    cdef size_t output_chunk_size = chunk_size / 7 * 8  # 7字节进 8字节出
    cdef size_t mod = length - chunk_size * threads # 剩下的单独加密
    cdef size_t output_size = <size_t> base16384.encode_len(<int> length) + 16

    cdef char *output_buf = <char *> PyMem_Malloc(output_size)  # 老规矩加16字节
    if output_buf == NULL:
        raise MemoryError
    cdef int i
    for i in prange(threads, nogil=True, schedule="guided"):
        base16384.encode(<const char *> &data[i*chunk_size],
                                          <int>chunk_size,
                                          &output_buf[i*output_chunk_size],
                                          <int>output_chunk_size)  # encode 整数倍的那个
    cdef int count
    if mod!=0:
        count = base16384.encode(<const char *> &data[length - mod],
                                <int>mod,
                                &output_buf[threads * output_chunk_size],
                                 <int>(output_size - threads * output_chunk_size))  # 余数
    else:
        count = 0

    ret = <bytes> output_buf[:threads * output_chunk_size + count]
    PyMem_Free(output_buf)
    return ret

cpdef inline bytes _decode_parallel(const uint8_t[::1] data):
    cdef int threads = omp_get_num_procs()
    cdef size_t length = data.shape[0]
    cdef size_t chunk_size = length / threads / 8 * 8  # 有几个线程分成几块 还要保证是8的倍数
    cdef size_t output_chunk_size = chunk_size / 8 * 7  # 8字节进 7字节出
    cdef size_t mod = length - chunk_size * threads  # 剩下的单独加密
    cdef size_t output_size = <size_t> base16384.decode_len(<int> length, 0) + 16

    cdef char *output_buf = <char *> PyMem_Malloc(output_size)  # 老规矩加16字节
    if output_buf == NULL:
        raise MemoryError
    cdef int i
    for i in prange(threads, nogil=True, schedule="guided"):
        base16384.decode(<const char *> &data[i * chunk_size],
                         <int> chunk_size,
                         &output_buf[i * output_chunk_size],
                         <int> output_chunk_size)  # encode 整数倍的那个
    cdef int count
    if mod != 0:
        count = base16384.decode(<const char *> &data[length - mod],
                                 <int> mod,
                                 &output_buf[threads * output_chunk_size],
                                 <int> (output_size - threads * output_chunk_size))  # 余数
    else:
        count = 0

    ret = <bytes> output_buf[:threads * output_chunk_size + count]
    PyMem_Free(output_buf)
    return ret

cpdef inline void encode_file(object input,
                       object output,
                       bint write_head = False,
                       int32_t buf_rate = 10) with gil:
    if not PyFile_Check(input):
        raise TypeError("input except a file-like object, got %s" % type(input).__name__)
    if not PyFile_Check(output):
        raise TypeError("output except a file-like object, got %s" % type(output).__name__)
    if buf_rate <= 0:
        buf_rate = 1

    if write_head:
        output.write(b'\xfe\xff')

    cdef int32_t current_buf_len = buf_rate * 7  # 一次读取这么多字节
    cdef size_t output_size = <size_t> base16384.encode_len(<int> current_buf_len) + 16 # 因为encode_len不是单调的 这16备用
    cdef char *output_buf = <char *> PyMem_Malloc(output_size)
    if output_buf == NULL:
        raise MemoryError

    cdef Py_ssize_t size
    cdef uint8_t first_check = 1  # 检查一次就行了 怎么可能出现第一次读出来是bytes 以后又变卦了的对象呢 不会吧不会吧
    cdef int count = 0
    while True:
        chunk = input.read(current_buf_len)
        if first_check:
            first_check = 0
            if not PyBytes_Check(chunk):
                raise TypeError(f"input must be a file-like rb object, got {type(input).__name__}")
        size = PyBytes_Size(chunk)
        if <int32_t> size < current_buf_len:  # 数据不够了 要减小一次读取的量
            if buf_rate > 1:  # 重新设置一次读取的大小 重新设置流的位置 当然要是已经是一次读取7字节了 那就不能再变小了 直接encode吧
                buf_rate = buf_rate / 2
                current_buf_len = buf_rate * 7
                input.seek(-size, 1)
                continue

        count = base16384.encode(<const char*>PyBytes_AsString(chunk), <int>size, output_buf, <int> output_size)
        output.write(<bytes>output_buf[:count])
        if size < 7:
            break
    PyMem_Free(output_buf)

cpdef inline void decode_file(object input,
                       object output,
                       int32_t buf_rate = 10) with gil:
    if not PyFile_Check(input):
        raise TypeError("input except a file-like object, got %s" % type(input).__name__)
    if not PyFile_Check(output):
        raise TypeError("output except a file-like object, got %s" % type(output).__name__)
    if buf_rate <= 0:
        buf_rate = 1

    chunk = input.read(1)  # type: bytes
    if not PyBytes_Check(chunk):
        raise TypeError(f"input must be a file-like rb object, got {type(input).__name__}")
    if chunk == b"\xfe":  # 去头
        input.read(1)
    else:
        input.seek(0, 0)  # 没有头 回到开头

    cdef int32_t current_buf_len = buf_rate * 8
    cdef size_t output_size = <size_t> base16384.decode_len(<int> current_buf_len, 0) + 16
    cdef char *output_buf = <char *> PyMem_Malloc(output_size)
    if output_buf == NULL:
        raise MemoryError
    cdef Py_ssize_t size
    cdef int count = 0
    while True:
        chunk = input.read(current_buf_len)  # 8的倍数
        size = PyBytes_Size(chunk)
        if size == 0:
            break
        if <int32_t> size < current_buf_len:  # 长度不够了
            if buf_rate > 1:  # 还能继续变小
                buf_rate = buf_rate / 2  # 重新设置一次读取的大小
                current_buf_len = buf_rate * 8
                input.seek(-size, 1)
                continue
        tmp = input.read(2)  # type: bytes
        if PyBytes_Size(tmp) == 2:
            if tmp[0] == 61:  # = stream完了   一次解码8n+2个字节
                chunk += tmp
                size += 2
            else:
                input.seek(-2, 1)

        count = base16384.decode(<const char *> PyBytes_AsString(chunk), <int> size, output_buf, <int> output_size)
        output.write(<bytes>output_buf[:count])
    PyMem_Free(output_buf)

cpdef inline bint is_64bits():
    return base16384.pybase16384_64bits()
