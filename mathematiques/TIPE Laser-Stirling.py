"""
Objective: Simulate energy reception of a stirling motor
Creator: XenonEGG

using: python 3.6
encoding: utf-8
"""

import math

laser_w0 = 13000                    # puissance laser entrée (W)
laser_rdt = 0.33                    # rendement laser
metal_m = 0.025                     # masse du metal a chauffer (kg)
metal_cv = 900                      # capacité thermique massique du métal (J.M-1.T-1) (en J.kg-1.K-1)

energy_flux = laser_w0 * laser_rdt  # flux d'énergie venant de la source chaude (J)
temp_flux = energy_flux / (metal_m * metal_cv)      # température ajoutée par seconde (K.s-1)

hot_temp = 273                      # température source chaude (initial) (K)
cold_temp = 273                     # température source froide (initial) (K)

volume_2 = 0.1 * 10 ** -3           # petit volume (m3)
volume_1 = 0.5 * 10 ** -3           # grand volume (m3)

gaz_mole = 1                        # qte du gaz dans le moteur (mole)


# Rendement du moteur
def get_rdt_motor(cold_temp, hot_temp):
    return 1 - cold_temp / hot_temp


"""
def w(tf, tc):
    return n * 8.314 * math.log(v1 / v2) - n * 8.314 * math.log(v1 / v2)

"""
