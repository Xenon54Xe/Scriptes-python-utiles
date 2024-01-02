# using python 3.6
# encoding utf-8

"""
Essaye de trouver l'extension recherchée dans les dossiers visés
"""

import os


path = "C:\\Users\\Titouan\\Documents\\Sony"  # dossier contenant les dossiers à fouiller
extension = ".txt"  # extension à trouver


class ExtensionFinder:
    def __init__(self):
        self.extension = None
        self.extension_paths = []

    def take_extension_paths(self, path):
        lib = os.listdir(path)
        for file in lib:
            if self.extension in file:
                self.extension_paths.append(f"{path}\\{file}")

    def open_folder(self, path):
        lib = os.listdir(path)
        for file in lib:
            new_path = f"{path}\\{file}"
            if os.path.isdir(new_path):
                self.take_extension_paths(new_path)
                self.open_folder(new_path)

    def find_extension(self, path, extension):
        self.extension = extension
        self.take_extension_paths(path)
        self.open_folder(path)
        return self.extension_paths


finder = ExtensionFinder()
found = finder.find_extension(path, extension)
print(found)
