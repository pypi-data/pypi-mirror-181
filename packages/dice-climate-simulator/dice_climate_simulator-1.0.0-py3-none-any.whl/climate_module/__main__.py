# Copyright (c) 2022 International Institute for Applied Systems Analysis.
# All rights reserved. The use and distribution terms for this software
# are covered by the MIT License (http://opensource.org/licenses/MIT)
# which can be found in the file LICENSE at the root of this distribution.
# By using this software in any fashion, you are agreeing to be bound by
# the terms of this license.
# You must not remove this notice, or any other, from this software.
"""Run package without build."""

__author__ = "Anna Shchiptsova"
__copyright__ = "Copyright (c) 2022 IIASA"
__license__ = "MIT"

import sys
from .core import simulate_temperature

if __name__ == '__main__':
    sys.exit(simulate_temperature(sys.argv[1:]))
