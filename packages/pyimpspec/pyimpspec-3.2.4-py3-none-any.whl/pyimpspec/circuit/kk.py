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
    Dict,
    List,
)
from math import pi
from collections import OrderedDict
from .base import Element
from numpy import inf


class KramersKronigRC(Element):
    """
    Parallel RC element used in linear Kramers-Kronig tests

        Symbol: K

        Z = R / (1 + j*2*pi*f*t)

        Variables
        ---------
        R: float = 1 (ohm)
        t: float = 1 (s)
    """

    def __init__(self, **kwargs):
        keys: List[str] = list(self.get_defaults().keys())
        super().__init__(keys=keys)
        self.reset_parameters(keys)
        self.set_parameters(kwargs)

    @staticmethod
    def get_symbol() -> str:
        return "K"

    @staticmethod
    def get_description() -> str:
        return "K: Linear Kramers-Kronig test element"

    @staticmethod
    def get_default_fixed() -> Dict[str, bool]:
        return {
            "R": False,
            "t": True,
        }

    @staticmethod
    def get_defaults() -> Dict[str, float]:
        return {
            "R": 1,
            "t": 1,
        }

    @staticmethod
    def get_default_lower_limits() -> Dict[str, float]:
        return {
            "R": -inf,
            "t": 0,
        }

    @staticmethod
    def get_default_upper_limits() -> Dict[str, float]:
        return {
            "R": inf,
            "t": inf,
        }

    def impedance(self, f: float) -> complex:
        return self._R / (1 + 2 * pi * f * self._t * 1j)

    def get_parameters(self) -> "OrderedDict[str, float]":
        return OrderedDict({"R": self._R, "t": self._t})

    def set_parameters(self, parameters: Dict[str, float]):
        if "R" in parameters:
            self._R = float(parameters["R"])
        if "t" in parameters:
            self._t = float(parameters["t"])

    def _str_expr(self, substitute: bool = False) -> str:
        string: str = "R / (1 + I*2*pi*f*t)"
        return self._subs_str_expr(string, self.get_parameters(), not substitute)
