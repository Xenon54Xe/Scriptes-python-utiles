"""
Objective: Make a hierarchy class representing the folder's hierarchy below a source path
Creator: XenonEGG

using: python 3.6
encoding: utf-8
"""

import os


class Filter:
    def __init__(self, typ: str, white_list: bool, filter_list: list):
        """
        A class representing filters used in HierarchyMaker
        """
        if typ not in ["file_name", "extension", "folder_name", "depth"]:
            raise f"{typ} filter type is not allowed"
        self.typ = typ
        self.white_list = white_list
        self.filter_list = filter_list

    def get_type(self) -> str:
        return self.typ

    def get_white_list(self) -> bool:
        return self.white_list

    def get_filter_list(self) -> list:
        return self.filter_list


class HierarchyObject:
    def __init__(self, name, path, depth):
        """
        The main class representing objects used in HierarchyMaker
        """
        self.name = name
        self.path = path
        self.depth = depth

    def get_name(self) -> str:
        return self.name

    def get_path(self) -> str:
        return self.path

    def get_depth(self) -> int:
        return self.depth

    def get_copy(self):
        """
        Return a full copy of the object
        """
        return HierarchyObject(self.name, self.path, self.depth)


class HierarchyFile(HierarchyObject):
    def __init__(self, name, path, depth):
        """
        A class representing file used in HierarchyMaker
        """
        super().__init__(name, path, depth)

    def get_copy(self):
        """
        Return a full copy of the file
        """
        return HierarchyFile(self.name, self.path, self.depth)


class HierarchyFolder(HierarchyObject):
    def __init__(self, name, path, depth):
        """
        A class representing folder used in HierarchyMaker
        """
        super().__init__(name, path, depth)
        self.entity_list = []

    def get_entity_list(self) -> list:
        """
        Return the list of entity stored in the folder
        """
        return self.entity_list

    def get_entity(self, index):
        """
        Return the entity with index
        """
        return self.entity_list[index]

    def get_copy(self):
        """
        Return a full copy of the folder (the others hierarchy-objects stored in are copied too)
        """
        new_entity = HierarchyFolder(self.name, self.path, self.depth)
        nl = []
        for entity in self.get_entity_list():
            nl.append(entity.get_copy())
        new_entity.set_entity_list(nl)
        return new_entity

    def set_entity_list(self, lst: list):
        self.entity_list = lst.copy()

    def add_entity(self, entity: HierarchyObject):
        self.entity_list.append(entity)

    def insert_entity(self, index: int, entity: HierarchyObject):
        self.entity_list.insert(index, entity)

    def remove_entity(self, entity: HierarchyObject):
        self.entity_list.remove(entity)

    def pop_entity(self, index: int):
        self.entity_list.pop(index)

    def clear_entity_list(self):
        self.entity_list.clear()


class HierarchyMaker:
    def __init__(self, source_path: str,  file_arrow: str = "--->", folder_arrow: str = ">   ", tab: str = "    "):
        """
        Use the classes HierarchyObject and Filter to make an object representing the file's hierarchy
        in you computer

        Step:
            - update(source_path) iterate over every folder in the root folder
            - get_hierarchy_folder(filter_list): get the list filtered or not
            - get_hierarchy_normalised_text(filter_list): get the string representing the list
        """

        """
        Variables used to print the hierarchy
        """
        self.file_arrow = file_arrow
        self.folder_arrow = folder_arrow
        self.tab = tab

        """
        Variables used to make the hierarchy
        """
        self.source_path = None
        self.source_name = None
        self.hierarchy_folder = HierarchyFolder("", "", -1)
        self.hierarchy_normalised_text = ""

        """
        Variables about the hierarchy
        """
        self.max_depth = 0
        self.folder_count = 0
        self.file_count = 0
        self.data_list = []  # A list storing type (File, Folder) and path of files/folders

        self.update(source_path)

    def get_max_depth(self) -> int:
        return self.max_depth

    def get_folder_count(self) -> int:
        return self.folder_count

    def get_file_count(self) -> int:
        return self.file_count

    def get_entity_count(self) -> int:
        return self.folder_count + self.file_count

    def update(self, source_path: str):
        """
        Update the hierarchy-object using a source path representing the root folder
        """
        self.source_path = source_path
        source_name = os.path.split(source_path)[-1]
        self.source_name = source_name

        self.hierarchy_folder = HierarchyFolder(source_name, source_path, 0)
        self.fill_hierarchy_object(source_path, self.hierarchy_folder)

    def get_hierarchy_object(self, filter_list: list = None) -> HierarchyFolder:
        """
        Return the hierarchy-object representing the folder's hierarchy filtered or not
        """

        if filter_list is None:
            return self.hierarchy_folder.get_copy()

        hierarchy_folder_copy = self.hierarchy_folder.get_copy()

        for current_filter in filter_list:
            filter_type, white_list, filter_list = current_filter.get_type(), current_filter.get_white_list(), current_filter.get_filter_list()

            if filter_type == "extension":
                filter_list = [e.replace(".", "") for e in filter_list]

            if len(filter_list) != 0:
                self.data_list.clear()
                self.clean_hierarchy_object(hierarchy_folder_copy, filter_type, filter_list, white_list)
                if filter_type == "folder_name" and white_list or filter_type == "depth":
                    # obligé de copier la liste lorsqu'on utilise convert_path_list
                    hierarchy_folder_copy = convert_path_list_to_hierarchy_list(self.source_path, self.data_list)

        return hierarchy_folder_copy

    def clean_hierarchy_object(self, root: HierarchyFolder, filter_type: str, filter_list: list, white_list: bool = True):
        """
        Clean the hierarchy-object using filters
        """
        if filter_type == "file_name":
            i = 0
            while i < len(root.get_entity_list()):
                entity = root.get_entity(i)
                typ = type(entity)
                if typ == HierarchyFile:
                    name = entity.get_name()

                    if white_list:
                        pop_this = True
                    else:
                        pop_this = False

                    for filter_string in filter_list:
                        if white_list and filter_string in name:
                            pop_this = False
                        if not white_list and filter_string in name:
                            pop_this = True

                    if pop_this:
                        root.pop_entity(i)
                        i -= 1
                elif typ == HierarchyFolder:
                    self.clean_hierarchy_object(entity, filter_type, filter_list, white_list)  # list in the i-ème element
                    if len(entity.get_entity_list()) == 0:  # list in the i-eme element
                        root.pop_entity(i)
                        i -= 1
                i += 1

        if filter_type == "extension":
            i = 0
            while i < len(root.get_entity_list()):
                entity = root.get_entity(i)
                typ = type(entity)
                if typ == HierarchyFile:
                    name = entity.get_name()
                    extension = name.split(".")[-1]
                    if white_list and extension not in filter_list or not white_list and extension in filter_list:
                        root.pop_entity(i)
                        i -= 1

                elif typ == HierarchyFolder:
                    self.clean_hierarchy_object(entity, filter_type, filter_list, white_list)
                    if len(entity.get_entity_list()) == 0:
                        root.pop_entity(i)
                        i -= 1
                i += 1

        if filter_type == "folder_name":
            i = 0
            data_list = []
            while i < len(root.get_entity_list()):
                entity = root.get_entity(i)
                name = entity.get_name()

                if white_list:
                    if type(entity) == HierarchyFile:
                        path = entity.get_path()
                        for filter_string in filter_list:
                            if filter_string in path:
                                data_list.append((type(entity), path))
                                break
                    elif type(entity) == HierarchyFolder:
                        self.clean_hierarchy_object(entity, filter_type, filter_list, white_list)

                elif type(entity) == HierarchyFolder:
                    if name in filter_list:
                        root.pop_entity(i)
                        i -= 1
                    else:
                        self.clean_hierarchy_object(root.get_entity(i), filter_type, filter_list, white_list)
                i += 1
            self.data_list += data_list

        if filter_type == "depth":
            data_list = []
            for entity in root.get_entity_list():
                depth = entity.get_depth()
                if white_list and depth in filter_list or not white_list and depth not in filter_list:
                    path = entity.get_path()
                    data_list.append((type(entity), path))
                if type(entity) == HierarchyFolder:
                    self.clean_hierarchy_object(entity, filter_type, filter_list, white_list)
            self.data_list += data_list

    def get_hierarchy_normalised_text(self, filter_list: list = None) -> str:
        """
        Return a string representing the folder's hierarchy, filtered or not
        """
        new_hierarchy_folder = self.get_hierarchy_object(filter_list)
        self.hierarchy_normalised_text = ""
        self.make_hierarchy_normalised_text(new_hierarchy_folder)
        return self.hierarchy_normalised_text

    def fill_hierarchy_object(self, source_path: str, root: HierarchyFolder, depth: int = 1):
        """
        Use hierarchy-object to store the folder's hierarchy

        source_path: The folder's path where the hierarchy begin
        """
        lib = os.listdir(source_path)

        if depth == 1:
            self.max_depth = 1
            self.file_count = 0
            self.folder_count = 0

        if len(lib) == 0:
            return
        sort_file_and_folder(lib, source_path)

        if self.max_depth < depth:
            self.max_depth = depth

        for file_name in lib:
            file_path = os.path.join(source_path, file_name)
            if os.path.isdir(file_path):
                self.folder_count += 1
                root.add_entity(HierarchyFolder(file_name, file_path, depth))
                self.fill_hierarchy_object(file_path, root.get_entity(-1), depth + 1)
            else:
                self.file_count += 1
                root.add_entity(HierarchyFile(file_name, file_path, depth))

    def make_hierarchy_normalised_text(self, root: HierarchyFolder, depth: int = 0):
        """
        Make a string representing the folder's hierarchy and store it in hierarchy_normalised_text
        """
        root_name, root_list = root.get_name(), root.get_entity_list()
        if depth == 0:
            self.hierarchy_normalised_text += root_name + "\n"
        else:
            self.hierarchy_normalised_text += self.tab * (depth - 1) + self.folder_arrow + root_name + "\n"

        for entity in root_list:
            typ = type(entity)
            if typ == HierarchyFile:
                self.hierarchy_normalised_text += self.tab * depth + self.file_arrow + entity.get_name() + "\n"
            else:
                self.make_hierarchy_normalised_text(entity, depth + 1)


def split_path(path: str, cut: str) -> list:
    """
    Return the path in a list and remove the first part of the path
    """
    nl = []
    while os.path.split(path)[-1] != "":
        x, y = os.path.split(path)
        nl.insert(0, y)
        if y == cut:
            return nl
        path = x
    return nl


def convert_path_list_to_hierarchy_list(source_path: str, data_list: list) -> HierarchyFolder:
    """
    Convert a list of path into a HierarchyFolder

    source_path: the folder where begin the HierarchyFolder
    data_list: a list of tuples representing the type and the path of files/folders
    """
    source_name = os.path.split(source_path)[-1]
    hierarchy_list = HierarchyFolder(source_name, source_path, 0)

    for data in data_list:
        typ, path = data
        target_folders = split_path(path, source_name)[1:]
        name = target_folders[-1]
        depth = len(target_folders)
        if typ == HierarchyFolder:
            entity = HierarchyFolder(name, path, depth)
        else:
            entity = HierarchyFile(name, path, depth)
        inserter(hierarchy_list, target_folders, entity)
    return hierarchy_list


def inserter(root: HierarchyFolder, target_folders: list, entity_data: HierarchyFile):
    """
    Use recursion to go into HierarchyFolder where the file/folder is stored
    """
    current_target_name = target_folders[0]

    if len(target_folders) <= 1:
        root.insert_entity(0, entity_data)
        return

    found = False
    for entity in root.get_entity_list():
        typ = type(entity)
        if typ == HierarchyFolder:
            entity_name = entity.get_name()
            if entity_name == current_target_name:
                inserter(entity, target_folders[1:], entity_data)
                found = True

    if not found:
        new_path = os.path.join(root.get_path(), current_target_name)
        new_entity = HierarchyFolder(current_target_name, new_path, root.get_depth() + 1)
        root.add_entity(new_entity)
        inserter(new_entity, target_folders[1:], entity_data)


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


"""
source = os.path.abspath("../..")
hierarchy = HierarchyMaker(source)

file_name_f = Filter("file_name", True, [])
extension_f = Filter("extension", True, [])
folder_name_fb = Filter("folder_name", False, [])
folder_name_fw = Filter("folder_name", True, [])
depth_f = Filter("depth", True, [11])
list_filter = [folder_name_fb, folder_name_fw, extension_f, file_name_f, depth_f]

text = hierarchy.get_hierarchy_normalised_text(list_filter)
text_b = hierarchy.get_hierarchy_normalised_text()

with open("hierarchy.txt", "w", encoding="utf-8") as file:
    file.write(text_b)

print(hierarchy.get_max_depth())
print(hierarchy.get_entity_count())
print(hierarchy.get_folder_count())
print(hierarchy.get_file_count())
"""
