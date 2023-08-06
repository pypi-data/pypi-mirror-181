# Copyright (c) 2022 International Institute for Applied Systems Analysis.
# All rights reserved. The use and distribution terms for this software
# are covered by the MIT License (http://opensource.org/licenses/MIT)
# which can be found in the file LICENSE at the root of this distribution.
# By using this software in any fashion, you are agreeing to be bound by
# the terms of this license.
# You must not remove this notice, or any other, from this software.
"""Forward and backward processing of I/O data."""

__author__ = "Anna Shchiptsova"
__copyright__ = "Copyright (c) 2022 IIASA"
__license__ = "MIT"

import os
import csv
from importlib.resources import open_text
import numpy as np  # type: ignore
from climate_module import resources


def _parse_emissions(file, transform, n_pars):
    """Parse net emissions curve values from csv file."""
    csvreader = csv.reader(file)
    header = next(csvreader)

    ids = []
    values = []
    for row in csvreader:
        ids.append(row[:n_pars])
        values.append(transform(np.array(row[n_pars:], dtype=float)))

    return header, ids, values


def read_emissions(
    resource,
    in_resources=False,
    transform=lambda x: x,
        n_pars=6):
    """Read net emissions pathways from csv file."""
    if in_resources:
        with open_text(resources, resource) as file:
            content = _parse_emissions(file, transform, n_pars)
    else:
        content = None
        try:
            with open(resource, 'r', encoding='utf8') as file:
                content = _parse_emissions(file, transform, n_pars)
        except IOError as error:
            print(f'open failed: unable to read file {resource}:\n{error}')

    return content


def read_other_rf_ratio(resource, ssp, ratio):
    """Read radiative forcing from non-CO2 curves from csv resources file."""
    file = open_text(resources, resource)
    csvreader = csv.reader(file)

    for row in csvreader:
        if row[0] == ssp and row[1] == ratio:
            other_rf = np.array(row[2:], dtype=float)
            break

    return other_rf


def write_output(args, variable, header, par_ids, data):
    """Write temperature pathways into csv file."""
    folder = os.path.join('climate', 'scenario ' + args['emissions'])
    if not os.path.exists(folder):
        os.makedirs(folder)

    filename = variable + ' (other_rf ' + args['ratio'] + ').csv'
    dir_path = None

    try:
        with open(
            os.path.join(folder, filename),
            'w',
            newline='',
                encoding='utf8') as file:

            csvwriter = csv.writer(file)
            csvwriter.writerow(header)

            for par_id, values in zip(par_ids, data):
                out = list(map(lambda x: format(x, '.3f'), values))
                csvwriter.writerow([*par_id, *out])

        dir_path = os.path.abspath(folder)

    except IOError as error:
        print(f'save failed: unable to write to {dir_path}:\n{error}')

    return dir_path
