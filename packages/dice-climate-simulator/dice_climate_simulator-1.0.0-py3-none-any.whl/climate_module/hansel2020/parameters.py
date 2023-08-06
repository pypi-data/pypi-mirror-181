# Copyright (c) 2022 International Institute for Applied Systems Analysis.
# All rights reserved. The use and distribution terms for this software
# are covered by the MIT License (http://opensource.org/licenses/MIT)
# which can be found in the file LICENSE at the root of this distribution.
# By using this software in any fashion, you are agreeing to be bound by
# the terms of this license.
# You must not remove this notice, or any other, from this software.
"""Climate module parameters.

Climate module parameters include initial values (Hansel et al. 2020;
DICE2016), parameters of carbon cycle (Smith et al. 2018; Hansel et al. 2020)
and parameters of energy balance model (Hansel et al. 2020).
"""

__author__ = "Anna Shchiptsova"
__copyright__ = "Copyright (c) 2022 IIASA"
__license__ = "MIT"

import numpy as np  # type: ignore


#: General:
#: years per period.
DT = 5

#: Initial cumulative CO2 emissions (GtCO2).
ECUM0 = 400 + 197

#: Initial atmospheric temperature change (°C from 1900);
#: adjusted to only include athropogenic forcing.
TAT0 = 1.243

#: Initial lower stratum temperature change (°C from 1900);
#: adjusted to only include athropogenic forcing.
TLO0 = 0.324

#: Carbon cycle:
#: pre-industrial time-integrated airborne fraction of CO2 (yr).
R0 = 35.0

#: Carbon cycle:
#: change in time-integrated airborne fraction with CO2 (yr/GtC).
RC = 0.019

#: Carbon cycle:
#: change in time-integrated airborne fraction with temperature
#: (yr/K).
RT = 4.165

#: Carbon cycle:
#: partition coefficient of carbon boxes.
A = np.array([0.217, 0.224, 0.282, 0.276])

#: Carbon cycle:
#: present-day decay time constants of CO2 (yr).
TAU = np.array([1000000, 394.4, 36.54, 4.304])

#: Carbon cycle:
#: box parameters.
CARBON_BOXES0 = np.array([127.159, 93.313, 37.840, 7.721])

#: Carbon cycle:
#: equilibrium concentration in atmosphere (GtC).
C_CO2_EQ = 588

#: Energy balance model:
#: equilibrium temperature impact (°C per doubling C02).
NU = 3.1

#: Energy balance model:
#: forcings of equilibrium CO2 doubling (Wm-2)
KAPPA = 3.6813

#: Energy balance model:
#: speed of adjustment parameter for atmospheric temperature.
XI1 = 7.3

#: Energy balance model:
#: climate model parameter.
XI2 = KAPPA / NU

#: Energy balance model:
#: coefficient of heat loss from atmosphere to oceans.
XI3 = 0.73

#: Energy balance model:
#: coefficient of heat gain by deep oceans.
XI4 = 106
