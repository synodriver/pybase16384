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

- decode
```python
from io import BytesIO

import pybase16384 as pybs

with open("output2.pcm", "rb") as f:
    data = f.read()


for i in range(1):
    pybs.decode_file(BytesIO(data), open("input2.pcm",'wb'))
```
- encode
```python
from io import BytesIO

import pybase16384 as pybs

with open("input.pcm", "rb") as f:
    data = f.read()
for i in range(1):
    pybs.encode_file(BytesIO(data), open("output2.pcm",'wb'), True)
```

### 公开函数
```python
from typing import BinaryIO

def decode_file(input: BinaryIO, output: BinaryIO) -> None: ...

def encode_file(input: BinaryIO, output: BinaryIO, boolwrite_head: bool = False) -> None: ...

def encode_from_string(data: str, write_head: bool = False) -> bytes: ...

def decode_from_bytes(data: bytes) -> str: ...
```
- write_head可以让编码出来的像是一堆utf16，即一堆神奇的汉字，一般在写入文件的时候使用，notepad打开的时候感觉就是一堆汉字