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
import scipy.sparse
import scipy.sparse.linalg
from ._tools import timeit

class LinearSystem :

    def __init__(self, elements, idx, n_fields, options, constraints = [], gid = ()) :
        localsize = idx.shape[1]
        self.rows = np.repeat(idx[:,:,None],localsize,axis=2)
        self.rows = self.rows.reshape([-1])
        self.cols = np.repeat(idx[:,None,:],localsize,axis=1)
        self.cols = self.cols.reshape([-1])
        self.idx = idx
        self.localsize = localsize
        self.constraints = constraints
        self.ndof = np.max(idx)+1
        self.globalsize = self.ndof+len(constraints)
        for i, constraint in enumerate(self.constraints):
            self.rows = np.hstack([self.rows,
                                      constraint,
                                      np.full((constraint.shape[0],),i+self.ndof)])
            self.cols = np.hstack([self.cols,
                                      np.full((constraint.shape[0],),i+self.ndof),
                                      constraint])

    @timeit
    def local_to_global(self,localv,localm, u, constraints_values = []):
        rhs = np.bincount(self.idx.flatten(),localv,self.globalsize)
        localm = localm.reshape([-1])
        for i, (c, cv) in enumerate(zip(self.constraints, constraints_values)):
            localm = np.hstack((localm, cv[0], cv[0]))
            rhs[i+self.ndof] = cv[1] + np.sum(u[c]*cv[0])
        coo = scipy.sparse.coo_matrix((localm, (self.rows,self.cols)))
        self.matrix = coo.tocsc()
        return rhs

    def solvelu(self,rhs) :
        scipy.sparse.linalg.use_solver(useUmfpack=False,assumeSortedIndices=True)
        r =  scipy.sparse.linalg.spsolve(self.matrix,rhs,permc_spec="MMD_ATA")[:self.ndof]
        return r

    def solvegmres(self,rhs) :
        print("ilu")
        #ilu = scipy.sparse.linalg.spilu(self.matrix,fill_factor=0)
        ilu = scipy.sparse.linalg.spilu(self.matrix,drop_tol=1e-5)
        print("ilu solve pc")
        pc = scipy.sparse.linalg.LinearOperator(self.matrix.shape,ilu.solve)
        print("gmres")
        return scipy.sparse.linalg.gmres(self.matrix,rhs,M=pc,restart=30,maxiter=1000)[0][:self.ndof]
        #return scipy.sparse.linalg.splu(self.matrix).solve(rhs)[:self.ndof]
        #return r

    @timeit
    def solve(self,rhs):
        return self.solvelu(rhs)
