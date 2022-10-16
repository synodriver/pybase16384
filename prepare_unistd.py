"""
Copyright (c) 2008-2022 synodriver <synodriver@gmail.com>
"""

source = """#ifndef _UNISTD_H
#define _UNISTD_H

#include <io.h>
#include <process.h>

#endif"""

with open(r"base16384\unistd.h", "w") as f:
    f.write(source)
