"""
Le but est de créer un cheval de troie qui, lorsque ce fichier sera appelé,
créera un fichier nommé correction.py dont la partie infectée doit rester invisible
"""


# don't look !
def occurences(text, mot):
    lst = []
    for i in range(len(text) - len(mot) + 1):
        e = text[i:i+len(mot)]
        if e == mot:
            lst.append(i)
    return lst


def vire_borne(text, borne):
    index_list = occurences(text, borne)
    nb_borne = len(index_list)

    if nb_borne % 2 != 0 or nb_borne == 0:
        raise Exception(f"Le nombre de bornes ({nb_borne}) doit être un nombre pair supérieur à 0")

    if nb_borne == 2:
        a, b = index_list[0], index_list[1]
        return text[:a-1] + text[b + len(borne) + 1:]

    new_text = ""
    a, b = 0, index_list[0]
    to_add = text[a:b-1]
    new_text += to_add

    nb_trunc = nb_borne // 2
    for i in range(0, nb_trunc - 1):
        print(i)
        a, b = index_list[i * 2 + 1], index_list[i * 2 + 2]
        to_add = text[a + len(borne):b-1]
        new_text += to_add

    a, b = index_list[-1], len(text)
    to_add = text[a + len(borne):b]
    new_text += to_add

    return new_text


def appelle_moi():
    with open("clonator.py", "r", encoding="utf-8") as source:
        data = source.read()
    deli = "!"
    data = vire_borne(data, f"# don't look {deli}")
    print(data)
    with open("troll.py", "w", encoding="utf-8") as file:
        file.write(data)


# don't look !
def triage(L):
# don't look !
    appelle_moi()
# don't look !
    return sorted(L)


x = triage([1, 5, 6, 2, 8, 0])
print(x)
# don't look !
"""
J'écris des conneries a longueur de journée
"""
# don't look !
