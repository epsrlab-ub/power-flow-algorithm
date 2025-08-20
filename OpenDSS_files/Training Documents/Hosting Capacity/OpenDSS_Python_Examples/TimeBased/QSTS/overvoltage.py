# -*- coding: utf-8 -*-
# @Time    : 7/22/2023 2:19 PM
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
dss.text(
    "new loadshape.gen "
    "npts=24 "
    "interval=1 "
    "mult=[0 0 0 0 0 0 .1 .2 .3  .5  .8  .9  1.0  1.0  .99  .9  .7  .4  .1 0  0  0  0  0]")

dss.text("edit generator.gen daily=gen")
dss.text("New monitor.v_gen element=generator.gen terminal=1 mode=0")

v_gen_penetration = dict()
# Hosting Capacity Loop
i = 0
HCSteps.step_kw = 100
while i * HCSteps.step_kw < HCSteps.max_kw:
    i = i + 1
    i_kw = i * HCSteps.step_kw
    gen_kw = {"gen": i_kw}

    HCSteps.increase_gen(dss, gen_kw)

    HCSteps.solve_qsts(dss)

    dss.monitors.name = "v_gen"
    v_gen_penetration[i_kw] = [v / (kv / np.sqrt(3)) / 1000.0 for v in dss.monitors.channel(1)]

    if HCSteps.check_qsts_overvoltage_violation(dss):
        hosting_capacity_value = (i - 1) * HCSteps.step_kw
        break


plt.rcParams.update({
    'font.size': 12,       # Set the font size for all text elements
    'axes.labelsize': 12,  # Set the font size for axis labels
    'axes.titlesize': 14,  # Set the font size for titles (if used)
    'xtick.labelsize': 10, # Set the font size for x-axis tick labels
    'ytick.labelsize': 10,  # Set the font size for y-axis tick labels
    'legend.title_fontsize': 7
})

plt.figure(num=1, figsize=(5, 4))
for pen, v_gen in v_gen_penetration.items():
    if pen in [100, 1000, 2000, 2500, 2600]:
        plt.scatter(range(1, 25), v_gen, label=pen / 1000)
plt.xlabel("Time (Hour)")
plt.ylabel("Voltage (pu)")
plt.axhline(y=1.05, c="red")
plt.axhline(y=0.95, c="red")
plt.title(f"Bus 4 Voltage for Different Penetration Levels")
plt.ylim([0.92, 1.08])
plt.legend(fontsize=6, title="Penetration Level (MW)")

plt.savefig(pathlib.Path(script_path).joinpath('QSTS.png'), dpi=300, transparent=True)

dss.loadshapes.name = "gen"
load_mults = dss.loadshapes.p_mult

plt.figure(num=2, figsize=(5, 4))
plt.scatter(range(1, 25), load_mults)
plt.xlabel("Time (Hour)")
plt.ylabel("Gen Multiplier (pu)")
plt.title(f"Generation Profile")
plt.ylim(0, 1)

plt.savefig(pathlib.Path(script_path).joinpath('gen_profile.png'), dpi=300, transparent=True)

print(f"Hosting Capacity: {hosting_capacity_value} MW")
