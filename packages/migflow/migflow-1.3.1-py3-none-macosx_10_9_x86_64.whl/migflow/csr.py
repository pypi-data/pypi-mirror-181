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
import time
class CSR :

    def __init__(self, idx, constraints):
        shift = 2**32
        self.idx = idx.astype('int64')
        num = np.max(idx)
        self.ndof = num+1
        pairs = (self.idx[:,:,None]*shift+self.idx[:,None,:]).flatten()
        allpairs = [pairs]
        self.constraints = constraints
        for c in constraints :
            num += 1
            pairs = np.ndarray([c.size*2+1],np.uint64)
            pairs[:c.size] = c*shift+num
            pairs[c.size:c.size*2] = num*shift+c
            pairs[c.size*2] = num*shift+num
            allpairs.append(pairs)
        pairs = np.concatenate(allpairs)
        pairs, pmap = np.unique(pairs,return_inverse=True)
        self.map = []
        count = 0
        for p in allpairs :
            self.map.append(pmap[count:count+p.size])
            count += p.size
        self.row = np.hstack([np.array([0],dtype=np.int32),
                              np.cumsum(np.bincount((pairs//shift).astype(np.int32)),
                              dtype=np.int32)])
        self.col = (pairs%shift).astype(np.int32)
        self.size = self.row.size-1
        self.idx = self.idx.reshape(-1)

    def assemble_rhs(self, localv, u, constraints_value) :
        rhs = np.bincount(self.idx, localv, self.size)
        for i, (c, cv) in enumerate(zip(self.constraints, constraints_value)):
            rhs[i+self.ndof] = cv[1] + np.sum(u[c]*cv[0])
        return rhs

    def assemble_mat(self, localm, constraints_value, v) :
        v[:] = np.bincount(self.map[0],localm,self.col.size)
        for cmap, cv in zip (self.map[1:], constraints_value) :
            v += np.bincount(cmap, np.concatenate((cv[0],cv[0],[0])), self.col.size)

