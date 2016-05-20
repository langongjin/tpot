# -*- coding: utf-8 -*-

"""
Copyright 2016 Randal S. Olson

This file is part of the TPOT library.

The TPOT library is free software: you can redistribute it and/or
modify it under the terms of the GNU General Public License as published by the
Free Software Foundation, either version 3 of the License, or (at your option)
any later version.

The TPOT library is distributed in the hope that it will be useful, but
WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
You should have received a copy of the GNU General Public License along with
the TPOT library. If not, see http://www.gnu.org/licenses/.
"""

from functools import wraps

def _gp_new_generation(func):
    """Decorator that wraps functions that indicate the beginning of a new GP
    generation.

    Parameters
    ----------
    func: function
        The function being decorated

    Returns
    -------
    wrapped_func: function
        A wrapper function around the func parameter
    """
    @wraps(func)
    def wrapped_func(self, *args, **kwargs):
        """Increment gp_generation and bump pipeline count if necessary"""
        ret = func(self, *args, **kwargs)
        self.gp_generation = self.gp_generation + 1

        if not self.pbar.disable:
            if self.pbar.n < self.gp_generation * self.population_size:
                missing_pipelines = (self.gp_generation * self.population_size) - self.pbar.n
                self.pbar.update(missing_pipelines)

        return ret # Pass back return value of func

    return wrapped_func
