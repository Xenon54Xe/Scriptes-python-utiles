"""
Objective: Make a way to render character and text on images
Creator: XenonEGG

using: python 3.6
encoding: utf-8
"""
import math as m
import numpy as np

"""
A character is represented by a vectorial that is a list of multi-lines
A multi-line is a list of points
"""

# Récupération des caractères


def split_text_with_index(text: str, index_list: list) -> list:
    nl = [text[0: index_list[0]]]
    for i in range(len(index_list) - 1):
        index_a, index_b = index_list[i], index_list[i + 1]
        nl.append(text[index_a + 1: index_b])
    nl.append(text[index_list[-1] + 1:])
    return nl


def get_free_virgule(text: str) -> list:
    count = 0
    index_list = []
    for i in range(len(text)):
        e = text[i]
        if e in ["[", "("]:
            count += 1
        elif e in ["]", ")"]:
            count -= 1
        elif count == 0 and e == ",":
            index_list.append(i)
    return index_list


def get_number_of(text: str):
    try:
        x = float(text)
        if x == int(x):
            return int(text)
        else:
            return float(text)
    except:
        return text


def get_evaluation_of(text: str):
    """
    Text épuré a convertir en liste
    """
    while "  " in text:
        text.replace("  ", " ")
    if text[0] == " ":
        text = text[1:]
    if text[-1] == " ":
        text = text[:-1]

    free_virgule_indexes = get_free_virgule(text)
    if len(free_virgule_indexes) > 0:
        il = split_text_with_index(text, free_virgule_indexes)
        nl = []
        for e in il:
            nl.append(get_evaluation_of(e)[0])
        return nl, "virgule"
    elif text[0] == "[" and text[-1] == "]":
        res, res_type = get_evaluation_of(text[1:-1])
        if res_type == "virgule":
            return res, "list"
        return [res], "list"
    elif text[0] == "(" and text[-1] == ")":
        res, res_type = get_evaluation_of(text[1:-1])
        if res_type == "virgule":
            return tuple(res), "tuple"
        return (res,), "tuple"
    else:
        return get_number_of(text), "number"


characters_dict = {}
with open("characters.csv", "r", encoding="utf-8") as file:
    data = file.read()
    lines = data.split("\n")
    for i in range(1, len(lines)):
        line = lines[i]
        character, style, text_vectorial = line.split(";")
        characters_dict[(character, style)] = get_evaluation_of(text_vectorial)[0]


def get_character_vectorial(car: str, style: str) -> list:
    return characters_dict[(car, style)]


def get_points(vectorial: list) -> list:
    points = []
    for multiline in vectorial:
        for point in multiline:
            points.append(point)
    return points


def get_all_coordinate(points: list, index: int) -> list:
    coord_list = []
    for point in points:
        coord_list.append(point[index])
    return coord_list


def get_width(vectorial: list) -> float:
    points = get_points(vectorial)
    x_list = get_all_coordinate(points, 0)
    return max(x_list) - min(x_list)


def get_height(vectorial: list) -> float:
    points = get_points(vectorial)
    y_list = get_all_coordinate(points, 1)
    return max(y_list) - min(y_list)


def trace_quadrant_est(im, point_a: tuple, point_b: tuple, color: tuple):
    xa, ya = point_a
    xb, yb = point_b
    dx = xb - xa
    dy = yb - ya
    im[xa, ya] = (0, 0, 0)
    im[xb, yb] = (0, 0, 0)
    for i in range(1, dx):
        nx = xa + i
        ny = m.floor(ya + dy / dx * i)
        im[nx, ny] = color


def trace_quadrant_sud(im, point_a: tuple, point_b: tuple, color: tuple):
    xa, ya = point_a
    xb, yb = point_b
    dx = xb - xa
    dy = yb - ya
    im[xa, ya] = (0, 0, 0)
    im[xb, yb] = (0, 0, 0)
    for i in range(1, dy):
        ny = ya + i
        nx = m.floor(xa + dx / dy * i)
        im[nx, ny] = color


def trace_line(im, point_a: tuple, point_b: tuple, color: tuple):
    xa, ya = point_a
    xb, yb = point_b
    dx = xb - xa
    dy = yb - ya
    if abs(dx) > abs(dy):
        if xa < xb:
            trace_quadrant_est(im, point_a, point_b, color)
        else:
            trace_quadrant_est(im, point_b, point_a, color)
    else:
        if ya < yb:
            trace_quadrant_sud(im, point_a, point_b, color)
        else:
            trace_quadrant_sud(im, point_b, point_a, color)


def rotate_90(im):
    a, b, r = im.shape
    im_type = im.dtype
    new_im = np.zeros((b, a, r), dtype=im_type)
    for i in range(a):
        for j in range(b):
            new_im[b - 1 - j, i] = im[i, j]
    return new_im


def trace_vectorial(im, vectorial: list, color: tuple):
    for multiline in vectorial:
        for i in range(len(multiline) - 1):
            point_a, point_b = multiline[i], multiline[i + 1]
            trace_line(im, point_a, point_b, color)


def modify_vectorial(f, vectorial: list) -> list:
    new_vectorial = []
    for multiline in vectorial:
        new_multiline = []
        for point in multiline:
            new_point = f(point)
            new_multiline.append(new_point)
        new_vectorial.append(new_multiline)
    return new_vectorial


def set_height_vectorial(vectorial: list, wanted_height: float) -> list:
    height = get_height(vectorial)
    factor = wanted_height / height
    f = lambda pt: (m.floor(pt[0] * factor), m.floor(pt[1] * factor))
    vectorial = modify_vectorial(f, vectorial)
    return vectorial


def get_normalised_vectorial(vectorial: list) -> list:
    """
    The bottom left point will be (0, 0)
    """
    points = get_points(vectorial)
    x_list = get_all_coordinate(points, 0)
    y_list = get_all_coordinate(points, 1)
    min_x = min(x_list)
    min_y = min(y_list)
    f = lambda pt: (pt[0] - min_x, pt[1] - min_y)
    vectorial = modify_vectorial(f, vectorial)
    return vectorial


def trace_car(im, car: str, style: str, po: tuple, wanted_height: float, color: tuple) -> float:
    """
    po: represent the wanted position of the bottom left corner of the character
    """
    vectorial = get_character_vectorial(car, style)
    vectorial = set_height_vectorial(vectorial, wanted_height)
    width = get_width(vectorial)

    points = get_points(vectorial)
    min_x = min(get_all_coordinate(points, 0))
    min_y = min(get_all_coordinate(points, 1))
    xo, yo = po
    f = lambda pt: (m.floor(pt[0] - min_x + xo), m.floor(pt[1] - min_y + yo))
    vectorial = modify_vectorial(f, vectorial)

    trace_vectorial(im, vectorial, color)
    return width


def trace_word(im, word: str, style: str, start_po: tuple, wanted_height: float, step: float, color: tuple) -> float:
    current_po = start_po
    total_size = 0
    for letter in word:
        if letter == " ":
            current_po = (current_po[0] + 10 * step, current_po[1])
            continue
        size = trace_car(im, letter, style, current_po, wanted_height, color)
        current_po = (current_po[0] + size + step, current_po[1])
        total_size += size + step

    total_size -= step
    return total_size


def trace_picture(im, picture_vectorial: list, start_po: tuple, wanted_height: float, color: tuple):
    picture_vectorial = get_normalised_vectorial(picture_vectorial)
    picture_vectorial = set_height_vectorial(picture_vectorial, wanted_height)
    xo, yo = start_po
    f = lambda pt: (pt[0] + xo, pt[1] + yo)
    picture_vectorial = modify_vectorial(f, picture_vectorial)
    trace_vectorial(im, picture_vectorial, color)


def get_rectangle(point_a: tuple, point_b: tuple):
    xa, ya = point_a
    xb, yb = point_b
    vectorial = [[(xa, ya), (xb, ya), (xb, yb), (xa, yb), (xa, ya)]]
    return vectorial
