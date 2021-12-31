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
    binary_number = f'{number:016b}'
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
    if number > 65536:
        nums = [number // 65536, number & 0xffff]
    else:
        nums = [number]
    words = []
    for num in nums:
        letter = split_binary_number(num)
        word = LETTERS['consonants'][next(letter)]
        word += LETTERS['vowels'][next(letter)]
        word += LETTERS['consonants'][next(letter)]
        word += LETTERS['vowels'][next(letter)]
        word += LETTERS['consonants'][next(letter)]
        words.append(word)

    return '-'.join(words)


def encode_ascii_proquint(first_number: int, second_number: int) -> str:
    """ Converts numbers into proquint """
    big_number = first_number * (2 ** 8) + second_number
    letter = split_binary_number(big_number)
    word = LETTERS['consonants'][next(letter)]
    word += LETTERS['vowels'][next(letter)]
    word += LETTERS['consonants'][next(letter)]
    word += LETTERS['vowels'][next(letter)]
    word += LETTERS['consonants'][next(letter)]

    return word


def text_to_proquint(text: str) -> str:
    decoded_text = decode_text(text)
    output = ''
    i = 0
    while i < len(decoded_text):
        if i != len(decoded_text) - 1 and decoded_text[i] < 256 and decoded_text[i + 1] < 256:
            output += encode_ascii_proquint(decoded_text[i], decoded_text[i + 1]) + ' '
            i += 2
        else:
            output += encode_proquint(decoded_text[i]) + ' '
            i += 1
    return output.rstrip()
