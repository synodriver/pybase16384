from time import time
from io import BytesIO

import pybase16384 as pybs
pybs.is_64bits()
with open("input.pcm", "rb") as f:
    data = f.read()

st = time()
for _ in range(10):
    pybs.encode_file(BytesIO(data), open("output2.pcm", 'wb'), True, len(data)//7)
print(f"耗时： {time() - st}")