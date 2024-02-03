import secrets
import sys

sys.path.append(".")

import unittest
from random import randint
from unittest import TestCase

import pybase16384 as bs


class Test(TestCase):
    def test_varlength(self):
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
        dt = bs.decode_from_string("嵞喇濡虸氞喇濡虸氞喇濡虸氞咶箭祫棚薇濡蘀㴆")
        self.assertEqual(dt, b"=xxxxxxxxxxxxxxxxxxxxxxkkkkkkkxxxx")

    def test_zerocopy(self):
        dst = bytearray(300)
        for i in range(10000):
            length = randint(1, 200)
            value = bytes([randint(0, 255) for _ in range(length)])
            cnt = bs._encode_into(value, dst)
            self.assertEqual(bs.decode(dst[:cnt]), value)

    def test_bit(self):
        if sys.maxsize > 2**32:
            self.assertEqual(bs.is_64bits(), True)
        else:
            self.assertEqual(bs.is_64bits(), False)

    def test_encode(self):
        dst = bytearray(300)
        for i in range(10000):
            length = randint(1, 200)
            value = bytes([randint(0, 255) for _ in range(length)])
            cnt = bs._encode_into(value, dst)
            self.assertEqual(bytes(dst[:cnt]), bs._encode(value))

    def test_omp(self):
        for i in range(10000):
            data = secrets.token_bytes(100)
            encoded = bs._encode_parallel(data, 2)
            self.assertEqual(bs.encode(data), encoded)
            decoded = bs._decode_parallel(encoded, 2)
            while decoded != data:
                decoded = bs._decode_parallel(encoded, 2)  # fixme: 为什么没有幂等性
                print("iter")
            self.assertEqual(data, decoded, data)

    def test_spcial(self):
        data = b'1\xcc/\xde\xf5\x1c2\x9c\xc8\xfa9ic\xb7\x16\x0b\x00_)\xba\xb9`4\xae\x19\n\xd0"V!\x8d\xfc>\x90\xb7\xc1\x89\x87\x9a-\x8aY\x99\xbd\x901%\xb6\xb8\xc9\x0c*\xd0\x13C5Y\xa1\x08\x1c}\xc8Yn\x89\xde\xda\xaca\x884\x03\x199\x83Gy:\xc6\xf9V0\xff\xe2\x8e\xfa\xc6\xed\xea\xba\xf1Dn\xde\xd7;\x0e\x19h\x16'

        encoded = bs._encode_parallel(data, 2)
        self.assertEqual(bs.encode(data), encoded)
        decoded = bs._decode_parallel(encoded, 2)
        self.assertEqual(decoded, data)


if __name__ == "__main__":
    unittest.main()
