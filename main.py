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


if __name__ == '__main__':
    for line in sys.stdin:
        print(text_to_proquint(line, True))
