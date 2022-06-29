"""
Copyright (c) 2008-2021 synodriver <synodriver@gmail.com>
"""
import platform
import sys

from cffi import FFI

if sys.maxsize > 2**32:
    CPUBIT = 64
else:
    CPUBIT = 32

system = platform.system()
if system == "Windows":
    macro_base = [("_WIN64", None)]
elif system == "Linux":
    macro_base = [("__linux__", None)]
elif system == "Darwin":
    macro_base = [("__MAC_10_0", None)]
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
int encode_len(int dlen);
int decode_len(int dlen, int offset);
int encode(const char* data, int dlen, char* buf, int blen);
int decode(const char* data, int dlen, char* buf, int blen);
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
    sources=[f"./base16384/base14{CPUBIT}.c"],
    include_dirs=["./base16384"],
    define_macros=macro_base,
)

if __name__ == "__main__":
    ffibuilder.compile()
