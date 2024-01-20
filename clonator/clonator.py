"""
Le but est de créer un cheval de troie qui, lorsque ce fichier sera appelé, créera un fichier nommé correction.py
dont la partie infectée doit rester invisible
"""
# voicicommentcréerunefonction!


def remove_text(text, simili_borne):
    """
    La borne considérée est la simili_borne + !
    """
    borne = simili_borne + "!"
    nb, size = len(text), len(borne)

    index = -1
    index_list = []
    for i in range(nb - size + 1):
        part = text[i: i + size]
        if index == -1 and part == borne:
            index = i
            index_list.append(i)
        elif part == borne:
            index = -1
            index_list.append(i + size + 1)

    if len(index_list) % 2 != 0 or len(index_list) == 0:
        raise Exception(f"Le nombre de bornes ({len(index_list)}) doit être un nombre pair supérieur à 0")

    if len(index_list) == 2:
        a, b = index_list[0], index_list[1]
        return text[:a] + text[b:]

    new_text = ""
    for i in range(len(index_list) - 1):
        if i == 0:
            a = 0
            b = index_list[0]
        elif 0 < i * 2 < len(index_list):
            a = index_list[i * 2 - 1]
            b = index_list[i * 2]
        else:
            a = index_list[len(index_list) - 1]
            b = len(text) + 1
        new_text += text[a:b]

    return new_text


def appelle_moi():
    with open("correction.py", "w", encoding="utf-8") as file:
        with open("clonator.py", "r", encoding="utf-8") as source:
            text = source.read()
            text = remove_text(text, "# voicicommentcréerunefonction")
        file.write(str(text))


# voicicommentcréerunefonction!


def triage(L):
    # voicicommentcréerunefonction!
    appelle_moi()
    # voicicommentcréerunefonction!
    return sorted(L)


x = triage([1, 5, 6, 2, 8, 0])
print(x)
# voicicommentcréerunefonction!
"""
J'écris des conneries a longueur de journée
"""
# voicicommentcréerunefonction!
