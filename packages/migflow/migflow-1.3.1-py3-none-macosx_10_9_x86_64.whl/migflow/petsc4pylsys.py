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

import petsc4py
import sys
petsc4py.init(sys.argv)
from petsc4py import PETSc
import numpy as np
from ._tools import timeit
from .csr import CSR

class LinearSystem:

    def __init__(self, elements, idx, n_fields, options="", constraints=[], gid=()) :
        idv, idp = gid
        isp1 = idv.shape[0] == idp.shape[0] 
        if isp1:
            PETSc.Options().prefixPush("fluid_")
            PETSc.Options().insertString("-pc_type ilu -pc_factor_levels 5 -pc_factor_shift_type INBLOCKS -pc_factor_shift_amount 1e-16")
            PETSc.Options().insertString(options)
            PETSc.Options().prefixPop()
        self.block = PETSc.Options().getBool("fluid_block_matrix",False)
        self.ksp = PETSc.KSP().create()
        self.ksp.setOptionsPrefix(b"fluid_")
        
        if self.block and isp1:
            if len(constraints) != 0 :
                raise ValueError("petsc block matrices not implemented with constraints")
            nn = elements.shape[1]
            self.csr = CSR(elements, [])
            self.mat = PETSc.Mat().createBAIJ(self.csr.size*n_fields, n_fields, csr=(self.csr.row, self.csr.col))
            self.idx = (elements[:,None,:]*n_fields+np.arange(n_fields)[None,:,None]).reshape([-1])
            self.n_fields = n_fields
            csrmapl = np.arange(n_fields*n_fields)[None,:].reshape(n_fields,n_fields)
            csrmap = (self.csr.map[0]*n_fields*n_fields)[:,None,None]+csrmapl[None,:,:]
            self.csrmap = np.swapaxes(csrmap.reshape([elements.shape[0],nn,n_fields,nn,n_fields]),2,3).reshape([-1])
        else:
            self.idx = idx
            self.constraints = list(constraints)
            self.csr = CSR(idx, self.constraints)
            self.val = np.zeros(self.csr.col.size)
            self.mat = PETSc.Mat().createAIJWithArrays(self.csr.size,(self.csr.row,self.csr.col,self.val))

        if not isp1 :
            pc = self.ksp.getPC()
            pc.setType(PETSc.PC.Type.FIELDSPLIT)
            isp = PETSc.IS().createGeneral(idp)
            isv = PETSc.IS().createGeneral(idv)
            pc.setFieldSplitIS(("velocity", isv), ('pressure', isp))
            PETSc.Options().prefixPush("fluid_")
            PETSc.Options().insertString("-pc_fieldsplit type schur -fieldsplit_velocity_ksp_type preonly -fieldsplit_velocity_pc_type lu"
            + " -fieldsplit_pressure_ksp_type preonly -fieldsplit_pressure_pc_type jacobi" )
            PETSc.Options().insertString(options)
            PETSc.Options().prefixPop()

        self.ksp.setFromOptions()

    @timeit
    def local_to_global(self, localv, localm, u, constraints_value):
        if self.block:
            rhs = np.bincount(self.idx,localv,self.csr.size*self.n_fields)
            val = np.bincount(self.csrmap,localm,self.csr.col.size*self.n_fields**2)
            self.mat.zeroEntries()
            self.mat.setValuesBlockedCSR(self.csr.row, self.csr.col, val)
            self.mat.assemble()
            return rhs
        else:
            self.csr.assemble_mat(localm, constraints_value, self.val)
            self.mat.assemble()
            return self.csr.assemble_rhs(localv, u, constraints_value)

    @timeit
    def solve(self,rhs) :
        x = np.ndarray(rhs.shape)
        prhs = PETSc.Vec().createWithArray(rhs.reshape([-1]))
        px = PETSc.Vec().createWithArray(x.reshape([-1]))
        self.ksp.setOperators(self.mat)
        self.ksp.solve(prhs,px)
        if self.block:
            return x
        else:
            return x[:self.csr.ndof]
