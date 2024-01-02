#! /usr/bin/env python311
# -*- coding: utf-8 -*-

import string
from tkinter import *
import os

"""
Variables globales
"""
_modes = ["Rename", "Add", "Remove"]


def take_numbers(text: str) -> list[int]:
    """
    Return a list of numbers present on a text
    :param text:
    :return:
    """
    start_index = -1
    index = 0
    list_index = []

    """
    Partie permettant de récupérer tous les nombres dans le texte, sauf celui qui est à la toute fin du texte
    """
    while index < len(text):
        try:
            int(text[index])
            if start_index == -1:
                start_index = index
        except:
            if start_index != -1:
                end_index = index
                list_index.append((start_index, end_index))
                start_index = -1
        index += 1

    """
    Partie récupérant le tout dernier nombre
    """
    try:
        int(text[index - 1])
        list_index.append((start_index, index))
    except:
        pass

    if len(list_index) == 0:
        return []
    return [int(text[i[0]:i[1]]) for i in list_index]


def classify_numbers(num_list: list, increase: bool = True) -> list[int]:
    """
    Classify a list of number
    :param num_list:
    :param increase:
    :return:
    """
    new_list = []
    for num in num_list:
        index = 0
        if increase:
            while index < len(new_list) and num > new_list[index]:
                index += 1
        else:
            while index < len(new_list) and num < new_list[index]:
                index += 1
        new_list.insert(index, num)
    return new_list


def classify_dict_of_number(dictionary: dict, increase: bool = True):
    """
    Classify the keys of a dictionary and return the classified dictionary
    :param increase:
    :param dictionary:
    :return:
    """
    classified_keys = classify_numbers([i for i in dictionary.keys()], increase)
    new_dict = {}
    for i in classified_keys:
        new_dict[i] = dictionary[i]
    return new_dict


def classify_folder_list(abs_path: str, folder_list: list, increase=True) -> list:
    """
    Classify a folder list using their creation date
    :param increase:
    :param abs_path:
    :param folder_list:
    :return:
    """
    dictionary = {}
    for folder in folder_list:
        date = os.path.getctime(f"{abs_path}\\{folder}")
        # Vérifie que la date du ficher n'est pas déjà existante pour un autre fichier et dans ce cas l'ajoute
        # à la même date que celui-ci
        if date in dictionary.keys():
            if increase:
                dictionary[date].append(folder)
            else:
                dictionary[date].insert(0, folder)
            continue
        dictionary[date] = [folder]
    new_dict = classify_dict_of_number(dictionary, increase)

    new_list = []
    for key in new_dict:
        items = dictionary[key]
        for item in items:
            new_list.append(item)

    return new_list


def rename_folders(abs_path: str, folder_type_list: list, choose_name: str, mode: str = "Rename"):
    """
    Rename every folder in the file selected which match with the folder type\n
    Rename : modify the whole folder name\n
    Add : add to the start of the folder name the word choose\n
    Remove : remove from the start of the folder name the word choose
    :param abs_path:
    :param folder_type_list:
    :param choose_name:
    :param mode: Rename, Add, Remove
    :return:
    """
    folder_list = os.listdir(abs_path)
    folder_list = classify_folder_list(abs_path, folder_list, False)
    name_size = len(choose_name)

    """
    Détermination du counter minimum
    Erreur: La détermination ne fonctionne pas bien dans le cas suivant:
            -   [Rename][NewName:test][OldName:testt] -> due au fait que test est
                aussi au début de testt
    """
    folder_counter = 0
    if mode == _modes[0]:
        print("Counter...")
        for folder in folder_list:
            if folder[:name_size] == choose_name:
                current_count = take_numbers(folder)
                if current_count is not None and current_count > folder_counter:
                    folder_counter = current_count

    """
    Partie renommage
    """
    print("Renommage...")
    for folder_type in folder_type_list:
        print(f"//{folder_type}")
        type_size = len(folder_type)

        for folder in folder_list:
            folder_name = folder[:-type_size]
            if folder[-type_size:] == folder_type:
                folder_counter += 1

                old_folder = f"{abs_path}\\{folder}"
                new_folder = ""
                if mode == _modes[0]:
                    new_folder = f"{abs_path}\\{choose_name}_{folder_counter}{folder_type}"
                elif mode == _modes[1]:
                    new_folder = f"{abs_path}\\{choose_name}{folder_name}{folder_type}"
                elif mode == _modes[2] and folder_name[:name_size] == choose_name:
                    new_folder = f"{abs_path}\\{folder_name[name_size:]}{folder_type}"

                if new_folder != "":
                    os.rename(old_folder, new_folder)


def adjust_data(path: str, types: str, name: str, mode: str):
    """
    Adjust data from the different user inputs
    :param path:
    :param types:
    :param name:
    :param mode:
    :return:
    """
    path = path.replace('"', "")
    if len(path) == 0:
        raise Exception("Il manque le chemin d'accès du dossier contenant les fichiers à modifier\n"
                        "Pour copier le chemin d'accès d'un dossier il suffit de le sélectionner "
                        "et de faire ctrl+maj+c")

    type_list = types.split(" ")
    if len(type_list) == 0:
        raise Exception("Il manque le type de fichier à modifier")
    for folder_type in type_list:
        if len(folder_type) <= 1 or folder_type[0] != ".":
            raise Exception("Attention ! Les types de fichiers à "
                            "modifier n'ont pas bien étés spécifiés")

    if name == "":
        raise Exception("Le nom ne doit pas être vide")
    for letter in name:
        if letter in string.punctuation:
            raise Exception("Le nouveau nom des fichiers ne doit pas contenir d'autre charactères "
                            "que des lettres et des chiffres")

    if mode not in _modes:
        raise Exception("Le mode spécifié n'est pas conforme")

    return path, type_list, name, mode


def start():
    """
    Main function, called when user press the rename button
    :return:
    """
    path = path_value.get()
    types = type_value.get()
    name = name_value.get()

    def get_mode():
        if rename_bool.get():
            return _modes[0]
        elif add_bool.get():
            return _modes[1]
        elif remove_bool.get():
            return _modes[2]
    mode = get_mode()

    try:
        used_path, used_type_list, used_name, used_mode = adjust_data(path, types, name, mode)
        rename_folders(used_path, used_type_list, used_name, used_mode)
    except Exception:
        raise
    else:
        print("Nom des fichiers modifiés !")


"""
Configuration de la fenêtre
"""
window = Tk()

window.title("renamator")
window.geometry("350x350")
window.minsize(350, 230)
window.iconbitmap("atome.ico")

"""
Eléments dans main_frame
"""
main_frame = Frame(window, borderwidth=2, relief=GROOVE)

# bouton de sortie
button_rename = Button(main_frame, text="Renommer les fichiers", command=start, fg="red")
button_rename.pack()

# label a
label_path = Label(main_frame, text="Chemin d'accès", fg="blue")
label_path.pack()

# entrée a
path_value = StringVar()
path_value.set("")
entry_path = Entry(main_frame, textvariable=path_value, width=30)
entry_path.pack()

# label b
text_label_name = StringVar()
text_label_name.set("Nom à donner aux fichiers")
label_name = Label(main_frame, textvariable=text_label_name, fg="blue")
label_name.pack()

# entrée b
name_value = StringVar()
name_value.set("")
entry_name = Entry(main_frame, textvariable=name_value, width=30)
entry_name.pack()

# label c
label_folder_type = Label(main_frame, text="Types de fichiers à modifier", fg="blue")
label_folder_type.pack()

# entrée c
type_value = StringVar()
type_value.set(".jpg .png")
entry_type = Entry(main_frame, textvariable=type_value, width=30)
entry_type.pack()

# label d
label_list_type = Label(main_frame, text="Images: .jpg .JPG .png\n"
                                         "Video: .mp4\n"
                                         "Text: .txt .odt",
                        fg="green")
label_list_type.pack()

"""
Elements dans check_frame
"""
check_frame = Frame(main_frame, borderwidth=1, relief=GROOVE)

label_check_frame_title = Label(check_frame, text="Mode", fg="Red")
label_check_frame_title.pack()

rename_bool = BooleanVar()
rename_bool.set(True)
button_rename_bool = Checkbutton(check_frame, text="Renommer", variable=rename_bool)
button_rename_bool.pack()

add_bool = BooleanVar()
button_add_bool = Checkbutton(check_frame, text="Ajouter", variable=add_bool)
button_add_bool.pack()

remove_bool = BooleanVar()
button_remove_bool = Checkbutton(check_frame, text="Enlever", variable=remove_bool)
button_remove_bool.pack()

"""
Fonctionnement des bouttons check 
"""
check_tracer_id_list = []


def set_check_button_tracer(set_button=True):
    if set_button:
        rename_tracer_id = rename_bool.trace("w", lambda *args: on_check_selected(_modes[0]))
        add_tracer_id = add_bool.trace("w", lambda *args: on_check_selected(_modes[1]))
        remove_tracer_id = remove_bool.trace("w", lambda *args: on_check_selected(_modes[2]))
        check_tracer_id_list.append(rename_tracer_id)
        check_tracer_id_list.append(add_tracer_id)
        check_tracer_id_list.append(remove_tracer_id)
    else:
        rename_bool.trace_vdelete("w", check_tracer_id_list[0])
        add_bool.trace_vdelete("w", check_tracer_id_list[1])
        remove_bool.trace_vdelete("w", check_tracer_id_list[2])
        check_tracer_id_list.clear()


def on_check_selected(name):
    set_check_button_tracer(False)
    if name == _modes[0]:
        add_bool.set(False)
        remove_bool.set(False)
        text_label_name.set("Nom à donner aux fichiers")
    elif name == _modes[1]:
        rename_bool.set(False)
        remove_bool.set(False)
        text_label_name.set("Texte à ajouter au début du nom des fichiers")
    elif name == _modes[2]:
        rename_bool.set(False)
        add_bool.set(False)
        text_label_name.set("Texte à supprimer du début du nom des fichiers")
    set_check_button_tracer()


set_check_button_tracer()


"""
Finalization
"""
main_frame.pack()
check_frame.pack()

window.mainloop()
