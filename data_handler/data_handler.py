#! /usr/bin/env python311
# -*- coding: utf-8 -*-

"""
Warning, the crypt method used in this scrypt is easily breakable, so it's not
recommended to use this as a way to crypt public data
"""

import os

_file_name = "data_handler.txt"

_indicator = "__Well-decrypted-by-password-because-this-first-sentence-appear-miraculously-correctly__"


class data_handler:

    def __init__(self, file_name=_file_name, indicator=_indicator):
        """
        Allow to interact with a crypt data file easily
        """
        self.file_name = file_name
        self.indicator = indicator
        self.user_text_list = []
        self.user_separator = ("zHGriPp5$`V9I1g9$dP3ù9YEbbVo5l%sL%kmB21LrB[y16{7C7C$sE%Y"
                               "N'c>u^**cX4k4<,b'zFmQDr,_owt[SwjjO34(</c]p~m")

        self.update_text_list()

    def update(self):
        """
        This function will replace the data in file by the data of text_list
        It's used in order to save data in file
        """
        with open(self.file_name, "w", encoding="utf-8") as file:
            for i in range(len(self.user_text_list)):
                line = self.user_text_list[i]
                if len(self.user_text_list) > 1 and i != len(self.user_text_list) - 1:
                    line += self.user_separator
                file.write(line)
            file.close()

    def update_text_list(self):
        """
        Warning, in order to save your data in file use update_file_data instead

        This function will replace the data in text_list by the data of file
        """
        if not os.path.isfile(self.file_name):
            raise Exception(f"{self.file_name} is missing")

        text = ""
        with open(self.file_name, "r", encoding="utf-8") as file:
            for i in file.readlines():
                text += i
            file.close()

        self.user_text_list = text.split(self.user_separator)
        if self.user_text_list[0] == "":
            self.user_text_list = []

    def get_file_name(self):
        return self.file_name

    def get_indicator(self):
        return self.indicator

    def get_text_list(self):
        return self.user_text_list

    def get_user_index(self, password: str) -> int:
        """
        Return the user line index in the list, -1 if not exist (from text_list)
        """
        if password == "":
            raise Exception("The password is empty !")

        index = 0
        found_index = -1
        while index < len(self.user_text_list) and found_index == -1:
            line = self.user_text_list[index]
            decrypted_line = get_crypt_text(line, password, True)
            if get_word_index(decrypted_line, self.indicator) != -1:
                found_index = index
            index += 1

        return found_index

    def get_user_data(self, password: str) -> str:
        """
        Return user data decrypted from text_list
        """
        if password == "":
            raise Exception("The password is empty !")

        user_index = self.get_user_index(password)
        if user_index == -1:
            raise Exception("This password isn't linked with an account")
        decrypt_text = get_crypt_text(self.user_text_list[user_index], password, True)

        return decrypt_text[len(self.indicator):]

    def set_user_data(self, data: str, password: str):
        """
        Set user data in text_list
        data: Data not crypt
        """
        if password == "":
            raise Exception("The password is empty !")

        user_index = self.get_user_index(password)
        if user_index == -1:
            raise Exception("This password isn't linked with an account")

        new_crypt_data = get_crypt_text(f"{self.indicator}{data}", password)
        self.user_text_list[user_index] = new_crypt_data

    def add_new_user(self, password: str):
        """
        Add a new user in the text_list
        """
        if password == "":
            raise Exception("The password is empty !")

        user_index = self.get_user_index(password)
        if user_index != -1:
            raise Exception("This password isn't correct")

        user_crypt_text = get_crypt_text(self.indicator, password)
        self.user_text_list.append(user_crypt_text)

    def clear(self):
        """
        This function will clear text_list
        """
        self.user_text_list = []


def get_crypt_text(text: str, word: str, decrypt=False) -> str:
    """
    Return the text with all letters replaced by another in the ascii board using a word
    """
    new_text = ""

    index = 0
    max_index = len(word)

    for i in range(len(text)):
        car = text[i]
        car_num = ord(car)
        word_car_num = ord(word[index])
        if decrypt:
            new_car_num = car_num - word_car_num - i
            if new_car_num < 0:
                new_car_num += 256
        else:
            new_car_num = car_num + word_car_num + i
            if new_car_num > 255:
                new_car_num -= 256
        new_car = chr(new_car_num)
        new_text += new_car

        index += 1
        if index >= max_index:
            index = 0

    return new_text


def get_word_index(text: str, word: str) -> int:
    """
    Return the first index of the word in text, -1 if word not in text
    """
    index = 0
    size = len(word)
    while index < len(text) and text[index:index + size] != word:
        index += 1

    if index == len(text):
        return -1
    return index
