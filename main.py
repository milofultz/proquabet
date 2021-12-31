from collections.abc import Iterator


LETTERS = {
    'consonants': [
        'b',
        'd',
        'f',
        'g',
        'h',
        'j',
        'k',
        'l',
        'm',
        'n',
        'p',
        'r',
        's',
        't',
        'v',
        'z',
    ],
    'vowels': [
        'a',
        'i',
        'o',
        'u',
    ]
}


def decode_text(chars: str) -> list:
    """ Converts string into list of UTF-8 codes """
    return [ord(char) for char in chars]


def split_binary_number(number: int) -> Iterator[int]:
    binary_number = f'{number:08b}'.zfill(16)
    state = 'consonant'

    while binary_number:
        if state == 'consonant':
            state = 'vowel'
            consonant, binary_number = int(binary_number[0:4], 2), binary_number[4:]
            yield consonant
        else:  # state == 'vowel'
            state = 'consonant'
            vowel, binary_number = int(binary_number[0:2], 2), binary_number[2:]
            yield vowel


def encode_proquint(number: int) -> str:
    """ Converts number into proquint """
    letter = split_binary_number(number)
    word = LETTERS['consonants'][next(letter)]
    word += LETTERS['vowels'][next(letter)]
    word += LETTERS['consonants'][next(letter)]
    word += LETTERS['vowels'][next(letter)]
    word += LETTERS['consonants'][next(letter)]
    return word
