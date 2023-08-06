# MolAlign
# Copyright (C) 2022 José M. Vásquez

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import numpy as np
from ase import Atoms
from molalignlibext import molalignlib

class Assign(Atoms):
    def __init__(
        self,
        atoms,
        weights = None,
        biasing = False,
        bias_tol = 0.2,
        bias_scale = 1.e3,
        iteration = False,
        testing = False,
        records = 1,
        count = 10,
        trials = None,
    ):
        if isinstance(atoms, Atoms):
            self.__dict__.update(atoms.__dict__)
        else:
            raise TypeError('An Atoms object was expected')
        if type(biasing) is not bool:
            raise TypeError('"biasing" must be a boolean')
        if type(iteration) is not bool:
            raise TypeError('"iteration" must be a boolean')
        if type(testing) is not bool:
            raise TypeError('"testing" must be a boolean')
        if type(records) is not int:
            raise TypeError('"records" must be an integer')
        if type(count) is not int:
            raise TypeError('"count" must be an integer')
        if type(bias_tol) is not float:
            raise TypeError('"bias_tol" must be a real')
        if type(bias_scale) is not float:
            raise TypeError('"bias_scale" must be a real')
        if trials is None:
            molalignlib.set_free_flag(True)
        elif type(trials) is int:
            molalignlib.set_free_flag(False)
            molalignlib.set_max_trials(trials)
        else:
            raise TypeError('"trials" must be an integer')
        if weights is None:
            weights = np.ones(len(atoms), dtype=np.float64)
        elif type(weights) is np.ndarray:
            if weights.dtype != np.float64:
                raise TypeError('"weights" dtype must be float64')
        else:
            raise TypeError('"weights" must be a numpy array')
        self.records = records
        self.weights = weights/sum(weights)
        molalignlib.set_bias_flag(biasing)
        molalignlib.set_bias_scale(bias_scale)
        molalignlib.set_bias_tol(bias_tol)
        molalignlib.set_conv_flag(iteration)
        molalignlib.set_test_flag(testing)
        molalignlib.set_max_count(count)
    def __call__(self, other):
        if not isinstance(other, Atoms):
            raise TypeError('An Atoms object was expected as argument')
        if len(other) != len(self):
            raise ValueError('Argument does no have the right length')
        znums0 = self.get_atomic_numbers()
        znums1 = other.get_atomic_numbers()
        types0 = np.ones(len(self), dtype=int)
        types1 = np.ones(len(other), dtype=int)
        coords0 = self.positions.T # Convert to column-major order
        coords1 = other.positions.T # Convert to column-major order
        nmap, mapind, mapcount, mapdist, error = molalignlib.assign_atoms(znums0, znums1, \
            types0, types1, coords0, coords1, self.weights, self.records)
        if error:
            raise RuntimeError('Assignment failed')
        return [mapind[:, i] - 1 for i in range(nmap)]

class Align(Atoms):
    def __init__(
        self,
        atoms,
        weights = None,
    ):
        if isinstance(atoms, Atoms):
            self.__dict__.update(atoms.__dict__)
        else:
            raise TypeError('An Atoms object was expected')
        if weights is None:
            weights = np.ones(len(atoms), dtype=np.float64)
        elif type(weights) is np.ndarray:
            if weights.dtype != np.float64:
                raise TypeError('"weights" dtype must be float64')
        else:
            raise TypeError('"weights" must be a numpy array')
        self.weights = weights/weights.sum()
    def __call__(self, other):
        if not isinstance(other, Atoms):
            raise TypeError('An Atoms object was expected as first argument')
        if len(other) != len(self):
            raise ValueError('First argument does no have the right length')
        znums0 = self.get_atomic_numbers()
        znums1 = other.get_atomic_numbers()
        types0 = np.ones(len(self), dtype=int)
        types1 = np.ones(len(other), dtype=int)
        coords0 = self.positions.T # Convert to column-major order
        coords1 = other.positions.T # Convert to column-major order
        travec, rotmat, error = molalignlib.align_atoms(znums0, znums1, types0, types1, \
            coords0, coords1, self.weights)
        if error:
            raise RuntimeError('Alignment failed')
        coords1 = np.dot(rotmat, coords1) + travec[:, np.newaxis]
        other.positions = coords1.T
        return other

def rmsd(atoms1, atoms2, weights):
    return ((weights*((atoms1.positions - atoms2.positions)**2).sum(axis=1)).sum()/weights.sum())**0.5
