"""
Objective: Make a little database
Creator: XenonEGG

using: python 3.6
encoding: utf-8
"""

import os

_abs_path = os.path.abspath("")

_file_path = f"{_abs_path}\\data_handler_not_crypted.txt"

_data_separator = "__Data-separator-de-la-mort__"

_user_separator = "__User-separator-de-la-mort__"


class data_handler:

    def __init__(self, file_path=_file_path, user_separator=_user_separator, data_separator=_data_separator):
        """
        Allow to interact with a data file easily
        """
        self.file_path = file_path
        self.user_text_dict = {}

        self.user_separator = user_separator
        self.data_separator = data_separator

        if not os.path.exists(file_path):
            with open(file_path, "wb") as file:
                pass

        self.update_text_list()

    def update(self):
        """
        This function will replace the data in file by the data of text_list
        It's used in order to save data in file
        """
        with open(self.file_path, "w", encoding="utf-8") as file:
            text = ""
            for key in self.user_text_dict.keys():
                line = f"{key}{self.data_separator}{self.user_text_dict[key]}{self.user_separator}"
                text += line
            text = text[:-len(self.user_separator)]
            file.write(text)

    def update_text_list(self):
        """
        Warning, in order to save your data in file use update instead

        This function will replace the data in text_list by the data of file
        """
        if not os.path.isfile(self.file_path):
            raise Exception(f"{self.file_path} is missing")

        with open(self.file_path, "r", encoding="utf-8") as file:
            text = file.read()

        self.clear()
        user_bytes = text.split(self.user_separator)
        if len(user_bytes) != 1 or user_bytes[0] != "":
            for byte in user_bytes:
                username, data = byte.split(self.data_separator)
                self.user_text_dict[username] = data

    def get_file_name(self):
        return self.file_path

    def get_text_dict(self):
        return self.user_text_dict

    def get_user_data(self, username: str) -> str:
        """
        Return user data decrypted from text_list
        """
        if username == "":
            raise Exception("The username is empty !")

        try:
            text = self.user_text_dict[username]
            return text
        except:
            raise Exception(f"{username} n'existe pas dans la base de données")

    def set_user_data(self, username: str, data: str):
        """
        Set user data in text_list
        data: Data not crypt
        """
        if username == "":
            raise Exception("The username is empty !")

        self.user_text_dict[username] = data

    def clear(self):
        """
        This function will clear text_dict
        """
        self.user_text_dict.clear()
