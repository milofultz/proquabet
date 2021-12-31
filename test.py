import string
import unittest

import main as proquabet


class TestTextDecoder(unittest.TestCase):
    def test_standard_ascii(self):
        cases = {
            'A A': [0x41, 0x20, 0x41],
            '123': [0x31, 0x32, 0x33],
            string.printable: [ord(char) for char in string.printable]
        }
        for example_input, expected in cases.items():
            actual = proquabet.decode_text(example_input)
            self.assertEqual(expected, actual)

    def test_utf_8_characters(self):
        cases = {
            'ก': [0x0E01],  # THAI CHARACTER KO KAI
            '€': [0x20AC],  # EURO SIGN
            '🨀': [0x1FA00],  # NEUTRAL CHESS KING
            '􀃿': [0x1000FF],  # The highest possible character (in hex value) as of
                              # https://www.utf8-chartable.de/unicode-utf8-table.pl
        }
        for example_input, expected in cases.items():
            actual = proquabet.decode_text(example_input)
            self.assertEqual(expected, actual)


class TestProquintEncoder(unittest.TestCase):
    def test_8_bit_number(self):
        cases = {
            0x00: 'babab',
            0xff: 'baguz',
            0x88: 'bafam',
            0x10: 'babib',
        }
        for example_input, expected in cases.items():
            actual = proquabet.encode_proquint(example_input)
            self.assertEqual(expected, actual)

    def test_16_bit_number(self):
        cases = {
            0x0000: 'babab',
            0xffff: 'zuzuz',
            0x8888: 'mofam',
            0x1010: 'dabib',
        }
        for example_input, expected in cases.items():
            actual = proquabet.encode_proquint(example_input)
            self.assertEqual(expected, actual)


if __name__ == '__main__':
    unittest.main()
