import unittest
from sigma_ptpy.apex import (ShutterSpeed2Converter, ShutterSpeed3Converter)


class Test_ShutterSpeed2Converter(unittest.TestCase):
    def test_decode_uint8(self):
        actual = ShutterSpeed2Converter.decode_uint8(0b00001001)
        self.assertEqual(None, actual)

        actual = ShutterSpeed2Converter.decode_uint8(0b00001100)
        self.assertEqual(None, actual)

        actual = ShutterSpeed2Converter.decode_uint8(0b00010001)
        self.assertEqual(30, actual)  # 30s

        actual = ShutterSpeed2Converter.decode_uint8(0b10110000)
        self.assertEqual(1 / 32000, actual)  # 1/32000s

    def test_encode_uint8(self):
        actual = ShutterSpeed2Converter.encode_uint8(30)
        self.assertEqual(0b00010001, actual)  # 30s

        actual = ShutterSpeed2Converter.encode_uint8(1 / 32000)
        self.assertEqual(0b10110000, actual)  # 1/32000s

        actual = ShutterSpeed2Converter.encode_uint8(100)
        self.assertEqual(0b00010001, actual)  # 30s

        actual = ShutterSpeed2Converter.encode_uint8(1 / 105)
        self.assertEqual(0b01110000, actual)  # 1/125

        actual = ShutterSpeed2Converter.encode_uint8(1 / 34000)
        self.assertEqual(0b10110000, actual)  # 1/32000


class Test_ShutterSpeed3Converter(unittest.TestCase):
    def test_decode_uint8(self):
        actual = ShutterSpeed3Converter.decode_uint8(0b00001001)
        self.assertEqual(None, actual)

        actual = ShutterSpeed3Converter.decode_uint8(0b00001011)
        self.assertEqual(None, actual)

        actual = ShutterSpeed3Converter.decode_uint8(0b00010000)
        self.assertEqual(30, actual)  # 30s

        actual = ShutterSpeed3Converter.decode_uint8(0b10110000)
        self.assertEqual(1 / 32000, actual)  # 1/32000s

    def test_encode_uint8(self):
        actual = ShutterSpeed3Converter.encode_uint8(30)
        self.assertEqual(0b00010000, actual)  # 30s

        actual = ShutterSpeed3Converter.encode_uint8(1 / 32000)
        self.assertEqual(0b10110000, actual)  # 1/32000s

        actual = ShutterSpeed3Converter.encode_uint8(100)
        self.assertEqual(0b00010000, actual)  # 30s

        actual = ShutterSpeed3Converter.encode_uint8(1 / 105)
        self.assertEqual(0b01101101, actual)  # 1/100

        actual = ShutterSpeed3Converter.encode_uint8(1 / 34000)
        self.assertEqual(0b10110000, actual)  # 1/32000
