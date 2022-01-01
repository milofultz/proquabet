import re
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


class TestTextEncoder(unittest.TestCase):
    def test_standard_ascii(self):
        cases = {
            'A A': [0x41, 0x20, 0x41],
            '123': [0x31, 0x32, 0x33],
            string.printable: [ord(char) for char in string.printable]
        }
        for expected, example_input in cases.items():
            actual = proquabet.encode_text(example_input)
            self.assertEqual(expected, actual)

    def test_utf_8_characters(self):
        cases = {
            'ก': [0x0E01],  # THAI CHARACTER KO KAI
            '€': [0x20AC],  # EURO SIGN
            '🨀': [0x1FA00],  # NEUTRAL CHESS KING
            '􀃿': [0x1000FF],  # The highest possible character (in hex value) as of
                              # https://www.utf8-chartable.de/unicode-utf8-table.pl
        }
        for expected, example_input in cases.items():
            actual = proquabet.encode_text(example_input)
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

    def test_32_bit_number(self):
        cases = {
            0xffffffff: 'zuzuz-zuzuz',
            0x88888888: 'mofam-mofam',
            0x10101010: 'dabib-dabib',
            0x12345678: 'damuh-jinum',
        }
        for example_input, expected in cases.items():
            actual = proquabet.encode_proquint(example_input)
            self.assertEqual(expected, actual)


class TestProquintDecoder(unittest.TestCase):
    def test_8_bit_number(self):
        cases = {
            0x00: 'babab',
            0xff: 'baguz',
            0x88: 'bafam',
            0x10: 'babib',
        }
        for expected, example_input in cases.items():
            actual = proquabet.decode_proquint(example_input)
            self.assertEqual(expected, actual)

    def test_16_bit_number(self):
        cases = {
            0x0000: 'babab',
            0xffff: 'zuzuz',
            0x8888: 'mofam',
            0x1010: 'dabib',
        }
        for expected, example_input in cases.items():
            actual = proquabet.decode_proquint(example_input)
            self.assertEqual(expected, actual)

    def test_32_bit_number(self):
        cases = {
            0xffffffff: 'zuzuz-zuzuz',
            0x88888888: 'mofam-mofam',
            0x10101010: 'dabib-dabib',
            0x12345678: 'damuh-jinum',
        }
        for expected, example_input in cases.items():
            actual = proquabet.decode_proquint(example_input)
            self.assertEqual(expected, actual)


class TestTextToProquint(unittest.TestCase):
    def test_text_only(self):
        cases = {
            'Hello World!': 'hodoj kudos kusob jitoz lanos kibod',
        }
        for example_input, expected in cases.items():
            actual = proquabet.text_to_proquint(example_input)
            self.assertEqual(expected, actual)

    def test_with_utf_8(self):
        cases = {
            '😎 Cool': 'babad-zimav fadag kutoz bados',
        }
        for example_input, expected in cases.items():
            actual = proquabet.text_to_proquint(example_input)
            self.assertEqual(expected, actual)

    def test_random_punc(self):
        re_punctuation = re.compile(rf'[{proquabet.PUNCTUATION}]')
        cases = {
            'Hello World!': 'hodoj kudos kusob jitoz lanos kibod',
        }
        for example_input, expected in cases.items():
            for i in range(25):
                actual = proquabet.text_to_proquint(example_input, True)
                actual_filtered = re_punctuation.sub('', actual)\
                    .replace('\n\n', ' ')\
                    .lower()
                self.assertEqual(expected, actual_filtered)


class TestProquintToText(unittest.TestCase):
    def test_text_only(self):
        cases = {
            'Hello World!': 'hodoj kudos kusob jitoz lanos kibod',
        }
        for expected, example_input in cases.items():
            actual = proquabet.proquint_to_text(example_input)
            self.assertEqual(expected, actual)

    def test_with_utf_8(self):
        cases = {
            '😎 Cool': 'babad-zimav fadag kutoz bados',
        }
        for expected, example_input in cases.items():
            actual = proquabet.proquint_to_text(example_input)
            self.assertEqual(expected, actual)

    def test_random_punc(self):
        cases = [
            'Hello World!',
        ]
        for expected in cases:
            for i in range(25):
                random_punc_input = proquabet.text_to_proquint(expected, True)
                actual = proquabet.proquint_to_text(random_punc_input, True)
                self.assertEqual(expected, actual)


if __name__ == '__main__':
    unittest.main()
