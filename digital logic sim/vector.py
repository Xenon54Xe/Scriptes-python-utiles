"""
Objective: Make a class to represent mathematical vectors
Creator: XenonEGG

using: python 3.6
encoding: utf-8
"""
import math
import math as m


class Vector:
    def __init__(self, name: str, x: float, y: float):
        """
        A class representing mathematical vector
        """
        self.name = name
        self.x = x
        self.y = y

    def get_name(self):
        return self.name

    def get_x(self):
        """
        Return the x coordinate of the vector
        """
        return self.x

    def get_y(self):
        """
        Return the y coordinate of the vector
        """
        return self.y

    def get_coordinates(self):
        """
        Return the coordinates of the vector
        """
        return self.x, self.y

    def get_floored_vector(self):
        """
        Return a vector with the floored coordinates of this vector
        """
        return Vector("floored", m.floor(self.x), m.floor(self.y))

    def get_length(self):
        """
        Return the length of the vector
        """
        return math.sqrt(self.x ** 2 + self.y ** 2)

    def __add__(self, other):
        """
        Two vector can be added together
        """
        x = self.x + other.get_x()
        y = self.y + other.get_y()
        name_a = self.name
        name_b = other.get_name()
        return Vector(f"{name_a}+{name_b}", x, y)

    def __sub__(self, other):
        """
        The second vector will sub his coordinates to the first
        """
        x = self.x - other.get_x()
        y = self.y - other.get_y()
        name_a = self.name
        name_b = other.get_name()
        return Vector(f"{name_a}-{name_b}", x, y)

    def __mul__(self, other: float):
        """
        A vector can be multiplied by a scalar
        """
        x = self.x * other
        y = self.y * other
        return Vector(self.name, x, y)

    def __truediv__(self, other: float):
        """
        A vector is always divided by a scalar
        """
        x = self.x / other
        y = self.y / other
        return Vector(self.name, x, y)

    def get_normalised(self):
        """
        Normalise the vector (set his length to 1)
        """
        assert self.x != 0 or self.y != 0, "The null vector can't be normalised !"
        return self / self.get_length()

    def __getitem__(self, item):
        """
        Return the coordinates of the vector like a list
        """
        if item == 0:
            return self.x
        elif item == 1:
            return self.y
        else:
            raise Exception("Indexes possibles: 0 et 1")

    def __repr__(self):
        """
        Represent a vector in a print
        """
        return f"({self.x}, {self.y})"
