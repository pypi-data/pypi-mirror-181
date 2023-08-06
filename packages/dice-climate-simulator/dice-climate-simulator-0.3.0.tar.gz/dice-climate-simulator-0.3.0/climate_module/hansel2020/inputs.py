# Copyright (c) 2022 International Institute for Applied Systems Analysis.
# All rights reserved. The use and distribution terms for this software
# are covered by the MIT License (http://opensource.org/licenses/MIT)
# which can be found in the file LICENSE at the root of this distribution.
# By using this software in any fashion, you are agreeing to be bound by
# the terms of this license.
# You must not remove this notice, or any other, from this software.
"""Net CO2 emissions and radiative forcing curves from Hansel et al. (2020)."""

__author__ = "Anna Shchiptsova"
__copyright__ = "Copyright (c) 2022 IIASA"
__license__ = "MIT"

import numpy as np  # type: ignore

#: Net CO2 FFI emissions curve (GtCO2).
emissions_ffi_co2 = np.array([
    35.7404, 37.6787, 29.0282, 29.4648, 29.4406,
    28.9376, 27.9357, 26.4317, 24.4262, 21.931,
    18.9743, 15.5854, 11.7991, 7.6487, 3.16449,
    -1.62853, -6.71595, -12.1001])

#: Curve with ratios of non-CO2 radiative forcing to CO2 radiative forcing (-).
radiative_forcing_non_co2 = np.array([
    0.31, 0.455, 0.514, 0.58, 0.586,
    0.592, 0.562, 0.533, 0.496, 0.462,
    0.443, 0.425, 0.411, 0.397, 0.382,
    0.367, 0.352, 0.337])


def emissions_land_use_co2(n_points):
    """AFOLU emissions (GtCO2)."""
    e_points = np.zeros(n_points)
    e_points[0] = 2.6

    for x_points in range(1, n_points):
        e_points[x_points] = e_points[x_points - 1] * (1 - 0.115)

    return e_points
