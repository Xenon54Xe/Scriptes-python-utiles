"""
Objective: Make my own program language
Creator: XenonEGG

using: python 3.6
encoding: utf-8
"""

import math as m

"""
Définition du corps:

Ligne:
Une ligne représente une opération
Une ligne commence par un mot clé

Mot clé:
Un mot clé est toujours suivi d'argument(s)

Argument:
Un argument représente soit une variable soit une constante existante (nombres, lettres...)
"""

"""
Récupération du program
"""
with open("program.txt", "r", encoding="utf-8") as file:
    _program = file.read()

"""
Définition des mots clés
"""
# Variables:
var_list = ["setvar", "add", "sub", "mul", "div", "power"]

# Fonctions:
func_list = ["print"]

# Tout:
key_word_list = var_list + func_list

"""
Variable handler
"""
var_dict = {"pi": "3.1415"}


"""
Classe d'erreurs
"""


class VarIsNotNumber(Exception):
    def __init__(self, name):
        super().__init__(f"'{name}'")


"""
Fonctions utilisables
"""


def setvar(*args):
    var = args[0]
    var_dict[var] = args[1]


def _can_be_number(arg):
    try:
        float(arg)
        return True
    except:
        return False


def _is_number(arg):
    if isinstance(arg, float):
        return True
    if isinstance(arg, int):
        return True
    return False


def _get_numbers(arg_a, arg_b):
    if _can_be_number(arg_a):
        var_a_value = float(arg_a)
    else:
        try:
            var_a_value = float(var_dict[arg_a])
        except:
            raise VarIsNotNumber(arg_a)
    if _can_be_number(arg_b):
        var_b_value = float(arg_b)
    else:
        try:
            var_b_value = float(var_dict[arg_b])
        except:
            raise VarIsNotNumber(arg_b)
    return var_a_value, var_b_value


def add(*args):
    var = args[0]
    var_a_value, var_b_value = _get_numbers(args[1], args[2])
    var_dict[var] = var_a_value + var_b_value


def sub(*args):
    var = args[0]
    var_a_value, var_b_value = _get_numbers(args[1], args[2])
    var_dict[var] = var_a_value - var_b_value


def mul(*args):
    var = args[0]
    var_a_value, var_b_value = _get_numbers(args[1], args[2])
    var_dict[var] = var_a_value * var_b_value


def div(*args):
    var = args[0]
    var_a_value, var_b_value = _get_numbers(args[1], args[2])
    var_dict[var] = var_a_value / var_b_value


def power(*args):
    var = args[0]
    var_a_value, var_b_value = _get_numbers(args[1], args[2])
    var_dict[var] = var_a_value ** var_b_value


"""
Analyse du programme
"""

operation_list = _program.split("\n")

for operation in operation_list:
    word_list = operation.split(" ")
    print(word_list)
    key_word = word_list.pop(0)
    if key_word != "":
        argument_list = word_list
        # Utilisation de la fonction associée au key_word
        globals()[key_word](*argument_list)

print(var_dict)
