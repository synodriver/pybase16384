from time import time
from io import BytesIO

import pybase16384 as pybs

with open("input.pcm", "rb") as f:
    data = f.read()

st = time()
for i in range(1):
    pybs.encode_file(BytesIO(data), open("output2.pcm", 'wb'), True)
print(f"耗时： {time() - st}")


from array import array