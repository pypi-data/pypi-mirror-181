# Copyright (c) 2022 International Institute for Applied Systems Analysis.
# All rights reserved. The use and distribution terms for this software
# are covered by the MIT License (http://opensource.org/licenses/MIT)
# which can be found in the file LICENSE at the root of this distribution.
# By using this software in any fashion, you are agreeing to be bound by
# the terms of this license.
# You must not remove this notice, or any other, from this software.
"""Python climate module implementation from Hansel et al. (2020).

References
----------
.. [1] Hansel, M., Drupp, M., Johansson, D., Nesje, F., Azar, C., Freeman, M.,
    Groom, B., & Sterner, T. (2020). Climate Economics Support for the UN
    Climate Targets. Nature Climate Change, 10: 781-789.
    https://doi.org/10.1038/s41558-020-0833-x
.. [2] Smith, C. J., Forster, P. M.,  Allen, M., Leach, N., Millar, R. J.,
    Passerello, G. A., & Regayre, L. A. (2018). FAIR v1.3: a Simple Emissions-
    Based Impulse Response and Carbon Cycle Model. Geoscientific Model
    Development, 11: 2273–2297. https://doi.org/10.5194/gmd-11-2273-2018
.. [3] Geoffroy, O., Saint-Martin, D., Olivié, D. J. L., Voldoire, A.,
    Bellon, G., & Tytéca, S. (2013). Transient Climate Response in a Two-Layer
    Energy-Balance Model. Part I: Analytical Solution and Parameter Calibration
    Using CMIP5 AOGCM Experiments. Journal of Climate, 26: 1841–1857.
    https://doi.org/10.1175/JCLI-D-12-00195.1

"""

__author__ = "Anna Shchiptsova"
__copyright__ = "Copyright (c) 2022 IIASA"
__license__ = "MIT"
