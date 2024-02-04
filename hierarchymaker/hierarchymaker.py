"""
Objective: Make a hierarchy class representing the folder's hierarchy below a source path
Creator: XenonEGG

using: python 3.6
encoding: utf-8
"""

import os


class HierarchyMaker:
    def __init__(self, source_path: str,  file_arrow: str = "--->", folder_arrow: str = ">   ", tab: str = "    "):
        """
        Make a list representing the folder's hierarchy and allow to get it or its representative string filtered or not

        Step:
            - update(source_path) iterate over every folder in the root folder
            - get_hierarchy_list(filter_dict) -> get the list filtered or not
            - get_hierarchy_normalised_text(filter_dict) -> get the string representing the list
        """
        self.file_arrow = file_arrow
        self.folder_arrow = folder_arrow
        self.tab = tab

        self.source_path = None
        self.source_name = None
        self.hierarchy_list = []
        self.hierarchy_normalised_text = ""

        self.depth = 0
        self.entity_count = 1
        self.path_list = []

        self.update(source_path)

    def update(self, source_path: str):
        """
        Update the hierarchy list using a source path representing the root folder
        """
        self.source_path = source_path
        source_name = os.path.split(source_path)[-1]
        self.source_name = source_name
        self.hierarchy_list.clear()
        self.hierarchy_list = ["list", source_name, 0, source_path, []]
        self.make_hierarchy_list(source_path, self.hierarchy_list)

    def get_hierarchy_list(self, filter_dict: dict = None) -> list:
        """
        Return the list representing the folder's hierarchy filtered or not

        filter_dict (dictionary):
            - keys : 'extension', 'file_name', 'folder_name'
            - value: a tuple representing filter data:
            1 allowing type (like a white list) : 'black' ('b') or 'white' ('w')
            2 a list of string (representing filtered words)
        """

        if filter_dict is None:
            return self.hierarchy_list.copy()

        hierarchy_list_copy = self.hierarchy_list.copy()

        filter_type_order = ("folder_name", "file_name", "extension", "depth")
        for filter_type in filter_type_order:
            if filter_type not in filter_dict.keys():
                continue
            if filter_type == "depth":
                continue

            allowing_filter_type, filter_strings = filter_dict[filter_type]
            if allowing_filter_type not in ("white", "black", "w", "b"):
                raise "Its needed to choose between white (w) or black (b) in the allowing filter type"

            if allowing_filter_type in ("white", "w"):
                white_list = True
            else:
                white_list = False

            if filter_type == "extension":
                filter_strings = [e.replace(".", "") for e in filter_strings]

            if len(filter_strings) != 0:
                clean_hierarchy_list(hierarchy_list_copy, filter_type, filter_strings, white_list)
        return hierarchy_list_copy

    def get_hierarchy_normalised_text(self, filter_dict: dict = None) -> str:
        """
        Return a string representing the folder's hierarchy, filtered or not

        filter_dict (dictionary):
            - keys : 'extension', 'file_name', 'folder_name'
            - value: a tuple representing filter data:
            1 allowing type (like a white list) : 'black' ('b') or 'white' ('w')
            2 a list of string (representing filtered words)
        """
        new_hierarchy_list = self.get_hierarchy_list(filter_dict)
        self.make_hierarchy_normalised_text(new_hierarchy_list)
        return self.hierarchy_normalised_text

    def get_depth(self):
        return self.depth

    def get_entity_count(self):
        return self.entity_count

    def get_entities_path(self, filter_type: str, filters: list):
        pass

    def make_hierarchy_list(self, source_path: str, root: list, depth: int = 1):
        """
        Use hierarchy-normalised list to store the folder's hierarchy

        source_path: The folder's path where the hierarchy begin
        root: A list hierarchy-normalised : [type, name, depth, path, list] (type = 'list' or 'file')
        """
        lib = os.listdir(source_path)
        sort_file_and_folder(lib, source_path)
        if depth == 1:
            self.entity_count = 1
            self.depth = 0
        self.entity_count += len(lib)

        if self.depth < depth:
            self.depth = depth

        for file_name in lib:
            file_path = os.path.join(source_path, file_name)
            if os.path.isdir(file_path):
                root[-1].append(["folder", file_name, depth, file_path, []])
                self.make_hierarchy_list(file_path, root[-1][-1], depth + 1)
                # root[-1][-1] = list in the last element of the root
            else:
                root[-1].append(["file", file_name, depth, file_path])

    def make_hierarchy_normalised_text(self, root: list, depth: int = 0):
        """
        Make a string representing the folder's hierarchy and store it in hierarchy_normalised_text
        """
        typ, name, e_depth, e_path, lst = root
        if depth == 0:
            self.hierarchy_normalised_text += name + "\n"
        else:
            self.hierarchy_normalised_text += self.tab * (depth - 1) + self.folder_arrow + name + "\n"

        for e in lst:
            if e[0] == "file":
                self.hierarchy_normalised_text += self.tab * depth + self.file_arrow + e[1] + "\n"
            else:
                self.make_hierarchy_normalised_text(e, depth + 1)


def split_path(cut: str, path: str):
    nl = []
    while os.path.split(path)[-1] != "":
        x, y = os.path.split(path)
        nl.insert(0, y)
        if y == cut:
            return nl
        path = x
    return nl


def inserter(root: list, target_folders: list, entity_data: list):
    current_target_name = target_folders.pop(0)
    typ, name, depth, path, lst = root
    print(root)
    print(current_target_name)
    print(target_folders)
    print("")
    if len(root[-1]) == 0 and len(target_folders) > 0:
        used_path = os.path.join(path, current_target_name)
        root[-1].append(["list", current_target_name, depth + 1, used_path, []])
        inserter(root[-1][-1], target_folders, entity_data)
    elif len(root[-1]) == 0 and len(target_folders) == 0:
        root[-1].append(entity_data)
    else:
        found = False
        for i in range(len(root[-1])):
            entity = root[-1][i]
            e_typ = entity[0]
            if e_typ == "list":
                e_typ, e_name, e_depth, e_path, e_lst = entity
                if e_name == current_target_name and len(target_folders) > 0:
                    used_path = os.path.join(path, current_target_name)
                    root[-1][i][-1].append(["list", current_target_name, e_depth + 1, used_path, []])
                    inserter(root[-1][i][-1][-1], target_folders, entity_data)
                    found = True
                elif e_name == current_target_name and len(target_folders) == 0:
                    root[-1][i][-1].append(entity_data)
                    found = True
        if not found and len(target_folders) == 0:
            root[-1].append(entity_data)
        elif not found and len(target_folders) > 0:
            used_path = os.path.join(path, current_target_name)
            root[-1].append(["list", current_target_name, depth + 1, used_path, []])
            inserter(root[-1][-1], target_folders, entity_data)


def convert_path_list_to_hierarchy_list(global_root_path: str, path_list: list) -> list:
    global_root_name = os.path.split(global_root_path)[-1]
    hierarchy_list = ["list", global_root_name, 0, global_root_path, []]
    for i in range(len(path_list)):
        current_path = path_list[i]
        target_folders = split_path(global_root_name, current_path)[1:]
        name = target_folders[-1]
        depth = len(target_folders)
        inserter(hierarchy_list, target_folders, ["file", name, depth, current_path])
    return hierarchy_list


def clean_hierarchy_list(root: list, filter_type: str, filter_strings: list, white_list: bool = True):
    """
    Clean the hierarchy-normalised list using filters

    root: hierarchy-normalised list
    """
    i = 0
    while i < len(root[-1]):
        """
        root[-1] = list
        root[-1][i] = i-ème entitée
        root[-1][i][0] = type de la i-ème entitée
        """
        typ = root[-1][i][0]
        if filter_type in ["extension", "file_name"]:
            if typ == "file":
                typ, file_name, depth, file_path = root[-1][i]
                extension = file_name.split(".")[-1]
                pop_this = False
                if filter_type == "extension" and (white_list and extension not in filter_strings or
                                                   not white_list and extension in filter_strings):
                    pop_this = True

                if filter_type == "file_name":
                    if white_list:
                        pop_this = True
                    else:
                        pop_this = False

                    for filter_string in filter_strings:
                        if white_list and filter_string in file_name:
                            pop_this = False
                        if not white_list and filter_string in file_name:
                            pop_this = True

                if pop_this:
                    root[-1].pop(i)
                    i -= 1
            else:
                clean_hierarchy_list(root[-1][i], filter_type, filter_strings, white_list)  # list in the i-ème element
                if len(root[-1][i][-1]) == 0:  # list in the i-eme element
                    root[-1].pop(i)
                    i -= 1

        elif filter_type == "folder_name":
            if typ == "folder":
                typ, folder_name, depth, file_path, lst = root[-1][i]
                if white_list and folder_name not in filter_strings or not white_list and folder_name in filter_strings:
                    root[-1].pop(i)
                    i -= 1
                else:
                    clean_hierarchy_list(root[-1][i], filter_type, filter_strings, white_list)  # list in the i-ème element
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
    """
    Sort a list of path using their type (file then folder)
    """
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


source = os.path.abspath("../..")
h = HierarchyMaker(source)

filter_dict = {
    "extension": ("white", []),
    "file_name": ("white", []),
    "folder_name": ("black", []),
    "depth": 10
}

x = h.get_hierarchy_normalised_text(filter_dict)

with open("hierarchy.txt", "w", encoding="utf-8") as file:
    file.write(x)

print(h.get_depth())
print(h.get_entity_count())
