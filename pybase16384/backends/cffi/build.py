"""
Copyright (c) 2008-2021 synodriver <synodriver@gmail.com>
"""

import platform
import sys

from cffi import FFI

CPUBIT = 64 if sys.maxsize > 2**32 else 32
system = platform.system()
if system == "Darwin":
    macro_base = [("__MAC_10_0", None)]
elif system == "Linux":
    macro_base = [("__linux__", None)]
elif system == "Windows":
    macro_base = [("_WIN64", None)]
else:
    macro_base = []

if sys.byteorder != "little":
    macro_base.append(("WORDS_BIGENDIAN", None))

if CPUBIT == 64:
    macro_base.append(("CPUBIT64", None))
else:
    macro_base.append(("CPUBIT32", None))

ffibuilder = FFI()
ffibuilder.cdef(
    """
// base16384_err_t is the return value of base16384_en/decode_file
enum base16384_err_t {
	base16384_err_ok,
	base16384_err_get_file_size,
	base16384_err_fopen_output_file,
	base16384_err_fopen_input_file,
	base16384_err_write_file,
	base16384_err_open_input_file,
	base16384_err_map_input_file,
};
// base16384_err_t is the return value of base16384_en/decode_file
typedef enum base16384_err_t base16384_err_t;
int base16384_encode_len(int dlen);
int base16384_decode_len(int dlen, int offset);
int base16384_encode(const char* data, int dlen, char* buf, int blen);
int base16384_decode(const char* data, int dlen, char* buf, int blen);
base16384_err_t base16384_encode_file(const char* input, const char* output, char* encbuf, char* decbuf);
base16384_err_t base16384_decode_file(const char* input, const char* output, char* encbuf, char* decbuf);
int32_t pybase16384_64bits();
    """
)

source = """
#include "base16384.h"

#ifdef CPUBIT32
#define pybase16384_64bits() 0
#else
#define pybase16384_64bits() 1
#endif
"""

ffibuilder.set_source(
    "pybase16384.backends.cffi._core_cffi",
    source,
    sources=[f"./base16384/base14{CPUBIT}.c", "./base16384/file.c"],
    include_dirs=["./base16384"],
    define_macros=macro_base,
)

if __name__ == "__main__":
    ffibuilder.compile()
