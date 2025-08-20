# -*- coding: utf-8 -*-
# @Time    : 7/22/2023 9:08 AM
# @Author  : Paulo Radatz
# @Email   : pradatz@epri.com
# @File    : load_thermal.py
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

# Compile OpenDSS feeder model
dss.text(f"compile [{dss_file}]")

# Set Feeder Condition
FeederCondition.set_load_level_condition(dss, load_mult=1)

# Calculate HC for bus 4
bus = "4"
dss.circuit.set_active_bus(bus)
kv = dss.bus.kv_base * np.sqrt(3)

load_bus = {"load": dss.bus.name}
load_kv = {"load": kv}

# Add generator at bus
HCSteps.add_load(dss, load_bus, load_kv)

# Hosting Capacity Loop
i = 0
while i * HCSteps.step_kw < HCSteps.max_kw:
    i = i + 1
    i_kw = i * HCSteps.step_kw
    load_kw = {"load": i_kw}

    HCSteps.increase_load(dss, load_kw)

    HCSteps.solve_powerflow(dss)

    if HCSteps.check_thermal_violation(dss):
        hosting_capacity_value = (i - 1) * HCSteps.step_kw
        break

# Print out results of simulation
print(HCSteps.result_centralized_info(bus,
                                      "thermal load",
                                      hosting_capacity_value,
                                      "offpeak",
                                      False,
                                      "Load"))