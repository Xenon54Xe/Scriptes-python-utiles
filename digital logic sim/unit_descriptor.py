"""
Logic unit visual descriptor
"""

import math as m
import numpy as np
import matplotlib.pyplot as plt
import text_descriptor as td
from vector_class import Vector


class UnitVisual:
    def __init__(self, name: str, input_count: int, output_count: int,
                 size_between_letters_factor: float, size_between_letters_and_rectangle_factor: float,
                 pins_size_factor: float, size_between_pins_and_rectangle_factor: float):
        """
        Represent a logic unit as a vectorial to be drawn on an image
        """
        self.name = name
        # Number of input
        self.input_count = input_count
        # Number of output
        self.output_count = output_count

        # The vectorial to represent the unit
        self.vectorial = None

        # The rapport of the space between letters and the width of the letters
        self.size_between_letters_factor = size_between_letters_factor
        # The rapport of the space between letters and rectangle and the mean width of letters
        self.size_between_letters_and_rectangle_factor = size_between_letters_and_rectangle_factor
        # The rapport of the size of pins and height of the main rectangle
        self.pins_size_factor = pins_size_factor
        # The rapport of the width of the main rectangle and the space between pins and main rectangle
        self.size_between_pins_and_rectangle_factor = size_between_pins_and_rectangle_factor
        # The step between each letter of the name of the unit
        self.step_between_letter = 0

        # The width of the unit (including rectangle)
        self.total_width = 0
        # The height of the unit (including rectangle)
        self.total_height = 0

        # List of coordinates of inputs and outputs
        self.input_coordinates_list = []
        self.output_coordinates_list = []

        # Processing
        self._make_shape_vectorial()
        self._make_input_and_output_vectorial()

    def _make_shape_vectorial(self):
        """
        Creation of the picture that will represent the unit (rectangle + characters)
        the point (0, 0) will be in the bottom left corner of the picture's rectangle
        """
        vectorial_list = []
        total_letters_width = 0
        for letter in self.name:
            vectorial = td.get_character_vectorial_vector(letter, "square")
            vectorial = td.set_height_vectorial(vectorial, 200)
            vectorial = td.get_normalised_vectorial(vectorial)
            total_letters_width += td.get_width(vectorial)

            vectorial_list.append(vectorial)

        width_mean = total_letters_width / len(self.name)
        step_between_letters = width_mean * self.size_between_letters_factor
        self.step_between_letter = step_between_letters

        new_vectorial_list = [vectorial_list[0]]
        current_x = 0
        # Adaptation of point's coordinates for the picture and relative position of vectorial
        for cur_vectorial in vectorial_list:
            # Add current x to every point and take floor of the coordinates
            def f(pt):
                step_vector = Vector("step_e", current_x, 0)
                pt += step_vector
                new_vector = Vector("point", m.floor(pt[0]), m.floor(pt[1]))
                return new_vector
            new_vectorial = td.modify_vectorial(f, cur_vectorial)
            width = td.get_width(new_vectorial)
            new_vectorial_list.append(new_vectorial)
            current_x += width + step_between_letters

        step_between_rectangle_and_letters = width_mean * self.size_between_letters_and_rectangle_factor
        total_width = total_letters_width + (len(self.name) - 1) * step_between_letters
        point_a = Vector("point_a", m.floor(-step_between_rectangle_and_letters),
                         m.floor(-step_between_rectangle_and_letters))
        point_b = Vector("point_b", m.floor(total_width + step_between_rectangle_and_letters),
                         m.floor(200 + step_between_rectangle_and_letters))
        rectangle_vectorial = td.get_rectangle(point_a, point_b)
        self.total_width = td.get_width(rectangle_vectorial)
        self.total_height = td.get_height(rectangle_vectorial)

        # Creation of the vectorial that contain every character and the rectangle
        main_vectorial = []
        for vectorial in new_vectorial_list + [rectangle_vectorial]:
            for multiline in vectorial:
                main_vectorial.append(multiline)

        self.vectorial = td.get_normalised_vectorial(main_vectorial)

    def _make_input_and_output_vectorial(self):
        """
        Creation of the pictures that will be added to the unit visual
        """
        pin_size = self.total_height * self.pins_size_factor
        step_between_pins_and_main_rectangle = self.total_width * self.size_between_pins_and_rectangle_factor

        mid_height_of_picture = self.total_height / 2

        """
        Input pin
        """
        if self.input_count > 0:
            # Determination of starting height
            dist_between_input = (self.total_height - pin_size) / self.input_count
            start_height = mid_height_of_picture - dist_between_input / 2 * (self.input_count - 1)

            point_zero = Vector("po", - step_between_pins_and_main_rectangle, start_height)
            for i in range(self.input_count):
                center = Vector(f"center_{i}", m.floor(point_zero[0]),
                                m.floor(point_zero[1] + i * dist_between_input))
                self.input_coordinates_list.append(center)

                point_a = Vector("point_a", m.floor(point_zero[0] - pin_size),
                                 m.floor(point_zero[1] + i * dist_between_input - pin_size))
                point_b = Vector("point_b", m.floor(point_zero[0] + pin_size),
                                 m.floor(point_zero[1] + i * dist_between_input + pin_size))
                new_rectangle = td.get_rectangle(point_a, point_b)
                self.vectorial.append(new_rectangle[0])

        """
        Output pin
        """
        if self.output_count > 0:
            # Determination of starting height
            dist_between_output = (self.total_height - pin_size) / self.output_count
            start_height = mid_height_of_picture - dist_between_output / 2 * (self.output_count - 1)

            point_zero = Vector("po", self.total_width + step_between_pins_and_main_rectangle, start_height)
            for i in range(self.output_count):
                center = Vector(f"center_{i}", m.floor(point_zero[0]),
                                m.floor(point_zero[1] + i * dist_between_output))
                self.output_coordinates_list.append(center)

                point_a = Vector("point_a", m.floor(point_zero[0] - pin_size),
                                 m.floor(point_zero[1] + i * dist_between_output - pin_size))
                point_b = Vector("point_b", m.floor(point_zero[0] + pin_size),
                                 m.floor(point_zero[1] + i * dist_between_output + pin_size))
                new_rectangle = td.get_rectangle(point_a, point_b)
                self.vectorial.append(new_rectangle[0])

    def get_vectorial(self):
        """
        The point (0, 0) is in the bottom left corner of the main rectangle
        """
        return self.vectorial

    def get_size(self):
        """
        Return size of the picture
        """
        return self.total_width, self.total_height

    def get_input_coordinates_normalised(self) -> [Vector]:
        """
        Return a list of points representing the center of each input,
        each point's length will be divided by the height of the unit (normalisation)
        """
        new_list = []
        for point in self.input_coordinates_list:
            new_list.append(point / self.total_height)
        return new_list

    def get_output_coordinates_normalised(self) -> [Vector]:
        """
        Return a list of points representing the center of each output,
        each point's length will be divided by the height of the unit (normalisation)
        """
        new_list = []
        for point in self.output_coordinates_list:
            new_list.append(point / self.total_height)
        return new_list


"""
Example
"""
if __name__ == '__main__':
    # Creation of the unit visual
    wanted_height = 50
    test = UnitVisual("and", 2, 1,
                      0.5, 0.7,
                      0.1, 0.1, )

    # Creation of the image
    im = np.ones((120, 55, 3), dtype=np.uint8) * 255

    # Drawing the unit on the image
    start_point = Vector("po", 20, 2)
    td.trace_picture(im, test.get_vectorial(), start_point, wanted_height, (0, 0, 0))

    # Drawing points on the image
    for coord in test.get_input_coordinates_normalised() + test.get_output_coordinates_normalised():
        coord *= wanted_height
        pos = coord.get_floored_vector()
        td.trace_line(im, pos + start_point, pos + start_point, (0, 0, 0))

    # Image showing
    im = td.rotate_90(im)
    plt.imshow(im)
    plt.show()
