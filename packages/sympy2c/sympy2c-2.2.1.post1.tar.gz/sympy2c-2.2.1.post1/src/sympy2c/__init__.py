# This file is part of sympy2c.
#
# Copyright (C) 2013-2022 ETH Zurich, Institute for Particle and Astrophysics and SIS
# ID.
#
# This program is free software: you can redistribute it and/or modify it under the
# terms of the GNU General Public License as published by the Free Software Foundation,
# either version 3 of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
# PARTICULAR PURPOSE.  See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with this
# program.  If not, see <http://www.gnu.org/licenses/>.

# flake8: noqa F401

import importlib
import sys

_c = {
    "compile_if_needed_and_load": "compiler",
    "Max": "expressions",
    "Min": "expressions",
    "isnan": "expressions",
    "Alias": "function",
    "Function": "function",
    "Globals": "globals",
    "ERROR": "integral",
    "Checked": "integral",
    "IfThenElse": "integral",
    "Integral": "integral",
    "InterpolationFunction1D": "interpolation",
    "InterpolationFunction1DInstance": "interpolation",
    "Module": "module",
    "Ode": "ode",
    "OdeCombined": "ode_combined",
    "OdeFast": "ode_fast",
    "PythonFunction": "python_function",
    "Symbol": "symbol",
    "symbols": "symbol",
    "Vector": "vector",
    "VectorElement": "vector",
}


class LazyFinder:
    @classmethod
    def find_spec(cls, name, path, target=None):
        if not name.startswith("sympy2c."):
            return
        inner = name.split(".", 1)[1]
        module_name = _c.get(inner)
        if module_name is None:
            return

        module = importlib.import_module("sympy2c." + module_name)
        sys.modules[name] = getattr(module, inner)


sys.meta_path.append(LazyFinder)

__author__ = "Uwe Schmitt"
__email__ = "uwe.schmitt@id.ethz.ch"

import pkg_resources

_s = pkg_resources.require(__package__)[0]
__version__ = tuple(map(int, _s.version.split(".")))
