"""
Objective: Simulate energy perdition due to atmosphere
Creator: XenonEGG

using: python 3.6
encoding: utf-8
"""

import matplotlib.pyplot as plt
import math as m


wc = 11         # puissance d'entrée du laser
kl = 0.001      # rendement du laser
ku = 0.12       # rendement cellule photovoltaïque
d = 10          # distance laser - cellule

ka = 0.01       # coefficient en rapport avec l'air


def calc_wi(wl, ka, d):
    #return wl
    return wl * (1 - m.exp(-1/(ka * d)))


def calc_wu(wc, kl, ka, ku, d):
    wl = wc * kl
    wi = calc_wi(wl, ka, d)
    wu = wi * ku
    return wu


def make_decade(ten_pow: int):
    decade = []
    for i in range(1, 10):
        num = i * 10 ** ten_pow
        decade.append(num)
    return decade

def make_multiple_decade(ten_pow_start: int, ten_pow_end: int):
    decades = []
    for ten_pow in range(ten_pow_start, ten_pow_end):
        decade = make_decade(ten_pow)
        decades += decade
    return decades


ka_list = [0.001, 0.01, 0.1, 1, 10]
d_list = make_multiple_decade(-3, 2)
for ka in ka_list:
    wu_list = []
    rend_list = []
    for d in d_list:
        wu = calc_wu(wc, kl, ka, ku, d)
        rend = wu / wc * 100
        wu_list.append(wu)
        rend_list.append(rend)
    plt.plot(d_list, rend_list, label=f"ka = {ka}")

plt.legend(loc="best")
plt.show()
