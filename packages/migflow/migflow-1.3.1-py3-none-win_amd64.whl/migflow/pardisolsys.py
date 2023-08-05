# MigFlow - Copyright (C) <2010-2022>
# <Universite catholique de Louvain (UCL), Belgium
#  Universite de Montpellier, France>
#
# List of the contributors to the development of MigFlow: see AUTHORS file.
# Description and complete License: see LICENSE file.
#
# This program (MigFlow) is free software:
# you can redistribute it and/or modify it under the terms of the GNU Lesser General
# Public License as published by the Free Software Foundation, either version
# 3 of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program (see COPYING and COPYING.LESSER files).  If not,
# see <http://www.gnu.org/licenses/>.

import ctypes
import numpy as np
from ._tools import timeit, _np2c
from .csr import CSR
import time
import os
import sysconfig
import sys

def find_mkl_library():
    schemes = {
            "linux":["posix_home","posix_user","posix_prefix"],
            "win32":["nt", "nt_user"],
            "darwin":["osx_framework_user"]}[sys.platform]
    pip_path = {
            "darwin":"lib",
            "linux":"lib",
            "win32":"Library\\bin"
        }[sys.platform]
    library = {
            "linux":"libmkl_rt.so.2",
            "win32":"mkl_rt.2.dll",
            "darwin":"libmkl_rt.2.dylib"
        }[sys.platform]
    found = None
    if "MKLROOT" in os.environ:
        path = os.path.join(os.environ["MKLROOT"], "lib", "intel64", library)
        if os.path.isfile(path):
            found = path
    # search for a pip installation
    if found is None:
        for scheme in schemes:
            path = os.path.join(sysconfig.get_paths(scheme)["data"], pip_path, library)
            if os.path.isfile(path):
                found = path
                break
    if found is None:
        lib = ctypes.CDLL(ctypes.util.find_library("mkl_rt"))
    else:
        lib = ctypes.CDLL(found)
    assert(lib.pardiso is not None)
    return lib

libmkl = find_mkl_library()
#libmkl.MKL_Set_Num_Threads(1)

class LinearSystem:
    def __init__(self, elements, idx, n_fields, options="", constraints=[], gid=()) :
        self._first = True
        self.idx = idx
        self.constraints = list(constraints)
        self.csr = CSR(idx, self.constraints)
        self.val = np.zeros(self.csr.col.size)
        self.perm = np.zeros(self.csr.size, np.int32)
        self.pt = _np2c(np.zeros(64, np.int64))
        iparm = np.zeros(64, np.int32)
        iparm[0] = 1   # do not use all default values
        iparm[1] = 2   # use metis reordering
        iparm[9] = 13  # pivoting perturbation (13 -> 1e-13)
        iparm[10] = 1  # enable scaling
        iparm[34] = 1  # 0-indexing
        self.iparm = iparm
        self.valpt = _np2c(self.val)
        self.rowpt = _np2c(self.csr.row, np.int32)
        self.colpt = _np2c(self.csr.col, np.int32)
        self.permpt = _np2c(self.perm, np.int32)
        self.iparmpt = _np2c(self.iparm, np.int32)
    
    def _call_pardiso(self, rhs, x, phase):
        error = ctypes.c_int(0)
        msglvl = ctypes.c_int(0)
        nrhs = ctypes.c_int(1)
        mattype = ctypes.c_int(11)
        phase = ctypes.c_int(phase)#13 if self._first else 23)
        maxfct = ctypes.c_int(1)
        mnum = ctypes.c_int(1)
        nrow = ctypes.c_int(self.csr.size)
        libmkl.pardiso(
                self.pt,
                ctypes.byref(maxfct),
                ctypes.byref(mnum),
                ctypes.byref(mattype),
                ctypes.byref(phase),
                ctypes.byref(nrow),
                self.valpt,
                self.rowpt,
                self.colpt,
                self.permpt,
                ctypes.byref(nrhs),
                self.iparmpt,
                ctypes.byref(msglvl),
                _np2c(rhs) if rhs is not None else None,
                _np2c(x) if x is not None else None,
                ctypes.byref(error))
        assert(error.value == 0)

    def __del__(self) :
        self._call_pardiso(None, None, -1)

    @timeit
    def local_to_global(self, localv, localm, u, constraints_value):
        self.csr.assemble_mat(localm, constraints_value, self.val)
        return self.csr.assemble_rhs(localv, u, constraints_value)

    @timeit
    def solve(self, rhs) :
        tic = time.time()
        x = np.ndarray(rhs.shape)
        if self._first :
            self._call_pardiso(rhs, x, 11)
            self._first = False
        self._call_pardiso(rhs, x, 23)
        print("time = ", time.time()-tic)
        return x[:self.csr.ndof]
