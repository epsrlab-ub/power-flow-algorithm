# -*- coding: utf-8 -*-
# @Time    : 7/22/2023 2:49 PM
# @Author  : Paulo Radatz
# @Email   : pradatz@epri.com
# @File    : overvoltage.py
# @Software: PyCharm

import py_dss_interface
import os
import pathlib
import numpy as np
import matplotlib.pyplot as plt

from HCWebinar.hc_steps import HCSteps

script_path = os.path.dirname(os.path.abspath(__file__))
dss_file = pathlib.Path(script_path).joinpath("../../feeders", "8bus", "Master.dss")
dss = py_dss_interface.DSS()

hc_hour_results = dict()
for hour in range(24):
    # Compile OpenDSS feeder model
    dss.text(f"compile [{dss_file}]")

    # Set Feeder Condition
    dss.text("new loadshape.lp npts=24 interval=1 mult=(file=load_profile.csv)")
    dss.text("batchedit load..* daily=lp")

    # Calculate HC for bus 4
    bus = "4"
    dss.circuit.set_active_bus(bus)
    kv = dss.bus.kv_base * np.sqrt(3)

    gen_bus = {"gen": dss.bus.name}
    gen_kv = {"gen": kv}

    # Add generator at bus
    HCSteps.add_gen(dss, gen_bus, gen_kv)

    # Hosting Capacity Loop
    i = 0
    while i * HCSteps.step_kw < HCSteps.max_kw:
        i = i + 1
        i_kw = i * HCSteps.step_kw
        gen_kw = {"gen": i_kw}

        HCSteps.increase_gen(dss, gen_kw)

        dss.text("set mode=daily")
        dss.text("set number=1")
        dss.text("set stepsize=1h")
        dss.text(f"set hour={hour}")  # OpenDSS solves hour + setpsize
        HCSteps.solve_powerflow(dss)

        if HCSteps.check_overvoltage_violation(dss):
            hosting_capacity_value = (i - 1) * HCSteps.step_kw
            hc_hour_results[hour] = hosting_capacity_value / 1000.0
            break

plt.rcParams.update({
    'font.size': 12,       # Set the font size for all text elements
    'axes.labelsize': 12,  # Set the font size for axis labels
    'axes.titlesize': 14,  # Set the font size for titles (if used)
    'xtick.labelsize': 10, # Set the font size for x-axis tick labels
    'ytick.labelsize': 10  # Set the font size for y-axis tick labels
})

plt.figure(num=1, figsize=(5, 4))
plt.scatter(range(1, 25), hc_hour_results.values())
plt.xlabel("Time (Hour)")
plt.ylabel("Hosting Capacity (MW)")
plt.title(f"Generation Time-Series Hosting Capacity of Bus 4")
plt.ylim(0, 3)

plt.savefig(pathlib.Path(script_path).joinpath('TSHC.png'), dpi=300, transparent=True)

dss.loadshapes.name = "lp"
load_mults = dss.loadshapes.p_mult

plt.figure(num=2, figsize=(5, 4))
plt.scatter(range(1, 25), load_mults)
plt.xlabel("Time (Hour)")
plt.ylabel("Load Multiplier (pu)")
plt.title(f"Load Profile for All Loads")
plt.ylim(0, 1)

plt.savefig(pathlib.Path(script_path).joinpath('load_profile.png'), dpi=300, transparent=True)
