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

// base16384_encode_fp encodes input file to output file.
//    encbuf & decbuf must be no less than BASE16384_ENCBUFSZ & BASE16384_DECBUFSZ
base16384_err_t base16384_encode_fp(FILE* input, FILE* output, char* encbuf, char* decbuf);

// base16384_encode_fd encodes input fd to output fd.
//    encbuf & decbuf must be no less than BASE16384_ENCBUFSZ & BASE16384_DECBUFSZ
base16384_err_t base16384_encode_fd(int input, int output, char* encbuf, char* decbuf);

// base16384_decode_fp decodes input file to output file.
//    encbuf & decbuf must be no less than BASE16384_ENCBUFSZ & BASE16384_DECBUFSZ
base16384_err_t base16384_decode_fp(FILE* input, FILE* output, char* encbuf, char* decbuf);

// base16384_decode_fd decodes input fd to output fd.
//    encbuf & decbuf must be no less than BASE16384_ENCBUFSZ & BASE16384_DECBUFSZ
base16384_err_t base16384_decode_fd(int input, int output, char* encbuf, char* decbuf);

int32_t pybase16384_64bits();

int get_encsize();

int get_decsize();
    """
)

source = """
#include "base16384.h"

#ifdef CPUBIT32
#define pybase16384_64bits() 0
#else
#define pybase16384_64bits() 1
#endif

int get_encsize()
{
    return BASE16384_ENCBUFSZ;
}

int get_decsize()
{
    return BASE16384_DECBUFSZ;
}
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
