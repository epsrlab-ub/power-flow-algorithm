# -*- coding: utf-8 -*-
# @Time    : 7/19/2023 12:40 PM
# @Author  : Paulo Radatz
# @Email   : pradatz@epri.com
# @File    : feeder_condition.py
# @Software: PyCharm

import py_dss_interface


class FeederCondition:

    @classmethod
    def set_load_level_condition(cls, dss: py_dss_interface.DSS, load_mult: float):
        dss.text(f"set loadmult={load_mult}")

    @classmethod
    def consider_existing_gen(cls, dss: py_dss_interface.DSS):
        dss.text("batchedit generator..* enabled=yes")
