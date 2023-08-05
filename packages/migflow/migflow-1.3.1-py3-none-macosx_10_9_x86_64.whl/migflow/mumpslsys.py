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

from gmsh import option
import numpy as np


import ctypes
import ctypes.util
import os
from ._tools import timeit, _np2c
from .csr import CSR

dir_path = os.path.dirname(os.path.realpath(__file__))
lib2 = np.ctypeslib.load_library("libmbfluid2",dir_path)

options_key = {"verbosity":4, "fill_in":14, "reorder_metis":7, "scaling":8, "openmp_threads" :16}

class LinearSystem :
    @timeit
    def __init__(self, elements, idx, n_fields, options=None, constraints=[], gid=()) :
        
        self.globalsize = np.max(idx)+1+len(constraints)
        self.localsize = idx.shape[1]
        self.idx = idx
        idxf = [self.idx+1]
        eltptr = [np.arange(1,idx.size+2,self.localsize)]
        self.ndof = np.max(idx)+1
        self.n_fields = n_fields
        self.constraints = constraints
        
        for i,constraint in enumerate(self.constraints):
            idxc = np.c_[np.full(constraint.shape[0], self.ndof+i+1), constraint+1].flatten()
            idxf.append(idxc)
            eltptr.append(eltptr[-1][-1]+np.arange(2,constraint.shape[0]*2+2,2))
        
        eltptr = np.concatenate([i.flat for i in eltptr])
        idxf = np.concatenate([i.flat for i in idxf])
        lib2.mumps_element_new.restype = ctypes.c_void_p
        self.mumps_ptr = ctypes.c_void_p(lib2.mumps_element_new(ctypes.c_int(self.globalsize),ctypes.c_int(eltptr.size-1),_np2c(eltptr,np.int32),_np2c(idxf,np.int32)))  
        options = None if options=="" else options
        if options is not None:
            options_vec = []
            for key, val in options.items():
                if isinstance(key,str):
                    key = options_key[key]
                    options_vec.extend([key,val])
            options_vec = np.array(options_vec, dtype=np.int32)
            lib2.mumps_set_options(self.mumps_ptr, _np2c(options_vec, np.int32), ctypes.c_int(np.size(options_vec)//2))

    @timeit
    def local_to_global(self,localv,localm,u, constraints_values=[]):
        rhs = np.bincount(self.idx.flatten(),localv,self.globalsize)
        for i, (c, cv) in enumerate(zip(self.constraints,constraints_values)):
            rhs[i+self.ndof] = cv[1] + np.sum(u[c]*cv[0])
        self.v = np.empty(localm.size+sum(c.shape[0]*4 for c in self.constraints))
        p = localm.size
        self.v[:p] = localm.flat
        for constraint, cv  in constraints_values:
            localc = np.zeros((constraint.shape[0],4))
            localc[:,1] = constraint
            localc[:,2] = constraint
            self.v[p:localc.size+p] = localc.flat
            p += localc
        return rhs

    @timeit
    def solve(self,rhs):
        lib2.mumps_element_solve(self.mumps_ptr,_np2c(self.v),_np2c(rhs))
        return rhs[:self.ndof]

    def __delete__(self):
        lib2.mumps_element_delete(self.mumps_ptr)

