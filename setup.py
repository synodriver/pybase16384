# -*- coding: utf-8 -*-
import os
import re
import glob
from collections import defaultdict
import platform
import sys

from Cython.Build import cythonize
from setuptools import Extension, setup, find_packages
from setuptools.command.build_ext import build_ext

BUILD_ARGS = defaultdict(lambda: ['-O3', '-g0'])

for compiler, args in [
    ('msvc', ['/EHsc', '/DHUNSPELL_STATIC', "/Oi", "/O2", "/Ot"]),
    ('gcc', ['-O3', '-g0'])]:
    BUILD_ARGS[compiler] = args


class build_ext_compiler_check(build_ext):
    def build_extensions(self):
        compiler = self.compiler.compiler_type
        args = BUILD_ARGS[compiler]
        for ext in self.extensions:
            ext.extra_compile_args = args
        super().build_extensions()


if sys.maxsize > 2**32:  # 64位
    CPUBIT = 64
else:
    CPUBIT = 32

system = platform.system()
if system == "Windows":
    macro_base = [("_WIN64", None), ("new", "PyMem_Malloc")]
elif system == "Linux":
    macro_base = [("__linux__", None), ("new", "PyMem_Malloc")]
elif system == "Darwin":
    macro_base = [("__MAC_10_0", None), ("new", "PyMem_Malloc")]
else:
    macro_base = [("new", "PyMem_Malloc")]

extensions = [
    Extension("pybase16384._core", ["pybase16384/_core.pyx"] + glob.glob(f'./base16384/{CPUBIT}/*.c'),
              include_dirs=[f"./base16384", "./pybase16384", f"./base16384/{CPUBIT}"],
              library_dirs=[f"./base16384"],
              define_macros=macro_base + [("CPUBIT32", None)] if CPUBIT == 32 else []
              ),
]


def get_dis():
    with open("README.markdown", "r", encoding="utf-8") as f:
        return f.read()


def get_version() -> str:
    path = os.path.join(os.path.abspath(os.path.dirname(__file__)), "pybase16384", "__init__.py")
    with open(path, "r", encoding="utf-8") as f:
        data = f.read()
    result = re.findall(r"(?<=__version__ = \")\S+(?=\")", data)
    return result[0]


packages = find_packages(exclude=('test', 'tests.*', "test*"))


def main():
    version: str = get_version()

    dis = get_dis()
    setup(
        name="pybase16384",
        version=version,
        url="https://github.com/synodriver/pybase16384",
        packages=packages,
        keywords=["encode", "decode", "16384"],
        description="16384 encode and decode",
        long_description_content_type="text/markdown",
        long_description=dis,
        author="synodriver",
        author_email="diguohuangjiajinweijun@gmail.com",
        python_requires=">=3.6",
        install_requires=["cython"],
        license='GPLv3',
        classifiers=[
            "Development Status :: 4 - Beta",
            "Operating System :: OS Independent",
            "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
            "Topic :: Security :: Cryptography",
            "Programming Language :: C",
            "Programming Language :: Cython",
            "Programming Language :: Python",
            "Programming Language :: Python :: 3.6",
            "Programming Language :: Python :: 3.7",
            "Programming Language :: Python :: 3.8",
            "Programming Language :: Python :: 3.9",
            "Programming Language :: Python :: 3.10",
            "Programming Language :: Python :: Implementation :: CPython"
        ],
        include_package_data=True,
        zip_safe=False,
        cmdclass={'build_ext': build_ext_compiler_check},
        ext_modules=cythonize(extensions,
                              compiler_directives={"cdivision": True,
                                                   "embedsignature": True,
                                                   "boundscheck": False,
                                                   "wraparound": False}),
    )


if __name__ == "__main__":
    main()
