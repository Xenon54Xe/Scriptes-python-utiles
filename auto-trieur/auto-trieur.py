import os


"""
Variables globales
"""

# __file__ est le chemin absolu du script
_program_name = __file__.split("\\")[-1:][0]
_ref_board_name = "reference.ods"

_abs_path = os.path.abspath("")
_files = os.listdir(_abs_path)

_filters = []


def get_word_index(word: str, text: str) -> int:
    """
    Renvoit l'index du mot dans le texte, -1 s'il n'y est pas
    :param word:
    :param text:
    :return:
    """
    for i in range(len(text)):
        if text[i:i + len(word)] == word:
            return i
    return -1


def is_word_in_text(word: str, text: str) -> bool:
    """
    Renvoit True si le mot est dans le texte, False sinon
    :param word:
    :param text:
    :return:
    """
    if get_word_index(word, text) != -1:
        return True
    return False


def sort_list(old_list: list[int], croissant=True) -> list[int]:
    new_list = []
    for num in old_list:
        if len(new_list) == 0:
            new_list.append(num)
            continue

        index = 0
        if croissant:
            while index < len(new_list) and num > new_list[index]:
                index += 1
        else:
            while index < len(new_list) and num < new_list[index]:
                index += 1
        new_list.insert(index, num)
    return new_list


def sort_dictionary(old_dict: dict, croissant=True) -> dict:
    old_keys = []
    for old_key in old_dict.keys():
        old_keys.append(old_key)

    new_keys = sort_list(old_keys, croissant)

    new_dict = {}
    for new_key in new_keys:
        new_dict[new_key] = old_dict[new_key]
    return new_dict


def start():
    """
    Fonction principale
    :return:
    """

    if _ref_board_name not in _files:
        print(f"/!\\ Le fichier '{_ref_board_name}' est introuvable et le programme ne peut donc pas fonctionner.")
        return

    # enlève le fichier reference.csv, ce fichier et les dossiers des fichiers à trier
    _files.remove(_program_name)
    _files.remove(_ref_board_name)
    for file in _files:
        if os.path.isdir(file):
            _files.remove(file)

    if len(_files) == 0:
        print("Il n'y a pas de fichiers à trier")
        return

    print("Files to sort:")
    print(_files)

    """
    Récupération des filtres et triage dans l'ordre décroissant de la taille
    """
    dict_size_filters = {}
    with open(_ref_board_name, "r") as file:
        lines = file.readlines()
        for num in range(1, len(lines)):  # regarde dans toutes les lignes sauf la première
            line = lines[num]
            component = line.split("\t")
            current_filter = component[0]
            if current_filter != "":
                size = len(current_filter)
                """
                Range les filtres en fonction de leur tailles dans le dictionnaire
                """
                try:
                    dict_size_filters[size].append(current_filter)
                except:
                    dict_size_filters[size] = [current_filter]
        file.close()
    sorted_filters = sort_dictionary(dict_size_filters, False)

    if len(dict_size_filters) == 0:
        print("Il n'y a pas de filtres")

    """
    Met les filtres dans _filters
    """
    for sorted_filter in sorted_filters.items():
        filter_list = sorted_filter[1]
        for current_filter in filter_list:
            _filters.append(current_filter)

    print("Filters :")
    print(_filters)

    """
    Filtration des fichiers
    """
    for num in range(len(_files)):
        file = _files[num]
        print("///// " + file)

        """
        Récupération des filtres du fichier
        """
        present_filters = []
        for main_filter in _filters:
            if is_word_in_text(main_filter, file):
                present_filters.append(main_filter)

        if len(present_filters) == 0:
            print(f"Il n'y a pas de filtres dans {file}")
            continue

        """
        Récupère les filtres dans l'ordre de leur apparition
        """
        index = 0
        sorted_file_filters = []
        while index < len(file):
            found = False
            for main_filter in present_filters:
                if main_filter == file[index:index + len(main_filter)]:
                    sorted_file_filters.append(main_filter)
                    index += len(main_filter)
                    found = True
                    break
            if not found:
                index += 1

        path = _abs_path
        for current_file_filter in sorted_file_filters:
            path += f"\\{current_file_filter}"

        if os.path.exists(path) and os.path.isdir(path):
            old_path = f"{_abs_path}\\{file}"
            new_path = f"{path}\\{file}"
            os.rename(old_path, new_path)


with open(_ref_board_name, "r", encoding="cp437") as file:
    lines = file.readlines()
    print(lines)
    text = ""
    for line in lines:
        text += line
    print(text)