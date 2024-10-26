"""
Objective: Make a way to solve mathematical functions
Creator: XenonEGG

using: python 3.6
encoding: utf-8
"""

import numpy as np
import matplotlib.pyplot as plt

# Solve f(x) = 0


def zero(f, a: float, b: float, accuracy=10**-8):
    if abs(f(a)) < accuracy:
        return a

    c = (a + b) / 2
    if f(a) * f(c) < 0:
        return zero(f, a, c, accuracy)
    else:
        return zero(f, c, b, accuracy)


def newton(f, fp, a: float, accuracy=10**-8):
    x = a
    while abs(f(x)) > accuracy:
        y = f(x)
        der = fp(x)
        x -= y / der
    return x


# Get integral


def square_right(f, a: float, b: float, n=10):
    step = (b - a) / n
    sum = 0
    for i in range(n):
        sum += step * f(a + i * step)
    return sum


def square_left(f, a: float, b: float, n=10):
    step = (b - a) / n
    sum = 0
    for i in range(n):
        sum += step * f(a + (i+1) * step)
    return sum


def square_mid(f, a: float, b: float, n=10):
    step = (b - a) / n
    sum = 0
    for i in range(n):
        sum += step * f(a + (i+1/2) * step)
    return sum


def trapeze(f, a: float, b: float, n=10):
    step = (b - a) / n
    sum = 0
    for i in range(n):
        k1 = step * f(a + i * step)
        k2 = step * f(a + (i+1) * step)
        sum += (k1 + k2) / 2
    return sum


def simpson(f, a: float, b: float, n=10):
    step = (b - a) / n
    sum = 0
    for i in range(n):
        k1 = step * f(a + i * step)
        k2 = step * f(a + (i+1) * step)
        k3 = step * f(a + (i+1/2) * step)
        sum += (k1 + k2 + k3 * 4) / 6
    return sum


# Get integral of a 1 dimension differential equation

def integral_equation_diff(f, y0: float, t: list):
    y = [y0]
    for i in range(1, len(t)):
        time_step = t[i] - t[i-1]
        ly = y[-1]
        lder = f(ly)
        ny = ly + time_step * lder
        y.append(ny)
    return y


# Get integral of a n dimension differential equation

def integral_equation_diff_n(fp, y0: list, t: list):
    y = np.zeros((len(t), len(y0)))
    y0 = np.array(y0)
    y[0] = y0
    for i in range(1, len(t)):
        time_step = t[i] - t[i-1]
        ly = y[i-1]
        lder = np.array(fp(ly))
        ny = ly + time_step * lder
        y[i] = ny
    return y


def fp(ly):
    k1 = 5
    k2 = 3
    k3 = 1
    a = ly[0]
    b = ly[1]
    c = ly[2]
    if a < 0:
        a = 0
    if b < 0:
        b = 0
    if c < 0:
        c = 0
    return -np.sqrt(k1*a), 2 * np.sqrt(k1*a) - k2*b - k3*b*c, k2*b - k3*b*c, k3*b*c


def differential_calcul(differential_coefficients: list, initial_conditions: list, nb_rows: int, simulation_time: float,
                        second_member_constant: float):
    """
    The differential equation need to give a unitary polynom in the characteristic equation
    """
    assert len(differential_coefficients) == len(initial_conditions) - 1, "Only nb_column-1 coefficients are needed"

    # Init
    dt = simulation_time / nb_rows

    # Creation of the board
    nb_column = len(initial_conditions)
    board = np.zeros((nb_rows, nb_column))

    # Differential equation motor
    def f(previous_row):
        previous_row = list(previous_row)
        greatest_derivation_value = second_member_constant
        for i in range(len(differential_coefficients)):
            current_coefficient = differential_coefficients[i]
            greatest_derivation_value -= current_coefficient * previous_row[i]
        new_row = previous_row[:-1].copy()
        new_row.append(greatest_derivation_value)
        return new_row

    # Board filling
    board[0] = initial_conditions
    # From row 1 to last row
    for i in range(1, nb_rows):
        next_row = f(board[i-1])

        # From last column-1 to first column
        for j in range(nb_column-2, -1, -1):
            j_value = board[i-1][j] + next_row[j+1] * dt
            next_row[j] = j_value
        board[i] = next_row
    return board


def get_f(board):
    n, m = board.shape
    l = []
    for i in range(n):
        l.append(board[i][0])
    return l


nb_lig = 1000
time = 20
boardd = differential_calcul([1], [5, 0], nb_lig, time, 0)
print(boardd)

y = get_f(boardd)

x = np.linspace(0, time, nb_lig)

plt.plot(x, y)
plt.show()
