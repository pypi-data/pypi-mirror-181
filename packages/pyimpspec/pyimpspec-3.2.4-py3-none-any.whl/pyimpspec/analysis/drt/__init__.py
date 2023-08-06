# pyimpspec is licensed under the GPLv3 or later (https://www.gnu.org/licenses/gpl-3.0.html).
# Copyright 2022 pyimpspec developers
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
# The licenses of pyimpspec's dependencies and/or sources of portions of code are included in
# the LICENSES folder.

from typing import (
    List,
    Optional,
)
from pyimpspec.data import DataSet
from pyimpspec.circuit import Circuit
from .result import (
    DRTError,
    DRTResult,
)
from .tr_nnls import _calculate_drt_tr_nnls
from .tr_rbf import _calculate_drt_tr_rbf
from .bht import _calculate_drt_bht
from .mRQfit import _calculate_drt_mRQfit


_METHODS: List[str] = [
    "bht",
    "m(RQ)fit",
    "tr-nnls",
    "tr-rbf",
]


def calculate_drt(
    data: DataSet,
    method: str = "tr-nnls",
    mode: str = "complex",
    lambda_value: float = -1.0,
    rbf_type: str = "gaussian",
    derivative_order: int = 1,
    rbf_shape: str = "fwhm",
    shape_coeff: float = 0.5,
    inductance: bool = False,
    credible_intervals: bool = False,
    num_samples: int = 2000,
    num_attempts: int = 10,
    maximum_symmetry: float = 0.5,
    circuit: Optional[Circuit] = None,
    W: float = 0.15,
    num_per_decade: int = 100,
    num_procs: int = -1,
) -> DRTResult:
    """
    Calculates the distribution of relaxation times (DRT) for a given data set.

    References:

    - Kulikovsky, A., 2020, Phys. Chem. Chem. Phys., 22, 19131-19138 (https://doi.org/10.1039/D0CP02094J)
    - Wan, T. H., Saccoccio, M., Chen, C., and Ciucci, F., 2015, Electrochim. Acta, 184, 483-499 (https://doi.org/10.1016/j.electacta.2015.09.097).
    - Ciucci, F. and Chen, C., 2015, Electrochim. Acta, 167, 439-454 (https://doi.org/10.1016/j.electacta.2015.03.123)
    - Effat, M. B. and Ciucci, F., 2017, Electrochim. Acta, 247, 1117-1129 (https://doi.org/10.1016/j.electacta.2017.07.050)
    - Liu, J., Wan, T. H., and Ciucci, F., 2020, Electrochim. Acta, 357, 136864 (https://doi.org/10.1016/j.electacta.2020.136864)
    - Boukamp, B.A., 2015, Electrochim. Acta, 154, 35-46, (https://doi.org/10.1016/j.electacta.2014.12.059)
    - Boukamp, B.A. and Rolle, A, 2017, Solid State Ionics, 302, 12-18 (https://doi.org/10.1016/j.ssi.2016.10.009)

    Parameters
    ----------
    data: DataSet
        The data set to use in the calculations.

    method: str = "tr-nnls"
        Valid values include:
        - "bht": Bayesian Hilbert Transform
        - "m(RQ)fit": m(RQ)fit for calculating the DRT based on a fitted circuit
        - "tr-nnls": Tikhonov regularization with non-negative least squares
        - "tr-rbf": Tikhonov regularization with radial basis function discretization

    mode: str = "complex"
        Which parts of the data are to be included in the calculations.
        Used by the "tr-nnls" and "tr-rbf" methods.
        Valid values include:
        - "complex" ("tr-rbf" method only and the default for that method)
        - "real" (default for the "tr-nnls" method)
        - "imaginary"

    lambda_value: float = -1.0
        The Tikhonov regularization parameter.
        Used by the "tr-nnls" and "tr-rbf" methods.
        If the method is "tr-nnls" and this value is equal to or below zero, then an attempt will be made to automatically find a suitable value.

    rbf_type: str = "gaussian"
        The type of function to use for discretization.
        Used by the "bht" and "tr-rbf" methods.
        Valid values include:
        - "gaussian"
        - "c0-matern"
        - "c2-matern"
        - "c4-matern"
        - "c6-matern"
        - "inverse-quadratic"
        - "inverse-quadric"
        - "cauchy"

    derivative_order: int = 1
        The order of the derivative used during discretization.
        Used by the "bht" and "tr-rbf" methods.

    rbf_shape: str = "fwhm"
        The shape control of the radial basis functions.
        Used by the "bht" and "tr-rbf" methods.
        Valid values include:
        - "fwhm": full width half maximum
        - "factor": `shape_coeff` is used directly

    shape_coeff: float = 0.5
        The full width at half maximum (FWHM) coefficient affecting the chosen shape type.
        Used by the "bht" and "tr-rbf" methods.

    inductance: bool = False
        If true, then an inductive element is included in the calculations.
        Used by the "tr-rbf" method.

    credible_intervals: bool = False
        If true, then the credible intervals are also calculated for the DRT results according to Bayesian statistics.
        Used by the "tr-rbf" method.

    num_samples: int = 2000
        The number of samples drawn when calculating the Bayesian credible intervals ("tr-rbf" method) or the Jensen-Shannon distance ("bht" method).
        A greater number provides better accuracy but requires more time.
        Used by the "bht" and "tr-rbf" methods.

    num_attempts: int = 10
        The minimum number of attempts to make when trying to find suitable random initial values.
        A greater number should provide better results at the expense of time.
        Used by the "bht" method.

    maximum_symmetry: float = 0.5
        A maximum limit (between 0.0 and 1.0) for a descriptor of the vertical symmetry of the DRT.
        A high degree of symmetry is common for results where the gamma value oscillates rather than forms distinct peaks.
        A low value for the limit should improve the results but may cause the "bht" method to take longer to finish.
        This limit is only used in the "tr-rbf" method when the regularization parameter (lambda) is not provided.
        Used by the "bht" and "tr-rbf" methods.

    circuit: Optional[Circuit] = None
        A circuit that contains one or more "(RQ)" or "(RC)" elements connected in series.
        An optional series resistance may also be included.
        For example, a circuit with a CDC representation of "R(RQ)(RQ)(RC)" would be a valid circuit.
        It is highly recommended that the provided circuit has already been fitted.
        However, if all of the various parameters of the provided circuit are at their default values, then an attempt will be made to fit the circuit to the data.
        Used by the "m(RQ)fit" method.

    W: float = 0.15
        The width of the Gaussian curve that is used to approximate the DRT of an "(RC)" element.
        Used by the "m(RQ)fit" method.

    num_per_decade: int = 100
        The number of points per decade to use when calculating a DRT.
        Used by the "m(RQ)fit" method.

    num_procs: int = -1
        The maximum number of processes to use.
        A value below one results in using the total number of CPU cores present.
    """
    assert (
        hasattr(data, "get_frequency")
        and callable(data.get_frequency)
        and hasattr(data, "get_impedance")
        and callable(data.get_impedance)
    ), "Invalid data object!"
    assert (
        type(method) is str and method in _METHODS
    ), f"Unsupported method! Valid values include: {', '.join(_METHODS)}"
    if method == "bht":
        return _calculate_drt_bht(
            data=data,
            rbf_type=rbf_type,
            derivative_order=derivative_order,
            rbf_shape=rbf_shape,
            shape_coeff=shape_coeff,
            num_samples=num_samples,
            num_attempts=num_attempts,
            maximum_symmetry=maximum_symmetry,
            num_procs=num_procs,
        )
    elif method == "m(RQ)fit":
        return _calculate_drt_mRQfit(
            data=data,
            circuit=circuit,
            W=W,
            num_per_decade=num_per_decade,
            num_procs=num_procs,
        )
    elif method == "tr-nnls":
        if mode == "complex":
            mode = "real"
        return _calculate_drt_tr_nnls(
            data=data,
            mode=mode,
            lambda_value=lambda_value,
            num_procs=num_procs,
        )
    elif method == "tr-rbf":
        return _calculate_drt_tr_rbf(
            data=data,
            mode=mode,
            lambda_value=lambda_value,
            rbf_type=rbf_type,
            derivative_order=derivative_order,
            rbf_shape=rbf_shape,
            shape_coeff=shape_coeff,
            inductance=inductance,
            credible_intervals=credible_intervals,
            num_samples=num_samples,
            maximum_symmetry=maximum_symmetry,
            num_procs=num_procs,
        )
    valid_methods: str = "\n- ".join(_METHODS)
    raise Exception(f"Unknown method: {method}\nSupported methods:\n- {valid_methods}")
