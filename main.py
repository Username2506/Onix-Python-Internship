import re
from functools import reduce
from constants.general import (
    TEXT_PATH,
    SENTENCE_DELIMITERS,
    LOWER_CASE_LETTERS,
    UPPER_CASE_LETTERS,
    ASCII_ENGLISH_OFFSET,
    LETTERS_IN_ALPHABET
)


def transliterate(content):
    text = content
    for letter in UPPER_CASE_LETTERS.keys():
        text = text.replace(letter, UPPER_CASE_LETTERS[letter])
    text = text.lower()
    for letter in LOWER_CASE_LETTERS.keys():
        text = text.replace(letter, LOWER_CASE_LETTERS[letter])
    return text


def getMatrixWidth(array):
    lengths = list(map(lambda sentence: len(sentence.split(' ')), array))
    return max(lengths)


# count from 1
def getNumberFromWord(word):
    def reducer(a, b):
        index = ord(b) - ASCII_ENGLISH_OFFSET
        if index < 0 or index > LETTERS_IN_ALPHABET:  # check if symbol belongs to english alphabet
            index = 0
        return a + index

    return reduce(reducer, word, 0)


def transformSentence(sentence, width):
    matrixRow = []
    words = sentence.split(' ')
    for word in words:
        matrixRow.append(getNumberFromWord(word))
    matrixRow.extend([0] * (width - len(matrixRow)))
    return matrixRow


def getMatrix(array):
    matrixWidth = getMatrixWidth(array)
    matrix = []
    for sentence in array:
        matrix.append(transformSentence(sentence, matrixWidth))
    return matrix


def vectorizer(file):
    content = file.read()
    content = transliterate(content)
    sentences = re.split(SENTENCE_DELIMITERS, content)
    return getMatrix(sentences)


textFile = open(TEXT_PATH, encoding='utf-8')
print(vectorizer(textFile))
textFile.close()
