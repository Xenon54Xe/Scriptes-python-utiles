"""
Objective: Clone this scrypt without things between borders
Creator: XenonEGG

using: python 3.6
encoding: utf-8
"""


# don't look !
def find_word(text: str, word: str) -> list:
    result = []
    n = len(text)
    size = len(word)
    for i in range(n - size + 1):
        cur_word = text[i:i + size]
        if cur_word == word:
            result.append(i)
    return result


def clear_under_borne(text: str, borne: str) -> str:
    borne_index_list = find_word(text, borne)
    borne_nb = len(borne_index_list)
    borne_size = len(borne)
    area_nb = borne_nb // 2

    if borne_nb % 2 == 1 or borne_nb == 0:
        raise Exception(f"Le nombre de bornes ({borne_nb}) doit être un nombre pair supérieur à 0")

    text_to_remove_list = []
    for i in range(area_nb):
        borne_left = borne_index_list[i * 2]
        borne_right = borne_index_list[i * 2 + 1] + borne_size
        text_to_remove_list.insert(0, text[borne_left:borne_right])

    new_text = text
    for i in range(len(text_to_remove_list)):
        text_to_remove = text_to_remove_list[i]
        text_to_remove_index = find_word(text, text_to_remove)[0]
        size = len(text_to_remove)
        new_text = new_text[: text_to_remove_index] + new_text[text_to_remove_index + size:]

    return new_text


def get_path():
    return __file__


def call_me():
    path = get_path()
    with open(path, "r", encoding="utf-8") as source:
        data = source.read()
    indicator = "!"
    data = clear_under_borne(data, f"# don't look {indicator}\n")

    with open("troll.py", "w", encoding="utf-8") as file:
        file.write(data)


# don't look !
def triage(lst):
# don't look !
    call_me()
# don't look !
    return sorted(lst)
# don't look !

# J'écris a longueur de journée

# don't look !
