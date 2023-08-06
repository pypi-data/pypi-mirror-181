# Copyright (c) 2022 International Institute for Applied Systems Analysis.
# All rights reserved. The use and distribution terms for this software
# are covered by the MIT License (http://opensource.org/licenses/MIT)
# which can be found in the file LICENSE at the root of this distribution.
# By using this software in any fashion, you are agreeing to be bound by
# the terms of this license.
# You must not remove this notice, or any other, from this software.
"""Climate module equations from Hansel et al. (2020).

Climate module includes:

1) carbon cycle representation from the FAIR climate model (Smith et al. 2018),

2) energy balance model based on Geoffroy (2013) with dynamic non-CO2 forcings.
"""

__author__ = "Anna Shchiptsova"
__copyright__ = "Copyright (c) 2022 IIASA"
__license__ = "MIT"

from functools import reduce
import numpy as np                  # type: ignore
from scipy.optimize import brentq   # type: ignore
from . import parameters as pars


def _co2_to_c(co2):
    """Convert GtCO2 to GtC."""
    return co2 / 3.666


def _init_emissions(e_co2):
    """Calculate cumulative net CO2 emissions curve (GtC)."""
    ecum_c = np.zeros(e_co2.size)
    ecum_c[0] = pars.ECUM0
    for idx in range(1, e_co2.size):
        ecum_c[idx] = ecum_c[idx - 1] + _co2_to_c(e_co2[idx - 1]) * pars.DT

    return ecum_c


def _iirf_equation(alpha, ecum_c, c_co2, temp_atm):
    """Equation of the 100-year average airborne fraction of a pulse of CO2."""
    iirf1 = pars.R0 + pars.RC * (ecum_c - (c_co2 - pars.C_CO2_EQ)) + \
        pars.RT * temp_atm
    iirf2 = alpha * (np.sum(pars.A * pars.TAU *
                            (1 - np.exp(-100 / (pars.TAU * alpha)))))

    return iirf2 - iirf1


def _carbon_concentration(carbon_boxes):
    """Calculate carbon concentration in atmosphere (GtC)."""
    return np.sum(carbon_boxes) + pars.C_CO2_EQ


def _carbon_cycle(e_co2, ecum_c, c_co2, temp_atm, carbon_boxes):
    """Carbon cycle model."""
    alpha = brentq(_iirf_equation, 0.01, 100, args=(ecum_c, c_co2, temp_atm))

    carbon_boxes_next = np.zeros(carbon_boxes.size)
    for idx1 in range(carbon_boxes.size):
        step = 0
        for idx2 in range(5):
            step += np.exp(- (pars.DT - idx2) / (alpha * pars.TAU[idx1]))

        carbon_boxes_next[idx1] = carbon_boxes[idx1] * \
            np.exp(-pars.DT / (alpha * pars.TAU[idx1])) + \
            pars.A[idx1] * _co2_to_c(e_co2) * step

    c_co2_next = _carbon_concentration(carbon_boxes_next)

    return c_co2_next, carbon_boxes_next, alpha


def _energy_balance_model(
    c_co2,
    other_rf,
    absolute_other_rf,
    temp_atm,
        temp_lo):
    """Energy balance model with dynamic non-CO2 forcings."""
    co2_rf = (pars.KAPPA / np.log(2.)) * np.log(c_co2 / pars.C_CO2_EQ)

    if absolute_other_rf:
        total_rf = co2_rf + other_rf
    else:
        total_rf = (1 + other_rf) * co2_rf

    temp_atm_next = reduce(
        lambda y, idx: y + 1 / pars.XI1 * (total_rf - pars.XI2 * y - pars.XI3 *
                                           (y - temp_lo)),
        range(4),
        temp_atm)

    temp_lo_next = temp_lo + pars.DT * pars.XI3 / pars.XI4 * \
        (temp_atm - temp_lo)

    return temp_atm_next, temp_lo_next


def climate_module(e_co2, other_rf, absolute_other_rf):
    """Temperature and carbon concentration pathways from Hansel et al. (2020).

    Climate module can be run either with given absolute non-CO2 forcings or
    with given ratio of non-CO2 to CO2 forcings.
    """
    ecum_c = _init_emissions(e_co2)
    c_co2 = np.zeros(e_co2.size)
    temp_atm = np.zeros(e_co2.size)

    alpha = np.zeros(e_co2.size - 1)

    carbon_boxes = pars.CARBON_BOXES0
    c_co2[0] = _carbon_concentration(carbon_boxes)
    temp_atm[0] = pars.TAT0
    temp_lo = pars.TLO0
    for idx in range(e_co2.size - 1):
        c_co2[idx + 1], carbon_boxes, alpha[idx] = _carbon_cycle(
            e_co2[idx],
            ecum_c[idx],
            c_co2[idx],
            temp_atm[idx],
            carbon_boxes)
        temp_atm[idx + 1], temp_lo = _energy_balance_model(
            c_co2[idx + 1],
            other_rf[idx + 1],
            absolute_other_rf,
            temp_atm[idx],
            temp_lo)

    return temp_atm, c_co2
