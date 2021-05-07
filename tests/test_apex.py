import unittest
from sigma_ptpy.apex import (ShutterSpeed2, ShutterSpeed3)


class Test_ShutterSpeed2(unittest.TestCase):
    def test_decode_uint8(self):
        actual = ShutterSpeed2.decode_uint8(0b00001001)
        self.assertEqual(None, actual)

        actual = ShutterSpeed2.decode_uint8(0b00001100)
        self.assertEqual(None, actual)

        actual = ShutterSpeed2.decode_uint8(0b00010001)
        self.assertEqual(30, actual)  # 30s

        actual = ShutterSpeed2.decode_uint8(0b10110000)
        self.assertEqual(1 / 32000, actual)  # 1/32000s

    def test_encode_uint8(self):
        actual = ShutterSpeed2.encode_uint8(30)
        self.assertEqual(0b00010001, actual)  # 30s

        actual = ShutterSpeed2.encode_uint8(1 / 32000)
        self.assertEqual(0b10110000, actual)  # 1/32000s

        actual = ShutterSpeed2.encode_uint8(100)
        self.assertEqual(0b00010001, actual)  # 30s

        actual = ShutterSpeed2.encode_uint8(1 / 105)
        self.assertEqual(0b01110000, actual)  # 1/125

        actual = ShutterSpeed2.encode_uint8(1 / 34000)
        self.assertEqual(0b10110000, actual)  # 1/32000


class Test_ShutterSpeed3(unittest.TestCase):
    def test_decode_uint8(self):
        actual = ShutterSpeed3.decode_uint8(0b00001001)
        self.assertEqual(None, actual)

        actual = ShutterSpeed3.decode_uint8(0b00001011)
        self.assertEqual(None, actual)

        actual = ShutterSpeed3.decode_uint8(0b00010000)
        self.assertEqual(30, actual)  # 30s

        actual = ShutterSpeed3.decode_uint8(0b10110000)
        self.assertEqual(1 / 32000, actual)  # 1/32000s

    def test_encode_uint8(self):
        actual = ShutterSpeed3.encode_uint8(30)
        self.assertEqual(0b00010000, actual)  # 30s

        actual = ShutterSpeed3.encode_uint8(1 / 32000)
        self.assertEqual(0b10110000, actual)  # 1/32000s

        actual = ShutterSpeed3.encode_uint8(100)
        self.assertEqual(0b00010000, actual)  # 30s

        actual = ShutterSpeed3.encode_uint8(1 / 105)
        self.assertEqual(0b01101101, actual)  # 1/100

        actual = ShutterSpeed3.encode_uint8(1 / 34000)
        self.assertEqual(0b10110000, actual)  # 1/32000
