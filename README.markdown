<h1 align="center"><i>✨ pybase16384 ✨ </i></h1>

<h3 align="center">The python binding for <a href="https://github.com/fumiama/base16384">base16384</a> </h3>

<h3 align="center"><i>一种神奇的编码 </i></h3>

[![pypi](https://img.shields.io/pypi/v/pybase16384.svg)](https://pypi.org/project/pybase16384/)
![python](https://img.shields.io/pypi/pyversions/pybase16384)
![implementation](https://img.shields.io/pypi/implementation/pybase16384)
![wheel](https://img.shields.io/pypi/wheel/pybase16384)
![license](https://img.shields.io/github/license/synodriver/pybase16384.svg)
![action](https://img.shields.io/github/workflow/status/synodriver/pybase16384/build%20wheel)


### 使用

- 编码/解码文本
```python
>>> import pybase16384 as pybs
>>> pybs.encode_string('hello!!')
'栙擆羼漡'
>>> pybs.decode_string('栙擆羼漡')
'hello!!'
```

- 编码文件

```python
from io import BytesIO

import pybase16384 as pybs

with open("input.pcm", "rb") as f:
    data = f.read()
for i in range(1):
    pybs.encode_file(BytesIO(data), open("output2.pcm", 'wb'), True)
```
- 解码文件

```python
from io import BytesIO

import pybase16384 as pybs

with open("output2.pcm", "rb") as f:
    data = f.read()
for i in range(1):
    pybs.decode_file(BytesIO(data), open("input2.pcm", 'wb'))
```

### 公开函数
```python
def encode_len(dlen: int) -> int: ...

def decode_len(dlen: int, offset: int) -> int: ...

def encode(data: bytes) -> bytes: ...

def decode(data: bytes) -> bytes: ...

def decode_file(input: BinaryIO, output: BinaryIO, buf_rate: int = 10) -> None: ...

def encode_file(input: BinaryIO, output: BinaryIO, boolwrite_head: bool = False, buf_rate: int = 10) -> None: ...

def encode_from_string(data: str, write_head: bool = False) -> bytes: ...

def encode_to_string(data: bytes) -> str: ...

def encode_string(data: str) -> str: ...

def decode_from_bytes(data: bytes) -> str: ...

def decode_from_string(data: str) -> bytes: ...

def decode_string(data: str) -> str: ...
```
- write_head将显式指明编码出的文本格式(utf16be)，以便文本编辑器(如记事本)能够正确渲染，一般在写入文件时使用。

- buf_rate指定读取文件的策略。当它为n时，则表示一次读取7n或者8n个字节。如果读到的字节长度小于预期，则说明长度不够，
此时，n将减半，恢复文件指针，重新读取。如果当n=1时长度仍然不够，就地encode/decode处理之。

- ```encode_len```和```decode_len```用于计算输出的长度

### 内部函数

- 他们直接来自底层的C库，高性能，但是一般不需要在外部使用（除非是增加性能）

```python
def _encode(data: BufferProtocol) -> bytes: ...

def _decode(data: BufferProtocol) -> bytes: ...

def _encode_into(data: BufferProtocol, dest: BufferProtocol) -> int: ...

def _decode_into(data: BufferProtocol, dest: BufferProtocol) -> int: ...

def is_64bits() -> bool: ...
```
- ```_decode```在解码```b'='```开头的数据时***不安全***：***解释器异常***
- ```_encode_into```和```_decode_into```直接操作缓冲区对象的底层指针，0拷贝，当然也和上面一样的问题，他们是没有检查的

### ✨  v0.3更新 ✨ 
融合了 [CFFI](https://github.com/synodriver/pybase16384-cffi) 版本的成果，现在一个包可以同时在cpython和pypy上运行

### 本机编译
```
python -m pip install setuptools wheel cython cffi
git clone https://github.com/synodriver/pybase16384
cd pybase16384
git submodule update --init --recursive
python setup.py bdist_wheel --use-cython --use-cffi
```

### 后端选择
默认由py实现决定，在cpython上自动选择cython后端，在pypy上自动选择cffi后端，使用```B14_USE_CFFI```环境变量可以强制选择cffi