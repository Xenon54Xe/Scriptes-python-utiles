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

    def get_hierarchy_list(self, filter_dict: dict = None) -> list:
        """
        Return a copy of the hierarchy list filtered or not, the filters need to be a dictionary like this:

        {
        extension: (white_list: True or False, filters: []),
        file_name: (white_list: True or False, filters: []),
        folder_name: (white_list: True or False, filters: [])
        }
        """
        if filter_dict is None:
            return self.hierarchy_list.copy()

        hierarchy_list_copy = self.hierarchy_list.copy()

        for filter_type in filter_dict.keys():
            white_list, filters = filter_dict[filter_type]
            if filter_type == "extension":
                filters = [e.replace(".", "") for e in filters]
            clean_hierarchy_list(hierarchy_list_copy, filter_type, filters, white_list)

        return hierarchy_list_copy

    def get_hierarchy_normalised_text(self, filter_dict: dict = None) -> str:
        """
        Return a text representing the folder's hierarchy, filtered or not
        """
        new_hierarchy_list = self.get_hierarchy_list(filter_dict)
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


def clean_hierarchy_list(root: list, filter_type: str, filters: list, white_list: bool = True):
    """
    Clean the root using filters
    :root: hierarchy-normalised list
    """
    i = 0
    while i < len(root[-1]):
        """
        root[-1] = list
        root[-1][i] = i-ème fichier
        root[-1][i][0] = type du i-ème fichier
        """
        typ = root[-1][i][0]
        if filter_type in ["extension", "file_name"]:
            if typ == "file":
                typ, file_name = root[-1][i]
                extension = file_name.split(".")[-1]
                if filter_type == "extension" and (white_list and extension not in filters or
                                                   not white_list and extension in filters)\
                        or filter_type == "file_name" and (white_list and file_name not in filters or
                                                           not white_list and file_name in filters):
                    root[-1].pop(i)
                    i -= 1
            else:
                clean_hierarchy_list(root[-1][i], filter_type, filters, white_list)  # list in the i-ème element
                if len(root[-1][i][-1]) == 0:
                    root[-1].pop(i)
                    i -= 1
        elif filter_type == "folder_name":
            if typ == "folder":
                typ, folder_name, lst = root[-1][i]
                if white_list and folder_name not in filters or not white_list and folder_name in filters:
                    root[-1].pop(i)
                    i -= 1
                else:
                    clean_hierarchy_list(root[-1][i], filter_type, filters, white_list)  # list in the i-ème element
        i += 1


def clean_hierarchy_list_folder_name(root: list, folder_name_list: list, white_list: bool = False):
    """
    Clean the root using folder name
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
        if typ == "folder":
            typ, folder_name, lst = root[-1][i]
            if white_list and folder_name not in folder_name_list or not white_list and folder_name in folder_name_list:
                root[-1].pop(i)
                i -= 1
            else:
                clean_hierarchy_list_folder_name(root[-1][i], folder_name_list)  # list in the i-ème element
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
filter_dict = {
    "extension": (False, []),
    "file_name": (True, ["main"]),
    "folder_name": (False, [])
}
x = h.get_hierarchy_normalised_text(filter_dict)

with open("hierarchy.txt", "w", encoding="utf-8") as file:
    file.write(x)
"""
