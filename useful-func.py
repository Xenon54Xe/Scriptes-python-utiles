#! /usr/bin/env python311
# -*- coding: utf-8 -*-


import math
import random
import time


def quicksort(lst: list):
    """
    Sort a list quickly without returning anything (recursive)

    Complexité: nlog(n) dans le meilleur des cas, n² sinon
    n est la taille de la liste considérée
    """
    if len(lst) < 2:
        return
    pivot = lst.pop()
    small, tall = [], []
    for i in range(len(lst)):
        x = lst.pop()
        if x <= pivot:
            small.append(x)
        else:
            tall.append(x)

    quicksort(small)
    quicksort(tall)

    # Partie changée
    lst += small + [pivot] + tall


def myquicksort(lst):
    """
    Version intéressante de quicksort lorsque les nombres contenus dans la liste n'ont
    pas un écart relatif trop élevé

    Inconvénients: permet de trier uniquement les entiers relatifs

    Complexité: 2(n + max_value - min_value)
    n est la taille de la liste considérée

    Pour l'instant la fonction écrase les doublons et n'est pas optimisée quand l'écart relatif
    maximal entre les valeurs est trop grand
    """
    mini, maxi = min(lst), max(lst)

    nb_e_max = maxi - mini + 1
    add = -mini
    mirror = ["0" for i in range(nb_e_max)]
    for e in lst:
        mirror[e + add] = e

    nl = []
    for e in mirror:
        if e != "0":
            nl.append(e)
    return mirror


def sort_dictionary(old_dict: dict, croissant=True) -> dict:  # check
    """
    Sort a dictionary using integers as keys
    :param old_dict: dict(int, Any)
    :param croissant:
    :return:
    """
    old_keys = []
    for old_key in old_dict.keys():
        old_keys.append(old_key)

    new_keys = sort_list(old_keys, croissant)

    new_dict = {}
    for new_key in new_keys:
        new_dict[new_key] = old_dict[new_key]
    return new_dict


def reverse_dictionary(old_dict: dict) -> dict:  # check
    """
    Reverse the keys and the values of the dictionary, the new values are list if two keys gives the same value
    :param old_dict:
    :return:
    """
    old_keys = []
    old_values = []
    for item in old_dict.items():
        old_keys.append(item[0])
        old_values.append(item[1])

    new_dict = {}
    just_one_value = True
    for i in range(len(old_values)):
        old_value = old_values[i]
        old_key = old_keys[i]
        try:
            new_dict[old_value].append(old_key)
            just_one_value = False
        except:
            new_dict[old_value] = [old_key]

    result_dict = {}
    if just_one_value:
        for key in new_dict.keys():
            result_dict[key] = new_dict[key][0]
        return result_dict

    return new_dict


def sort_any_dictionary(old_dict: dict, croissant=True) -> dict:  # check
    """
    Sort a dictionary if it's possible
    :param old_dict:
    :param croissant:
    :return:
    """
    old_keys = []
    usable = True
    for key in old_dict.keys():
        old_keys.append(key)
        if type(key) not in [int, float]:
            usable = False

    if usable:  # si les clés sont des nombres
        return sort_dictionary(old_dict, croissant)

    old_values = []
    usable = True
    for item in old_dict.items():
        old_values.append(item[1])
        if type(item[1]) not in [int, float]:
            usable = False

    if usable:  # si les valeurs sont des nombres
        reversed_dict = reverse_dictionary(old_dict)
        sorted_dict = sort_dictionary(reversed_dict, croissant)
        return sorted_dict

    key_usable = True
    value_usable = True
    key_len_list = []
    value_len_list = []
    for item in old_dict.items():
        current_key = item[0]
        current_value = item[1]
        try:
            size = len(current_key)
            if size in key_len_list:
                key_usable = False
            key_len_list.append(size)
        except:
            key_usable = False
        try:
            size = len(current_value)
            if size in value_len_list:
                value_usable = False
            value_len_list.append(size)
        except:
            value_usable = False

    if key_usable:  # si toutes les clés ont une longueur différente
        len_dict = {}
        for i in range(len(key_len_list)):
            size = key_len_list[i]
            key = old_keys[i]
            len_dict[size] = key
        new_len_dict = sort_dictionary(len_dict)

        reversed_new_dict = {}
        for len_key in new_len_dict.keys():
            key = new_len_dict[len_key]
            reversed_new_dict[key] = old_dict[key]

        return reversed_new_dict

    if value_usable:  # si toutes les valeurs ont une longueur différente
        len_dict = {}
        for i in range(len(value_len_list)):
            size = value_len_list[i]
            value = old_values[i]
            len_dict[size] = value
        new_len_dict = sort_dictionary(len_dict)

        reversed_old_dict = reverse_dictionary(old_dict)

        reversed_new_dict = {}
        for len_key in new_len_dict.keys():
            value = new_len_dict[len_key]
            reversed_new_dict[value] = reversed_old_dict[value]

        return reverse_dictionary(reversed_new_dict)

    return {}


def convert(start_base: int, target_base: int, number: str) -> str:
    """
    Convert a number from the start_base to the target_base
    :param start_base:
    :param target_base:
    :param number:
    :return:
    """
    ref = {
        0: "0",
        1: "1",
        2: "2",
        3: "3",
        4: "4",
        5: "5",
        6: "6",
        7: "7",
        8: "8",
        9: "9",
        10: "A",
        11: "B",
        12: "C",
        13: "D",
        14: "E",
        15: "F",
        16: "G",
        17: "H",
        18: "I",
        19: "J",
        20: "K",
        21: "L",
        22: "M",
        23: "N",
        24: "O",
        25: "P",
        26: "Q",
        27: "R",
        28: "S",
        29: "T",
        30: "U",
        31: "V",
        32: "W",
        33: "X",
        34: "Y",
        35: "Z"
    }
    inverted_ref = reverse_dictionary(ref)

    if not 2 <= start_base <= 35 or not 2 <= target_base <= 35 or start_base == target_base:
        raise Exception("The bases need to be between the base 2 and the base 35")

    """
    Verification: is the number interpretable in the 'start_base'
    """
    keys = []
    for i in inverted_ref.keys():
        keys.append(i)

    for i in number:
        if i not in keys[:start_base]:
            raise Exception(f"{number} in base {start_base} isn't correct")

    """
    Convert the number from 'start_base' to base 10
    """
    power = len(number) - 1
    value = 0
    for i in range(len(number)):
        num = inverted_ref[number[i]]
        value += num * math.pow(start_base, power - i)

    """
    Convert the number from base 10 to 'target_base'
    """
    result = ""
    while value > 0:
        rest = value % target_base
        result = ref[rest] + result
        value //= target_base

    return result
