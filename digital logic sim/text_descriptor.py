"""
Objective: Make a way to render character, text and pictures on images
Creator: XenonEGG

using: python 3.6
encoding: utf-8
"""
import math as m
import numpy as np
from vector_class import Vector

"""
A character is represented by a vectorial that is a list of multi-lines
A multi-line is a list of points
"""

# Récupération des caractères


def split_text_with_index(text: str, index_list: list) -> list:
    """
    Split a text in a list of text using a list of index
    """
    nl = [text[0: index_list[0]]]
    for i in range(len(index_list) - 1):
        index_a, index_b = index_list[i], index_list[i + 1]
        nl.append(text[index_a + 1: index_b])
    nl.append(text[index_list[-1] + 1:])
    return nl


def get_free_comma(text: str) -> list:
    """
    Return the indexes of comma that are in the higher layer of a list of ...
    The higher layer is the last list, that don't contain other list
    """
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
    """
    Return an int or float of a text if possible
    """
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
    A recursive function that return an evaluation of a text (int, float, list, ...)
    """

    # Remove useless spaces
    while "  " in text:
        text.replace("  ", " ")
    if text[0] == " ":
        text = text[1:]
    if text[-1] == " ":
        text = text[:-1]

    """
    1- Find free comma and take an evaluation of each part of the text representing an object in a list
    2- If the text start by '[' and end by ']' take an evaluation of the text without '[' and ']' and return a list
    3- If the text start by '(' and end by ')' ...
    4- If the text represent other thing return a number or a text
    """

    # Research of free comma (comma that will represent separation between objects of the last layer's lists)
    free_virgule_indexes = get_free_comma(text)
    if len(free_virgule_indexes) > 0:
        split_text = split_text_with_index(text, free_virgule_indexes)
        new_list = []
        for e in split_text:
            new_list.append(get_evaluation_of(e)[0])
        return new_list, "comma"

    # If the text represent a list
    elif text[0] == "[" and text[-1] == "]":
        res, res_type = get_evaluation_of(text[1:-1])
        # The evaluation return already a list if the type is comma
        if res_type == "comma":
            return res, "list"
        return [res], "list"

    # If the text represent a tuple
    elif text[0] == "(" and text[-1] == ")":
        res, res_type = get_evaluation_of(text[1:-1])
        # The evaluation return a list if the type is comma
        if res_type == "comma":
            return tuple(res), "tuple"
        return (res,), "tuple"
    else:
        return get_number_of(text), "number"


"""
Recovery of character's data
"""
characters_dict = {}
with open("characters.csv", "r", encoding="utf-8") as file:
    data = file.read()
    lines = data.split("\n")
    for i in range(1, len(lines)):
        line = lines[i]
        character, style, text_vectorial = line.split(";")
        characters_dict[(character, style)] = get_evaluation_of(text_vectorial)[0]


def get_character_vectorial(car: str, style: str) -> list:
    """
    Return the vectorial, that represent geometrically a character
    """
    return characters_dict[(car, style)]


def get_points(vectorial: list) -> list:
    """
    Return a list of points that compose a vectorial
    """
    points = []
    for multiline in vectorial:
        for point in multiline:
            points.append(point)
    return points


def get_all_coordinate(points: list, index: int) -> list:
    """
    Return the first or second coordinate of each points from a list of points
    """
    coord_list = []
    for point in points:
        coord_list.append(point[index])
    return coord_list


def get_width(vectorial: list) -> float:
    """
    Return the width of a vectorial (x coordinate)
    """
    points = get_points(vectorial)
    x_list = get_all_coordinate(points, 0)
    return max(x_list) - min(x_list)


def get_height(vectorial: list) -> float:
    """
    Return the height of a vectorial (y coordinate)
    """
    points = get_points(vectorial)
    y_list = get_all_coordinate(points, 1)
    return max(y_list) - min(y_list)


def trace_quadrant_est(im, point_a: Vector, point_b: Vector, color: tuple):
    """
    Draw a line between two points in an image from west to est
    """
    xa, ya = point_a.get_coords()
    xb, yb = point_b.get_coords()
    dx = xb - xa
    dy = yb - ya
    im[xa, ya] = (0, 0, 0)
    im[xb, yb] = (0, 0, 0)
    for i in range(1, dx):
        nx = xa + i
        ny = m.floor(ya + dy / dx * i)
        im[nx, ny] = color


def trace_quadrant_south(im, point_a: Vector, point_b: Vector, color: tuple):
    """
    Draw a line between two points in an image from north to south
    """
    xa, ya = point_a.get_coords()
    xb, yb = point_b.get_coords()
    dx = xb - xa
    dy = yb - ya
    im[xa, ya] = (0, 0, 0)
    im[xb, yb] = (0, 0, 0)
    for i in range(1, dy):
        ny = ya + i
        nx = m.floor(xa + dx / dy * i)
        im[nx, ny] = color


def trace_line(im, point_a: Vector, point_b: Vector, color: tuple):
    """
    Draw a line between two points
    """
    xa, ya = point_a.get_coords()
    xb, yb = point_b.get_coords()
    dx = xb - xa
    dy = yb - ya
    if abs(dx) > abs(dy):
        if xa < xb:
            trace_quadrant_est(im, point_a, point_b, color)
        else:
            trace_quadrant_est(im, point_b, point_a, color)
    else:
        if ya < yb:
            trace_quadrant_south(im, point_a, point_b, color)
        else:
            trace_quadrant_south(im, point_b, point_a, color)


def rotate_90(im):
    """
    Return an image rotated by 90° in the trigonometrical way
    """
    a, b, r = im.shape
    im_type = im.dtype
    new_im = np.zeros((b, a, r), dtype=im_type)
    for i in range(a):
        for j in range(b):
            new_im[b - 1 - j, i] = im[i, j]
    return new_im


def trace_vectorial(im, vectorial: list, color: tuple):
    """
    Draw a vectorial on an image (the coordinates of each points of the vectorial will be the coordinates
    on the image)
    """
    for multiline in vectorial:
        for i in range(len(multiline) - 1):
            point_a, point_b = multiline[i], multiline[i + 1]
            trace_line(im, point_a, point_b, color)


def modify_vectorial(f, vectorial: list) -> list:
    """
    Return a vectorial where was applied for each points of the vectorial the function <f>
    """
    new_vectorial = []
    for multiline in vectorial:
        new_multiline = []
        for point in multiline:
            new_point = f(point)  # Warning, the function need to be well think
            new_multiline.append(new_point)
        new_vectorial.append(new_multiline)
    return new_vectorial


def set_height_vectorial(vectorial: list, wanted_height: float) -> list:
    """
    Fixes the height of the vectorial and adapt the width
    """
    height = get_height(vectorial)
    factor = wanted_height / height

    def f(pt: Vector):
        x, y = pt.get_coords()
        nx = m.floor(x * factor)
        ny = m.floor(y * factor)
        return Vector(pt.get_name(), nx, ny)

    vectorial = modify_vectorial(f, vectorial)
    return vectorial


def get_normalised_vectorial(vectorial: list) -> list:
    """
    Return a vectorial where all the points are in the quarter north est of a geometric reference
    """
    points = get_points(vectorial)
    x_list = get_all_coordinate(points, 0)
    y_list = get_all_coordinate(points, 1)
    min_x = min(x_list)
    min_y = min(y_list)
    step = Vector("step_a", -min_x, -min_y)
    f = lambda pt: pt + step
    vectorial = modify_vectorial(f, vectorial)
    return vectorial


def trace_car(im, car: str, style: str, po: Vector, wanted_height: float, color: tuple) -> float:
    """
    Draw a character on an image at the position of <po> (bottom left corner of the vectorial)
    and the height of <wanted_height> for this character
    """
    vectorial = get_character_vectorial(car, style)
    vectorial = set_height_vectorial(vectorial, wanted_height)
    width = get_width(vectorial)

    points = get_points(vectorial)
    min_x = min(get_all_coordinate(points, 0))
    min_y = min(get_all_coordinate(points, 1))
    xo, yo = po.get_coords()

    step = Vector("step_b", xo - min_x, yo - min_y)
    f = lambda pt: pt + step

    vectorial = modify_vectorial(f, vectorial)
    trace_vectorial(im, vectorial, color)
    return width


def trace_word(im, word: str, style: str, start_po: Vector, wanted_height: float, step: float, color: tuple) -> float:
    """
    Draw a word on an image where the characters have a fixed height and the bottom left corner of the word
    will be at position <start_po>
    Return the size of the word
    """
    current_po = start_po
    step_vector = Vector("step_c", step, 0)
    total_size = 0
    for letter in word:
        if letter == " ":
            current_po = current_po + step_vector * 10
            continue
        size = trace_car(im, letter, style, current_po, wanted_height, color)
        current_po = current_po + step_vector + Vector("size", size, 0)
        total_size += size + step

    total_size -= step
    return total_size


def trace_picture(im, picture_vectorial: list, start_po: Vector, wanted_height: float, color: tuple):
    """
    Draw a picture on an image like a character
    """
    picture_vectorial = get_normalised_vectorial(picture_vectorial)
    picture_vectorial = set_height_vectorial(picture_vectorial, wanted_height)
    xo, yo = start_po.get_coords()
    step = Vector("step_d", xo, yo)
    f = lambda pt: pt + step
    picture_vectorial = modify_vectorial(f, picture_vectorial)
    trace_vectorial(im, picture_vectorial, color)


def get_rectangle(point_a: Vector, point_b: Vector):
    """
    Return a rectangle that passes through <point_a> and <point_b>
    """
    xa, ya = point_a.get_coords()
    xb, yb = point_b.get_coords()
    vectorial = [[(xa, ya), (xb, ya), (xb, yb), (xa, yb), (xa, ya)]]
    return vectorial
