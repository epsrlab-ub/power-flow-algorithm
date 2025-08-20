# -*- coding: utf-8 -*-
# @Time    : 7/22/2023 12:47 PM
# @Author  : Paulo Radatz
# @Email   : pradatz@epri.com
# @File    : d_calculation.py
# @Software: PyCharm

import py_dss_interface
import os
import pathlib
import numpy as np
import cmath

from HCWebinar.feeder_condition import FeederCondition


def solve_quadratic_equation(A, B, C):
    # Calculate the discriminant
    discriminant = B**2 - 4*A*C

    # Check if the discriminant is non-negative (real roots) or negative (complex roots)
    if discriminant >= 0:
        # Calculate real roots
        root1 = (-B + cmath.sqrt(discriminant)) / (2*A)
        root2 = (-B - cmath.sqrt(discriminant)) / (2*A)
        return abs(root1), abs(root2)
    else:
        # Calculate complex roots
        root1 = (-B + cmath.sqrt(discriminant)) / (2*A)
        root2 = (-B - cmath.sqrt(discriminant)) / (2*A)
        return root1, root2

script_path = os.path.dirname(os.path.abspath(__file__))
dss_file = pathlib.Path(script_path).joinpath("../feeders", "8bus", "Master.dss")
dss = py_dss_interface.DSS()

# Compile OpenDSS feeder model
dss.text(f"compile [{dss_file}]")

# Set Feeder Condition
FeederCondition.set_load_level_condition(dss, load_mult=0.2)

# Calculate HC for bus 4
bus = "4"
dss.circuit.set_active_bus(bus)
kv = dss.bus.kv_base * np.sqrt(3)

for element in dss.circuit.elements_names:
    if element.split(".")[0].lower() in ["line", "transformer"]:
        dss.circuit.set_active_element(element)
        if dss.cktelement.bus_names[1].split(".")[0].lower() == bus:
            break

dss.text("solve")

# ATTENTION: The direct calculation must be applied for all elements between feederhead and der location
# In this particular example, it is enough to apply only in the first upstream element of the generator bus.
# Looking at terminal 1 (could look at 2 as well)
powers = dss.cktelement.powers
sa = np.sqrt(powers[0] ** 2 + powers[1] ** 2)
sb = np.sqrt(powers[2] ** 2 + powers[3] ** 2)
sc = np.sqrt(powers[4] ** 2 + powers[5] ** 2)

s = [sa, sb, sc]
index_min = min(range(len(s)), key=lambda i: s[i])
p_thermal_gen = powers[0 + 2 * index_min]
q_thermal_gen = powers[1 + 2 * index_min]

s_rating = dss.cktelement.norm_amps * kv / np.sqrt(3)  # Rating power of one phase

# Assuming generator with pf = 1 then Q = 0
# s_rating ** 2 =  (p_thermal_gen - P) ** 2 + (q_thermal_gen - Q)**2
A = 1
B = - 2 * p_thermal_gen
C = p_thermal_gen ** 2 + q_thermal_gen ** 2 - s_rating ** 2
solution1, solution2 = solve_quadratic_equation(A, B, C)

hosting_capacity_value = max([solution1, solution2]) * 3

print(f"Thermal HC generation = {hosting_capacity_value}")


