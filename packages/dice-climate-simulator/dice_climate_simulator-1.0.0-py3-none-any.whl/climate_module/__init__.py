# Copyright (c) 2022 International Institute for Applied Systems Analysis.
# All rights reserved. The use and distribution terms for this software
# are covered by the MIT License (http://opensource.org/licenses/MIT)
# which can be found in the file LICENSE at the root of this distribution.
# By using this software in any fashion, you are agreeing to be bound by
# the terms of this license.
# You must not remove this notice, or any other, from this software.
"""Command line operations for climate module.

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

import sys
from .core import simulate_temperature


def main():
    """Entry point for the application script."""
    sys.exit(simulate_temperature(sys.argv[1:]))
