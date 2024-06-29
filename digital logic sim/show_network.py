"""
Unit visual descriptor
"""

import math as m
import numpy as np
import matplotlib.pyplot as plt
import text_descriptor as td


class UnitVisual:
    def __init__(self, name: str, input_count: int, output_count: int, accuracy: float):
        self.name = name
        self.input_count = input_count
        self.output_count = output_count
        self.accuracy = accuracy

        self.vectorial = None
        self.step_between_letter = 0
        self.total_width = 0
        self.total_height = 0

        self.make_shape_vectorial()
        self.make_input_and_output_vectorial()

    def make_shape_vectorial(self):
        vectorial_list = []
        total_letters_width = 0
        for letter in self.name:
            vectorial = td.get_character_vectorial(letter, "square")
            vectorial = td.set_height_vectorial(vectorial, self.accuracy)
            vectorial = td.get_normalised_vectorial(vectorial)
            total_letters_width += td.get_width(vectorial)

            vectorial_list.append(vectorial)

        width_mean = total_letters_width / len(self.name)
        step = width_mean / 10
        self.step_between_letter = step

        new_vectorial_list = [vectorial_list[0]]
        current_x = 0
        for cur_vectorial in vectorial_list:
            f = lambda pt: (m.floor(pt[0] + current_x), m.floor(pt[1]))
            new_vectorial = td.modify_vectorial(f, cur_vectorial)
            width = td.get_width(new_vectorial)
            new_vectorial_list.append(new_vectorial)
            current_x += width + step

        total_width = total_letters_width + (len(self.name) - 1) * step
        point_a = (m.floor(- 2 * step), m.floor(- 2 * step))
        point_b = (m.floor(total_width + 2 * step), m.floor(self.accuracy + 2 * step))
        rectangle_vectorial = td.get_rectangle(point_a, point_b)
        self.total_width = td.get_width(rectangle_vectorial)
        self.total_height = td.get_height(rectangle_vectorial)

        main_vectorial = []
        for vectorial in new_vectorial_list + [rectangle_vectorial]:
            for multiline in vectorial:
                main_vectorial.append(multiline)

        self.vectorial = main_vectorial

    def make_input_and_output_vectorial(self):
        new_vectorial = td.get_normalised_vectorial(self.vectorial)
        dist = self.accuracy / 20

        """
        Input pin
        """
        po = (- 2 * self.step_between_letter, self.total_height / 2 - (self.input_count - 1) * 2 * dist)
        for i in range(self.input_count):
            point_a = (m.floor(po[0] - dist), m.floor(po[1] + i * 4 * dist - dist))
            point_b = (m.floor(po[0] + dist), m.floor(po[1] + i * 4 * dist + dist))
            new_rectangle = td.get_rectangle(point_a, point_b)
            new_vectorial.append(new_rectangle[0])

        """
        Output pin
        """
        po = (self.total_width + 2 * self.step_between_letter, self.total_height / 2 - (self.output_count - 1) * 2 * dist)
        for i in range(self.output_count):
            point_a = (m.floor(po[0] - dist), m.floor(po[1] + i * 4 * dist - dist))
            point_b = (m.floor(po[0] + dist), m.floor(po[1] + i * 4 * dist + dist))
            new_rectangle = td.get_rectangle(point_a, point_b)
            new_vectorial.append(new_rectangle[0])

        self.vectorial = new_vectorial

    def get_vectorial(self):
        """
        The point (0, 0) is in the bottom left corner of the rectangle
        """
        return self.vectorial


test = UnitVisual("and", 2, 1, 200)
im = np.ones((1000, 1000, 3), dtype=np.uint8) * 255
td.trace_picture(im, test.get_vectorial(), (500, 500), 10, (0, 0, 0))
im = td.rotate_90(im)
plt.imshow(im)
plt.show()
