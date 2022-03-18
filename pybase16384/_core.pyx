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

cpdef bytes _encode(const uint8_t[:] data):
    cdef size_t length = data.shape[0]
    cdef base16384.LENDAT *cret = base16384.encode(<const uint8_t *> &data[0],<const int32_t>length) # encode 整数倍的那个
    ret = <bytes> cret.data[:cret.len]
    base16384.LENDAT_Del(&cret)
    return ret

cpdef bytes _decode(const uint8_t[:] data):
    cdef size_t length = data.shape[0]
    cdef base16384.LENDAT *cret = base16384.decode(<const uint8_t *> &data[0], <const int32_t>length)
    ret = <bytes> cret.data[:cret.len]
    base16384.LENDAT_Del(&cret)
    return ret

cpdef void encode_file(object input,
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

    cdef int32_t current_buf_len = buf_rate * 7
    cdef Py_ssize_t size
    cdef uint8_t first_check = 1  # 检查一次就行了 怎么可能出现第一次读出来是bytes 以后又变卦了的对象呢 不会吧不会吧
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

        ot = _encode(chunk)  # type: bytes
        output.write(ot)
        if size < 7:
            break

cpdef void decode_file(object input,
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
    cdef Py_ssize_t size
    cdef uint8_t can_skip_check = 0  # 不能跳过结尾检查
    while True:
        if not can_skip_check:
            chunk = input.read(2)  # type: bytes
            if PyBytes_Size(chunk) > 0:
                if chunk[0] == 61:  # = stream完了
                    output.write(chunk)
                    break
                else:
                    input.seek(-2, 1)
            else:
                break
        can_skip_check = 0

        chunk = input.read(current_buf_len)  # 8的倍数
        size = PyBytes_Size(chunk)
        if <int32_t> size < current_buf_len:  # 长度不够了
            if buf_rate > 1:  # 还能继续变小
                buf_rate = buf_rate / 2  # 重新设置一次读取的大小
                current_buf_len = buf_rate * 8
                input.seek(-size, 1)
                can_skip_check = 1  # 这次就可以跳过结尾检查
                continue
        ot = _decode(chunk)  # type: bytes
        output.write(ot)
        if size < 8:
            break
