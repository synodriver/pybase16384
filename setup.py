# -*- coding: utf-8 -*-
import os
import platform
import re
import sys
from collections import defaultdict

try:
    from Cython.Build import cythonize
except ImportError:
    Cython = None
from setuptools import Extension, find_packages, setup
from setuptools.command.build_ext import build_ext

BUILD_ARGS = defaultdict(lambda: ["-O3", "-g0"])

for compiler, args in [
    ("msvc", ["/EHsc", "/DHUNSPELL_STATIC", "/Oi", "/O2", "/Ot"]),
    ("gcc", ["-O3", "-g0"]),
]:
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

print(macro_base)
extensions = [
    Extension(
        "pybase16384.backends.cython._core_cy",
        ["pybase16384/backends/cython/_core_cy.pyx", f"./base16384/base14{CPUBIT}.c"],
        include_dirs=[f"./base16384"],
        library_dirs=[f"./base16384"],
        define_macros=macro_base,
    ),
]
cffi_modules = ["pybase16384/backends/cffi/build.py:ffibuilder"]


def get_dis():
    with open("README.markdown", "r", encoding="utf-8") as f:
        return f.read()


def get_version() -> str:
    path = os.path.join(
        os.path.abspath(os.path.dirname(__file__)), "pybase16384", "__init__.py"
    )
    with open(path, "r", encoding="utf-8") as f:
        data = f.read()
    result = re.findall(r"(?<=__version__ = \")\S+(?=\")", data)
    return result[0]


packages = find_packages(exclude=("test", "tests.*", "test*"))


def has_option(name: str) -> bool:
    if name in sys.argv[1:]:
        sys.argv.remove(name)
        return True
    return False


setup_requires = []
install_requires = []
setup_kw = {}
if has_option("--use-cython"):
    print("building cython")
    setup_requires.append("cython")
    setup_kw["ext_modules"] = cythonize(
        extensions,
        compiler_directives={
            "cdivision": True,
            "embedsignature": True,
            "boundscheck": False,
            "wraparound": False,
        },
    )
if has_option("--use-cffi"):
    print("building cffi")
    setup_requires.append("cffi>=1.0.0")
    install_requires.append("cffi>=1.0.0")
    setup_kw["cffi_modules"] = cffi_modules


def main():
    version: str = get_version()
    dis = get_dis()
    setup(
        name="pybase16384",
        version=version,
        url="https://github.com/synodriver/pybase16384",
        packages=packages,
        keywords=["encode", "decode", "base16384"],
        description="base16384 encode and decode",
        long_description_content_type="text/markdown",
        long_description=dis,
        author="synodriver",
        author_email="diguohuangjiajinweijun@gmail.com",
        python_requires=">=3.6",
        setup_requires=setup_requires,
        install_requires=install_requires,
        license="GPLv3",
        classifiers=[
            "Development Status :: 5 - Production/Stable",
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
            "Programming Language :: Python :: Implementation :: CPython",
            "Programming Language :: Python :: Implementation :: PyPy",
        ],
        include_package_data=True,
        zip_safe=False,
        cmdclass={"build_ext": build_ext_compiler_check},
        **setup_kw,
    )


if __name__ == "__main__":
    main()
