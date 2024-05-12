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


y0 = [1.4, 0, 0, 0]
t = np.linspace(0, 2, 10000)
y = integral_equation_diff_n(fp, y0, t)
plt.plot(t, y[:, 0])
plt.plot(t, y[:, 1])
plt.plot(t, y[:, 2])
plt.plot(t, y[:, 3])
plt.legend("abcd")
plt.show()
