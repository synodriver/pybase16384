from time import time
from io import BytesIO

import pybase16384 as pybs

with open("output2.pcm", "rb") as f:
    data = f.read()

st = time()
for i in range(1):
    pybs.decode_file(BytesIO(data), open("input2.pcm",'wb'))
print(f"耗时： {time() - st}")


