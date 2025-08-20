# -*- coding: utf-8 -*-
# @Time    : 7/18/2023 4:05 PM
# @Author  : Paulo Radatz
# @Email   : pradatz@epri.com
# @File    : hc_steps.py
# @Software: PyCharm

import py_dss_interface
import pandas as pd
import os
import pathlib
from typing import List

script_path = os.path.dirname(os.path.abspath(__file__))

class HCSteps:

    max_kw = 10000
    step_kw = 100
    ov_threshold = 1.05
    uv_threshold = 0.95
    themal_limit_per = 100

    @classmethod
    def add_gen(cls, dss: py_dss_interface.DSS, gen_bus: dict, gen_kv: dict):
        for gen in gen_bus.keys():
            dss.text(f"new generator.{gen} "
                     f"phases=3 bus1={gen_bus[gen]} kv={gen_kv[gen]} "
                     f"kw=0.0001 pf=1 Vminpu=0.7 Vmaxpu=1.2")

    @classmethod
    def change_gen_pf(cls, dss: py_dss_interface.DSS, gen_pf: dict):
        for gen, pf in gen_pf.items():
            dss.text(f"edit generator.{gen} pf={pf}")

    @classmethod
    def increase_gen(cls, dss: py_dss_interface.DSS, gen_kw: dict):
        for gen, kw in gen_kw.items():
            dss.text(f"Edit generator.{gen} kw={kw}")

    @classmethod
    def add_load(cls, dss: py_dss_interface.DSS, load_bus: dict, load_kv: dict):
        for load in load_bus.keys():
            dss.text(f"new load.{load} "
                     f"phases=3 bus1={load_bus[load]} kv={load_kv[load]} "
                     f"kw=0.0001 pf=1 Vminpu=0.7 Vmaxpu=1.2 status=Fixed")

    @classmethod
    def increase_load(cls, dss: py_dss_interface.DSS, load_kw: dict):
        for load, kw in load_kw.items():
            dss.text(f"Edit load.{load} kw={kw}")

    @classmethod
    def add_fixed_size_gen(cls, dss: py_dss_interface.DSS, bus: str, kv: float, kw: float):
        dss.text(f"new generator.gen_{bus} "
                 f"phases=3 bus1={bus} kv={kv} "
                 f"kw={kw} pf=1 Vminpu=0.7 Vmaxpu=1.2")

    @classmethod
    def solve_powerflow(cls, dss: py_dss_interface.DSS):
        dss.text("solve")

    @classmethod
    def solve_qsts(cls, dss: py_dss_interface.DSS):
        dss.text("set demandinterval=True")
        dss.text("set voltexceptionreport=True")
        dss.text("set overloadreport=True")

        dss.text("set mode=daily")
        dss.text("set number=24")
        dss.text("set stepsize=1h")
        dss.text("solve")

        dss.text("closeDI")

    @classmethod
    def check_overvoltage_violation(cls, dss: py_dss_interface.DSS):
        violation = False
        voltages = dss.circuit.buses_vmag_pu
        max_voltage = max(voltages)

        if max_voltage > cls.ov_threshold:
            violation = True

        return violation

    @classmethod
    def check_undervoltage_violation(cls, dss: py_dss_interface.DSS):
        violation = False
        voltages = dss.circuit.buses_vmag_pu
        min_voltage = min(voltages)

        if min_voltage < cls.uv_threshold:
            violation = True

        return violation

    @classmethod
    def check_thermal_violation(cls, dss: py_dss_interface.DSS):
        violation = False

        for element in dss.circuit.elements_names:
            if element.split(".")[0].lower() in ["line", "transformer"]:
                dss.circuit.set_active_element(element)
                current = dss.cktelement.currents_mag_ang
                rating_current = dss.cktelement.norm_amps

                # Consider currents in both terminals of line and first terminal of transformer (could improve it for transformer)
                if element.split(".")[0].lower() in "line":
                    num_terminal = 1
                elif element.split(".")[0].lower() in "transformer":
                    num_terminal = 1

                if max(current[:int(len(current) * num_terminal / 2):2]) / rating_current > cls.themal_limit_per / 100.0:
                    violation = True
                    return violation

        return violation

    @classmethod
    def check_qsts_overvoltage_violation(cls, dss: py_dss_interface.DSS):
        violation = False
        di_voltexceptions_1_file = pathlib.Path(script_path).joinpath("feeders", "8bus", "source", "DI_yr_0",
                                                                      "DI_VoltExceptions_1.csv")

        voltage_results_df = pd.read_csv(di_voltexceptions_1_file, index_col=0)

        if not (voltage_results_df[' "Overvoltage"'] > 0).any() or \
                (voltage_results_df[' "Undervoltages"'] > 0).any() or \
                (voltage_results_df[' "LV Overvoltage"'] > 0).any() or \
                (voltage_results_df[' "LV Undervoltages"']).any():

            return violation
        else:
            violation = True
            return violation

    @classmethod
    def result_centralized_info(cls, bus: str, metric: str, hc_value: float, load_condition: str, existing_gen: bool, device_type: str):
        info = f"""Summary of the Centralized Hosting Capacity Analysis

Feeder Conditions:
    Load level condition = {load_condition}
    Existing Gen considered = {existing_gen}

Hosting Capacity:
    Bus = {bus}
    Value = {hc_value} MW
    Device Type = {device_type}
    Metric = {metric}"""

        return info

    @classmethod
    def result_distributed_info(cls, buses: List[str], metric: str, hc_value: float, load_condition: str, existing_gen: bool,
                                device_type: str):
        info = f"""Summary of the Centralized Hosting Capacity Analysis

Feeder Conditions:
    Load level condition = {load_condition}
    Existing Gen considered = {existing_gen}

Hosting Capacity:
    Buses = {buses}
    Value = {hc_value} MW
    Device Type = {device_type}
    Metric = {metric}"""

        return info