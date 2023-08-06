# Copyright (c) 2022 International Institute for Applied Systems Analysis.
# All rights reserved. The use and distribution terms for this software
# are covered by the MIT License (http://opensource.org/licenses/MIT)
# which can be found in the file LICENSE at the root of this distribution.
# By using this software in any fashion, you are agreeing to be bound by
# the terms of this license.
# You must not remove this notice, or any other, from this software.
"""Climate module (Hansel et al.) for DICE-like simulation model.

References
----------
.. [1] Hansel, M., Drupp, M., Johansson, D., Nesje, F., Azar, C., Freeman, M.,
    Groom, B., & Sterner, T. (2020). Climate Economics Support for the UN
    Climate Targets. Nature Climate Change, 10: 781-789.
    https://doi.org/10.1038/s41558-020-0833-x
.. [2] [SSP Database] https://tntcat.iiasa.ac.at/SspDb/

"""

__author__ = "Anna Shchiptsova"
__copyright__ = "Copyright (c) 2022 IIASA"
__license__ = "MIT"

from climate_module.hansel2020.inputs import (
    radiative_forcing_non_co2,
    emissions_land_use_co2)
from climate_module.hansel2020.model import climate_module
from .options import parse
from .provider import read_emissions, read_other_rf_ratio, write_output


def _options():
    """Supported command line options."""
    return {
        'emissions': ['hansel2020', 'SSP1', 'SSP2', 'SSP3', 'SSP4', 'SSP5'],
        'ratio': ['avg', 'max', 'min']
    }


def _emissions(label, folder):
    """Map emissions curve data by label."""
    if label == 'hansel2020':
        return read_emissions(
            'hansel FFI.csv',
            in_resources=True,
            transform=lambda e: e + emissions_land_use_co2(e.size))

    return read_emissions(folder + '/net-emissions ' + label + '.csv')


def _other_rf(label, ratio):
    """Map non-CO2 forcings data by label."""
    if ratio == 'hansel2020':
        return radiative_forcing_non_co2, True

    labels = {'avg': 'Avg Ratio', 'max': 'Max', 'min': 'Min'}
    return read_other_rf_ratio(
        'SSP markers ratio non_CO2 to CO2.csv',
        label,
        labels[ratio]), False


def simulate_temperature(argv) -> int:
    """Perform climate simulations from generic DICE model."""
    args = parse(argv, _options())

    if args is None:
        return 1

    content = _emissions(
        args['emissions'],
        args['folder'])

    if content is None:
        return 1

    header, par_ids, net_emissions_paths = content

    other_rf, absolute_other_rf = _other_rf(
        args['emissions'],
        args['ratio'])

    climate_output = [[], []]  # type: ignore
    for net_emissions in net_emissions_paths:
        temp_atm, concentration = climate_module(
            net_emissions,
            other_rf,
            absolute_other_rf)
        climate_output[0].append(temp_atm)
        climate_output[1].append(concentration)

    for variable, data in zip(
        ['temperature change', 'concentration'],
            climate_output):
        folder = write_output(args, variable, header, par_ids, data)

    if folder is None:
        return 1

    print('Results saved to: ' + folder)
    return 0
