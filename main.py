from collections.abc import Iterator
from random import randint
import sys


PUNCTUATION = '!.?,:;'
CONSONANTS = [
    'b', 'd', 'f', 'g',
    'h', 'j', 'k', 'l',
    'm', 'n', 'p', 'r',
    's', 't', 'v', 'z',
]
VOWELS = [
    'a', 'i',
    'o', 'u',
]


def decode_text(chars: str) -> list:
    """ Converts string into list of UTF-8 codes """
    return [ord(char) for char in chars]


def encode_text(numbers: list[int]) -> str:
    """ Converts list of numbers into a UTF-8 string """
    return ''.join(chr(num) for num in numbers)


def split_binary_number(number: int) -> Iterator[int]:
    binary_number = f'{number:016b}'
    is_consonant = True

    while binary_number:
        if is_consonant:
            consonant, binary_number = int(binary_number[0:4], 2), binary_number[4:]
            yield consonant
        else:  # state == 'vowel'
            vowel, binary_number = int(binary_number[0:2], 2), binary_number[2:]
            yield vowel

        is_consonant = not is_consonant


def compile_binary_number(numbers: list[int]) -> int:
    binary_number = ''

    while numbers:
        binary_number += f'{numbers.pop(0):04b}'
        binary_number += f'{numbers.pop(0):02b}'
        binary_number += f'{numbers.pop(0):04b}'
        binary_number += f'{numbers.pop(0):02b}'
        binary_number += f'{numbers.pop(0):04b}'

    return int(binary_number, 2)


def encode_proquint(number: int) -> str:
    """ Converts number into proquint """
    nums = [number]
    if number > 65536:
        nums = [number // 65536, number & 0xffff]
    words = []
    for num in nums:
        letter = split_binary_number(num)
        word = CONSONANTS[next(letter)]
        word += VOWELS[next(letter)]
        word += CONSONANTS[next(letter)]
        word += VOWELS[next(letter)]
        word += CONSONANTS[next(letter)]
        words.append(word)

    return '-'.join(words)


def decode_proquint(word: str) -> int:
    """ Converts a proquint into a number """
    word = list(word.replace('-', ''))  # If 32-bit UTF-8
    nums = []

    while word:
        nums.append(CONSONANTS.index(word.pop(0)))
        nums.append(VOWELS.index(word.pop(0)))
        nums.append(CONSONANTS.index(word.pop(0)))
        nums.append(VOWELS.index(word.pop(0)))
        nums.append(CONSONANTS.index(word.pop(0)))

    return compile_binary_number(nums)


def text_to_proquint(text: str, random_punc: bool = False) -> str:
    decoded_text = decode_text(text)

    output = ''
    i = 0
    capitalize = True
    start = True

    while i < len(decoded_text):
        if not start and random_punc:
            if randint(0, 12) == 6:
                output += PUNCTUATION[randint(3, len(PUNCTUATION) - 1)]
            elif randint(0, 12) == 7:
                output += PUNCTUATION[randint(0, 2)]
                capitalize = True
            elif randint(0, 25) == 7:
                output += PUNCTUATION[randint(0, 2)] + '\n\n'
                capitalize = True
                start = True

        if i != len(decoded_text) - 1 and decoded_text[i] < 256 and decoded_text[i + 1] < 256:
            current_letter = decoded_text[i] * (2 ** 8) + decoded_text[i + 1]
            i += 1
        else:
            current_letter = decoded_text[i]

        new_word = encode_proquint(current_letter)
        i += 1

        if not start:
            output += ' '
        else:
            start = False

        if random_punc and capitalize:
            new_word = new_word.capitalize()
            capitalize = False
        output += new_word

    output = output.rstrip()
    if random_punc:
        output += PUNCTUATION[randint(0, 2)]
    return output


def proquint_to_text(raw_proquints: str) -> str:
    proquints = raw_proquints.split(' ')

    output = ''

    for word in proquints:
        if len(word) == 5:
            decoded = decode_proquint(word)
            b = f'{decoded:016b}'
            first, second = int(b[:8], 2), int(b[8:], 2)
            output += decode_nums([first, second])
        else:
            decoded = decode_proquint(word)
            output += decode_nums([decoded])

    return output.replace('\x00', '')  # Remove hanging ASCII chars with no pair


if __name__ == '__main__':
    for line in sys.stdin:
        print(text_to_proquint(line, True))
