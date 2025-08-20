# -*- coding: utf-8 -*-
# @Time    : 7/19/2023 12:30 PM
# @Author  : Paulo Radatz
# @Email   : pradatz@epri.com
# @File    : fixed_allocation_1.py
# @Software: PyCharm

import py_dss_interface
import os
import pathlib
import numpy as np

from HCWebinar.hc_steps import HCSteps
from HCWebinar.feeder_condition import FeederCondition

script_path = os.path.dirname(os.path.abspath(__file__))
dss_file = pathlib.Path(script_path).joinpath("../feeders", "8bus", "Master.dss")
dss = py_dss_interface.DSS()

# Set Feeder Model
dss.text(f"compile [{dss_file}]")
FeederCondition.set_load_level_condition(dss, load_mult=0.2)

# Add Generation at bus 4
bus = "4"
dss.circuit.set_active_bus(bus)
kv = dss.bus.kv_base * np.sqrt(3)

gen_bus = {"gen": dss.bus.name}
gen_kv = {"gen": kv}

HCSteps.add_gen(dss, gen_bus, gen_kv)

# Hosting Capacity Loop
i = 0
while i * HCSteps.step_kw < HCSteps.max_kw:
    i = i + 1
    i_kw = i * HCSteps.step_kw
    gen_kw = {"gen": i_kw}

    # Set Penetration Level
    HCSteps.increase_gen(dss, gen_kw)

    # Perform Power flow
    HCSteps.solve_powerflow(dss)

    # Violation?
    if HCSteps.check_overvoltage_violation(dss):
        hosting_capacity_value = (i - 1) * HCSteps.step_kw
        break

# Print out results of simulation
print(HCSteps.result_centralized_info(bus,
                                      "Overvoltage",
                                      hosting_capacity_value,
                                      "offpeak",
                                      False,
                                      "Generator"))