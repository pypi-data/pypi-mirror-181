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

import numpy as np
import atexit

from ._tools import timeit, _np2c
from .csr import CSR

import ctypes
import os

petscpath = os.environ["PETSC_DIR"]+"/"+os.environ["PETSC_ARCH"]+"/lib"
os.environ["LD_LIBRARY_PATH"] = os.environ.get("LD_LIBRARY_PATH","")+":"+petscpath
try:
    lib = np.ctypeslib.load_library("libpetsc",petscpath)
except:
    try:
        lib = np.ctypeslib.load_library("libpetsc_real",petscpath)
    except:
        raise ValueError("petsc library not found")

lib.PetscInitialize(None, None, None)
COMM_WORLD = ctypes.c_void_p.in_dll(lib,"PETSC_COMM_WORLD")
#atexit.register(lib.PetscFinalize)


class PetscObj:
    
    def __init__(self, constructor, destructor, *args):
        self._p = ctypes.c_void_p()
        self._destructor = destructor
        lib[constructor](*args,ctypes.byref(self._p))

    def __del__(self):
        lib[self._destructor](ctypes.byref(self._p))

    @property
    def _as_parameter_(self) :
        return self._p


class Vec(PetscObj) :

    def __init__(self, v) :
        super().__init__("VecCreateSeqWithArray","VecDestroy",COMM_WORLD,
                ctypes.c_int(v.shape[-1]), ctypes.c_int(v.size),ctypes.c_void_p(v.ctypes.data))

def insert_options(prefix,options):
    lib.PetscOptionsPrefixPush(None, prefix.encode())
    lib.PetscOptionsInsertString(None, options.encode())
    lib.PetscOptionsPrefixPop(None)

def get_option_bool(prefix, name, default):
    v = ctypes.c_int(0)
    lib.PetscOptionsGetBool(None, prefix.encode(), name.encode(), ctypes.c_int(default), ctypes.byref(v))
    return v.value

class LinearSystem:

    def __init__(self, elements, idx, n_fields, options="", constraints=[], gid=()) :
        idv, idp = gid
        isp1 = idv.shape[0] == idp.shape[0] 
        if isp1:
            insert_options("fluid", "-pc_type ilu -pc_factor_levels 5 -pc_factor_shift_type INBLOCKS -pc_factor_shift_amount 1e-16")
        insert_options("fluid", options)
        self.block = get_option_bool("fluid","-block_matrix",0)
        self.ksp = PetscObj("KSPCreate", "KSPDestroy", COMM_WORLD)
        lib.KSPSetOptionsPrefix(self.ksp,b"fluid")
        if self.block:
            if len(constraints) != 0 :
                raise ValueError("petsc BAIJ not implemented with constraints")
            if n_fields*elements.shape[1] != idx.shape[1]:
                raise ValueError("petsc block matrices not implemented with p2p1")
            # TO FIX
            nn = elements.shape[1]
            self.csr = CSR(elements,elements,[])
            self.localsize = elements.shape[1]*n_fields
            self.idx = (elements[:,None,:]*n_fields+np.arange(n_fields)[None,:,None]).reshape([-1])
            self.n_fields = n_fields
            csrmapl = np.arange(nn*nn)[None,:].reshape(nn,nn).T
            csrmap = (self.csr.map[0]*nn*nn)[:,None,None]+csrmapl[None,:,:]
            self.csrmap = np.copy(np.swapaxes(csrmap.reshape([elements.shape[0],nn,nn, n_fields,n_fields]),2,3).reshape([-1]))
            self.vsize = np.max(self.csrmap)+1
            self.mat = PetscObj("MatCreate", "MatDestroy", COMM_WORLD)
            lib.MatSetType(self.mat, b"seqbaij")
            ms = self.csr.size*n_fields
            lib.MatSetSizes(self.mat,ctypes.c_int(ms),ctypes.c_int(ms),ctypes.c_int(ms),ctypes.c_int(ms))
            lib.MatSeqBAIJSetPreallocationCSR(self.mat,
                    ctypes.c_int(n_fields), _np2c(self.csr.row, np.int32), _np2c(self.csr.col, np.int32), None)
        else:
            self.idx = idx
            self.constraints = list(constraints)
            self.csr = CSR(idx, self.constraints)
            self.val = np.zeros(self.csr.col.size)
            self.mat = PetscObj("MatCreateSeqAIJWithArrays", "MatDestroy", COMM_WORLD,
                    ctypes.c_int(self.csr.size), ctypes.c_int(self.csr.size), 
                    _np2c(self.csr.row,np.int32), _np2c(self.csr.col,np.int32), _np2c(self.val))
        
        # if not isp1 :
        #     pc = ctypes.POINTER(ctypes.c_void_p)()
        #     lib.KSPGetPC(self.ksp, ctypes.byref(pc))
        #     lib.PCSetType(pc, ctypes.c_char_p(b"fieldsplit"))
        #     isv = ctypes.POINTER(ctypes.c_void_p)()
        #     isp = ctypes.POINTER(ctypes.c_void_p)()
        #     lib.ISCreateGeneral(COMM_WORLD, ctypes.c_int(idp.size), _np2c(idp, np.int32), ctypes.c_int(0), ctypes.byref(isp))
        #     lib.ISCreateGeneral(COMM_WORLD, ctypes.c_int(idv.size), _np2c(idv, np.int32), ctypes.c_int(0), ctypes.byref(isv))
        #     lib.PCFieldSplitSetIS(pc, ctypes.c_char_p(b"velocity"), isv)
        #     lib.PCFieldSplitSetIS(pc, ctypes.c_char_p(b"pressure"), isp)
        #     insert_options("fluid", "-pc_fieldsplit type schur -fieldsplit_velocity_ksp_type preonly -fieldsplit_velocity_pc_type lu"
        #     + " -fieldsplit_pressure_ksp_type preonly -fieldsplit_pressure_pc_type jacobi" )
        
        lib.KSPSetFromOptions(self.ksp)



    @timeit
    def local_to_global(self,localv,localm, u, constraints_value = []):
        if self.block:
            rhs = np.bincount(self.idx,localv,self.csr.size*self.n_fields)
            aptr = ctypes.POINTER(ctypes.c_double)()
            lib.MatSeqBAIJGetArray(self.mat, ctypes.byref(aptr))
            a = np.ctypeslib.as_array(aptr,shape=(self.vsize,))
            a[:] = np.bincount(self.csrmap,localm,self.csr.col.size*self.n_fields**2)
            lib.MatSeqBAIJRestoreArray(self.mat, ctypes.byref(aptr))
        else:
            self.csr.assemble_mat(localm, constraints_value, self.val)
            rhs = self.csr.assemble_rhs(localv, u , constraints_value)
        lib.MatAssemblyBegin(self.mat,0)
        lib.MatAssemblyEnd(self.mat,0)
        return rhs

    @timeit
    def solve(self,rhs) :
        x = np.zeros_like(rhs)
        #lib.KSPSetReusePreconditioner(self, 0)
        lib.KSPSetOperators(self.ksp, self.mat, self.mat)
        if self.block:
            lib.KSPSolve(self.ksp, Vec(rhs.reshape(-1,self.n_fields)), Vec(x))
            return x.reshape(rhs.shape)
        else:
            lib.KSPSolve(self.ksp, Vec(rhs.reshape(-1)), Vec(x))
            return x.reshape(rhs.shape)[:self.csr.ndof]

