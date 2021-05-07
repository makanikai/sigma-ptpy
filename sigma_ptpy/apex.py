"""APEX (ISO sensitivity, exposure compensation, shutter speed, and aperture) conversion"""


def _bsearch_nearest(compare, lst):
    n = len(lst)
    if n == 0:
        return None
    elif n == 1:
        return 0
    else:  # n >= 2
        imin = 0
        imax = n - 1
        while imin <= imax:
            i = int((imax - imin) / 2) + imin
            e = compare(lst[i])
            if e < 0:  # target < x
                imax = i - 1
            elif e > 0:  # target > x
                imin = i + 1
            else:
                return i

        def abs_cmp(x):
            return abs(compare(x))

        j = i
        if 0 < i and abs_cmp(lst[j]) > abs_cmp(lst[i - 1]):
            j = i - 1
        if i < n - 1 and abs_cmp(lst[j]) > abs_cmp(lst[i + 1]):
            j = i + 1

        return j


class ApexConverter(object):
    def __init__(self, table):
        self.__dectable = table
        self.__enctable = sorted(table, key=lambda x: x[1])

    def decode_uint8(self, code):
        """Decodes a 8-bit integer code.

        Args:
           code (int): a 8-bit integer code returned from a camera.

        Returns:
           int or float: an APEX value."""
        i = _bsearch_nearest(lambda x: code - x[0], self.__dectable)
        code_, val = self.__dectable[i]
        return val if code == code_ else None

    def encode_uint8(self, val):
        """Encodes an APEX value.

        If an given value is not found in a conversion table, the nearest value is encoded.

        Args:
           val (int or float): an APEX value.

        Returns:
           int: a 8-bit integer code passed to a camera."""
        i = _bsearch_nearest(lambda x: val - x[1], self.__enctable)
        return self.__enctable[i][0]


ISOSpeedConverter = ApexConverter([
    (0, 6), (3, 8), (5, 10), (8, 12), (11, 16), (13, 20), (16, 25), (19, 32), (21, 40),
    (24, 50), (27, 64), (29, 80), (32, 100), (35, 125), (37, 160), (40, 200), (43, 250),
    (45, 320), (48, 400), (51, 500), (53, 640), (56, 800), (59, 1000), (61, 1250),
    (64, 1600), (67, 2000), (69, 2500), (72, 3200), (75, 4000), (77, 5000), (80, 6400),
    (83, 8000), (85, 10000), (88, 12800), (91, 16000), (93, 20000), (96, 25600),
    (99, 32000), (101, 40000), (104, 51200), (107, 64000), (109, 80000), (112, 102400)
])
"""ApexConverter: ISO sensitivity converter."""

ExpComp2Converter = ApexConverter([
    (0, 0.0), (4, 0.5), (8, 1.0), (12, 1.5), (16, 2.0), (20, 2.5), (24, 3.0),
    (232, -3.0), (236, -2.5), (240, -2.0), (244, -1.5), (248, -1.0), (252, -0.5)
])
"""ApexConverter: 1/2 step exposure compensation converter."""

ExpComp3Converter = ApexConverter([
    (0, 0.0), (3, 0.3), (5, 0.7), (8, 1.0), (11, 1.3), (14, 1.7), (16, 2.0),
    (19, 2.3), (21, 2.7), (24, 3.0), (27, 3.3), (29, 3.7), (32, 4.0), (35, 4.3),
    (37, 4.7), (40, 5.0), (43, 5.3), (45, 5.7), (48, 6.0), (51, 6.3),
    (205, -6.3), (208, -6.0), (211, -5.7), (213, -5.3), (216, -5.0), (219, -4.7),
    (221, -4.3), (224, -4.0), (227, -3.7), (229, -3.3), (232, -3.0), (235, -2.7),
    (237, -2.3), (240, -2.0), (243, -1.7), (245, -1.3), (248, -1.0), (251, -0.7),
    (253, -0.4)
])
"""ApexConverter: 1/3 step exposure compensation converter."""

ShutterSpeed2Converter = ApexConverter([
    (17, 30), (20, 20), (24, 15), (28, 10), (32, 8), (36, 6), (40, 4),
    (44, 3), (48, 2), (52, 1.5), (56, 1), (60, 0.7), (64, 1 / 2), (68, 1 / 3),
    (72, 1 / 4), (76, 1 / 6), (80, 1 / 8), (84, 1 / 10), (88, 1 / 15), (92, 1 / 20), (96, 1 / 30),
    (100, 1 / 45), (104, 1 / 60), (108, 1 / 90), (112, 1 / 125), (116, 1 / 180), (120, 1 / 250),
    (124, 1 / 350), (128, 1 / 500), (132, 1 / 750), (136, 1 / 1000), (140, 1 / 1500),
    (144, 1 / 2000), (148, 1 / 3000), (152, 1 / 4000), (156, 1 / 6000), (160, 1 / 8000),
    (168, 1 / 16000), (176, 1 / 32000)
])
"""ApexConverter: 1/2 step shutter speed converter."""

ShutterSpeed3Converter = ApexConverter([
    (16, 30), (19, 25), (21, 20), (24, 15), (27, 13), (29, 10),
    (32, 8), (35, 6), (37, 5), (40, 4), (43, 3.2), (45, 2.5), (48, 2),
    (51, 1.6), (53, 1.3), (56, 1), (59, 0.8), (61, 0.6), (64, 0.5), (67, 0.4),
    (69, 0.3), (72, 1 / 4), (75, 1 / 5), (77, 1 / 6), (80, 1 / 8), (83, 1 / 10), (85, 1 / 13),
    (88, 1 / 15), (91, 1 / 20), (93, 1 / 25), (96, 1 / 30), (99, 1 / 40), (101, 1 / 50), (104, 1 / 60),
    (107, 1 / 80), (109, 1 / 100), (112, 1 / 125), (115, 1 / 160), (117, 1 / 200), (120, 1 / 250),
    (123, 1 / 320), (125, 1 / 400), (128, 1 / 500), (131, 1 / 640), (133, 1 / 800), (136, 1 / 1000),
    (139, 1 / 1250), (141, 1 / 1600), (144, 1 / 2000), (147, 1 / 2500), (149, 1 / 3200), (152, 1 / 4000),
    (155, 1 / 5000), (157, 1 / 6000), (160, 1 / 8000), (163, 1 / 10000), (165, 1 / 12800),
    (168, 1 / 16000), (171, 1 / 20000), (173, 1 / 25600), (176, 1 / 32000)
])
"""ApexConverter: 1/3 step shutter speed converter."""

Aperture2Converter = ApexConverter([
    (8, 1.0), (12, 1.2), (16, 1.4), (20, 1.8), (28, 2.5), (32, 2.8), (36, 3.5),
    (40, 4.0), (44, 4.5), (48, 5.6), (52, 6.7), (56, 8.0), (60, 9.5), (64, 11),
    (68, 13), (72, 16), (76, 19), (80, 22), (84, 27), (88, 32), (92, 38),
    (96, 45), (100, 54), (104, 64), (108, 76), (112, 91),
])
"""ApexConverter: 1/2 step aperture converter."""

Aperture3Converter = ApexConverter([
    (8, 1.0), (11, 1.1), (13, 1.2), (16, 1.4), (19, 1.6), (21, 1.8), (24, 2.0),
    (27, 2.2), (29, 2.5), (32, 2.8), (35, 3.2), (37, 3.5), (40, 4.0), (43, 4.5),
    (45, 5.0), (48, 5.6), (51, 6.3), (53, 7.1), (56, 8.0), (59, 9.0), (61, 10),
    (64, 11), (67, 13), (69, 14), (72, 16), (75, 18), (77, 20), (80, 22),
    (83, 25), (85, 29), (88, 32), (91, 36), (93, 40), (96, 45), (99, 51),
    (191, 57), (104, 64), (107, 72), (108, 76), (112, 91),
])
"""ApexConverter: 1/3 step aperture converter."""
