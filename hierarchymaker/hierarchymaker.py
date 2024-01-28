"""
Objective: Make a hierarchy class representing the folder's hierarchy below a source path
Creator: XenonEGG

using: python 3.6
encoding: utf-8
"""

import os


class HierarchyMaker:
    def __init__(self, file_arrow: str = "--->", folder_arrow: str = ">   ", tab: str = "    "):
        """
        Make a list representing the folder's hierarchy and allow to print it with conditions
        """
        self.file_arrow = file_arrow
        self.folder_arrow = folder_arrow
        self.tab = tab

        self.hierarchy_list = []
        self.hierarchy_normalised_text = ""

    def update(self, source_path: str):
        """
        Update the hierarchy list using a source path representing the root folder
        """
        self.hierarchy_list.clear()
        self.hierarchy_list = ["folder", "root", []]
        make_hierarchy_list(source_path, self.hierarchy_list)

    def get_hierarchy_list(self, extension_allowed: list = None, file_name_allowed: list = None) -> list:
        """
        Return a copy of the hierarchy list filtered or not
        """
        if extension_allowed is None and file_name_allowed is None:
            return self.hierarchy_list.copy()
        if extension_allowed is not None and file_name_allowed is not None:
            raise ("Les filtres d'extension et de nom ne sont pas compatibles,"
                   "il faut choisir soit l'un soit l'autre")

        hierarchy_list_copy = self.hierarchy_list.copy()

        if extension_allowed is not None:
            extension_allowed = [e.replace(".", "") for e in extension_allowed]
            clean_hierarchy_list_extension(hierarchy_list_copy, extension_allowed)
        else:
            clean_hierarchy_list_file_name(hierarchy_list_copy, file_name_allowed)
        return hierarchy_list_copy

    def get_hierarchy_normalised_text(self, extension_allowed: list = None, file_name_allowed: list = None) -> str:
        """
        Return a text representing the folder's hierarchy, filtered or not
        """
        new_hierarchy_list = self.get_hierarchy_list(extension_allowed, file_name_allowed)
        self.make_hierarchy_normalised_text(new_hierarchy_list)
        return self.hierarchy_normalised_text

    def make_hierarchy_normalised_text(self, root: list, depth: int = 0):
        """
        Make a string representing the folder's hierarchy and store it in hierarchy_normalised_text
        """
        typ, name, lst = root
        if depth == 0:
            self.hierarchy_normalised_text += name + "\n"
        else:
            self.hierarchy_normalised_text += self.tab * (depth - 1) + self.folder_arrow + name + "\n"

        for e in lst:
            if e[0] == "file":
                self.hierarchy_normalised_text += self.tab * depth + self.file_arrow + e[1] + "\n"
            else:
                self.make_hierarchy_normalised_text(e, depth + 1)


def make_hierarchy_list(source_path: str, root: list):
    """
    Use a list hierarchy-normalised to store the hierarchy
    :source_path: The folder's path where the hierarchy begin
    :root: A list hierarchy-normalised : [type, name, list]
    """
    lib = os.listdir(source_path)
    sort_file_and_folder(lib, source_path)
    for file_name in lib:
        file_path = os.path.join(source_path, file_name)
        if os.path.isdir(file_path):
            root[-1].append(["folder", file_name, []])
            make_hierarchy_list(file_path, root[-1][-1])
        else:
            root[-1].append(["file", file_name])


def clean_hierarchy_list_extension(root: list, extension_allowed: list = None):
    """
    Clean the root using file extension
    :root: [list, name, [[file, name], [list, name, []], [file, name]]]
    """
    i = 0
    while i < len(root[-1]):
        """
        root[-1] = list
        root[-1][i] = i-ème fichier
        root[-1][i][0] = type du i-ème fichier
        """
        typ = root[-1][i][0]
        if typ == "file":
            typ, file_name = root[-1][i]
            extension = file_name.split(".")[-1]
            if extension not in extension_allowed:
                root[-1].pop(i)
                i -= 1
        else:
            clean_hierarchy_list_extension(root[-1][i], extension_allowed)  # list in the i-ème element
            if len(root[-1][i][-1]) == 0:
                root[-1].pop(i)
                i -= 1
        i += 1


def clean_hierarchy_list_file_name(root: list, file_name_allowed: list = None):
    """
    Clean the root using file name
    :root: [list, name, [[file, name], [list, name, []], [file, name]]]
    """
    i = 0
    while i < len(root[-1]):
        """
        root[-1] = list
        root[-1][i] = i-ème fichier
        root[-1][i][0] = type du i-ème fichier
        """
        typ = root[-1][i][0]
        if typ == "file":
            typ, file_name = root[-1][i]
            if file_name not in file_name_allowed:
                root[-1].pop(i)
                i -= 1
        else:
            clean_hierarchy_list_file_name(root[-1][i], file_name_allowed)  # list in the i-ème element
            if len(root[-1][i][-1]) == 0:
                root[-1].pop(i)
                i -= 1
        i += 1


def find_file_with_name(path: str, name: str):
    """
    Try to find a file using its name
    Return the absolute path of the targeted file
    """
    lib = os.listdir(path)
    if len(lib) == 0:
        return None

    for file_name in lib:
        file_path = os.path.join(path, file_name)
        if name == file_name:
            return file_path
        if os.path.isdir(file_path):
            res = find_file_with_name(file_path, name)
            if res is not None:
                return res
    return None


def sort_file_and_folder(lib: list, path: str):
    i = 0
    time = 0
    while i < len(lib) and time < len(lib) * 2:
        e = lib[i]
        file_path = os.path.join(path, e)
        lib.pop(i)
        if os.path.isdir(file_path):
            lib.append(e)
            i -= 1
        else:
            lib.insert(0, e)
        i += 1
        time += 1


"""
source = os.path.abspath("../..")
h = HierarchyMaker()

h.update(source)
x = h.get_hierarchy_normalised_text()

with open("hierarchy.txt", "w", encoding="utf-8") as file:
    file.write(x)
"""
