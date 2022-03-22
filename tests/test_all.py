from unittest import TestCase
import unittest
import time
import sys
from random import randint

import pybase16384 as bs


class Test(TestCase):
    def test_fvarlength(self):
        value = b"="
        for i in range(1000):
            value += b"x"
            self.assertEqual(bs.decode(bs.encode(value)), value)

    def test_rand(self):
        for i in range(10000):
            length = randint(1, 1000)
            value = bytes([randint(0, 255) for _ in range(length)])
            self.assertEqual(bs.decode(bs.encode(value)), value)

    def test_chn(self):
        dt = bs.decode_from_string('嵞喇濡虸氞喇濡虸氞喇濡虸氞咶箭祫棚薇濡蘀㴆')
        self.assertEqual(dt, b'=xxxxxxxxxxxxxxxxxxxxxxkkkkkkkxxxx')

    def test_zerocopy(self):
        dst = bytearray(300)
        for i in range(10000):
            length = randint(1, 200)
            value = bytes([randint(0, 255) for _ in range(length)])
            cnt = bs._encode_into(value, dst)
            self.assertEqual(bs.decode(dst[:cnt]), value)

    def test_bit(self):
        if sys.maxsize > 2 ** 32:
            self.assertEqual(bs.is_64bits(), True)
        else:
            self.assertEqual(bs.is_64bits(), False)

    def test_parallel(self):
        for i in range(10000):
            length = randint(1, 1000)
            value = bytes([randint(0, 255) for _ in range(length)])
            data = bs._encode_parallel(value)
            data2 = bs._encode(value)
            self.assertEqual(data, data2)

            # self.assertEqual(bs.decode(data2), bs._decode_parallel(data2))

    def test_speed(self):
        value = bytes(5000000)
        start = time.time()
        for i in range(1):
            data = bs._encode_parallel(value)
        print(f"multithread {time.time()-start}")
        start = time.time()
        for i in range(1):
            data2 = bs._encode(value)
        print(f"single {time.time() - start}")


if __name__ == "__main__":
    unittest.main()
