'''
Module for normalizing and fixing OCR mistakes
'''


def normalize_word(word: str):
    '''
    Takes recognized word and cleans it.
    Removes trailing comma sign if exists
    and performs OCR mistakes normalization
    '''
    if not isinstance(word, str):
        return word

    normalized_word = word

    if normalized_word[-1] == ',':
        normalized_word = normalized_word[0:-1]

    return normalize_ocr_mistakes(normalized_word)


def normalize_ocr_mistakes(word: str):
    '''
    Takes recognized word and cleans it.
    Replaces long "s" to short "s" (for Fraktur)
    and replaces 'ift' with 'ist'
    '''
    if not isinstance(word, str):
        return ''

    if 'ift' in word:
        return 'ist'

    normalized_word = word

    normalized_word = normalized_word.replace('ſ', 's')

    return normalized_word
