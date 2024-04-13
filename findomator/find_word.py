"""
Objective: Automatize the research of word in text file
Creator: XenonEGG

using: python 3.6
encoding: utf-8
"""


def find_word(text: str, word: str) -> list:
    result = []
    n = len(text)
    size = len(word)
    for i in range(n - size + 1):
        cur_word = text[i:i + size]
        if cur_word == word:
            result.append(i)
    return result


def find_line_of_word(file_name: str, word: str) -> list:
    with open(file_name, "r", encoding="utf-8") as file:
        lines = file.readlines()

    index = []
    for i in range(len(lines)):
        line = lines[i]
        word_index = find_word(line, word)
        if len(word_index) > 0:
            index.append(i)

    return index


indexes = find_line_of_word("to_search.txt", "host")
print(indexes)
