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
>>> pybs.encode_to_string(b'hello!!')
栙擆羼漡
>>> pybs.decode_from_string("栙擆羼漡")
b'hello!!'
```

- 编码文件
```python
from io import BytesIO

import pybase16384 as pybs

with open("input.pcm", "rb") as f:
    data = f.read()
for i in range(1):
    pybs.encode_file(BytesIO(data), open("output2.pcm",'wb'), True)
```
- 解码文件
```python
from io import BytesIO

import pybase16384 as pybs

with open("output2.pcm", "rb") as f:
    data = f.read()
for i in range(1):
    pybs.decode_file(BytesIO(data), open("input2.pcm",'wb'))
```

### 公开函数
```python
def decode_file(input: BinaryIO, output: BinaryIO) -> None: ...

def encode_file(input: BinaryIO, output: BinaryIO, boolwrite_head: bool = False) -> None: ...

def encode_from_string(data: str, write_head: bool = False) -> bytes: ...

def encode_to_string(data: bytes) -> str: ...

def decode_from_bytes(data: bytes) -> str: ...

def decode_from_string(data: str) -> bytes:
```
- write_head将显式指明编码出的文本格式(utf16be)，以便文本编辑器(如记事本)能够正确渲染，一般在写入文件时使用。