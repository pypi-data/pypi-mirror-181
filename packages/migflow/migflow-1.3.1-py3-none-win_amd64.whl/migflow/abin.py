#!/usr/bin/env python
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
import sys
import os

def idxread(path):
    with open(path+".idx","r") as f:
        return np.memmap(f, dtype=np.uint64, order="C", mode="r").reshape(-1,2)

def metaread(path):
    meta = {}
    with open(path+".ameta","r") as f:
        for l in f :
            try :
                assert(l.strip()[0] != '#')
                k, v = l.split(":",1)
            except:
                continue
            v = v.strip()
            k = k.strip()
            if k == "shape" :
                v = list(int(i) for i in v.split())
            meta[k] = v
    return meta

def metawrite(name, meta):
    path = os.path.dirname(name)
    if len(path) != 0:
        os.makedirs(path, exist_ok=True)
    with open(name+".ameta","w") as f:
        for k, v in  meta.items() :
            if k == "shape":
                v = " ".join(str(i) for i in v)
            f.write(f"{k} : {v}\n")


def openread(path):
    meta = metaread(path)
    assert meta["byteorder"] in ("na",sys.byteorder)
    if np.prod(meta["shape"]) == 0:
        return np.ndarray(meta["shape"], meta["dtype"])
    with open(path+".abin","rb") as f:
        return np.memmap(
                f,
                dtype=meta["dtype"],
                shape=tuple(meta["shape"]),
                order="C",
                mode="r")

def openmod(path):
    meta = metaread(path)
    assert meta["byteorder"] in ("na",sys.byteorder)
    if np.prod(meta["shape"]) == 0:
        return np.ndarray(meta["shape"], meta["dtype"])
    with open(path+".abin", "rb+") as f:
        return np.memmap(
                f,
                dtype=meta["dtype"],
                shape=tuple(meta["shape"]),
                order="C",
                mode="r+")

def openwrite(path, shape, dtype, extrameta={}):
    meta = {'shape':shape, 'dtype':dtype, 'byteorder':sys.byteorder}
    for k,v in extrameta.items():
        meta[k] = v
    dtype = str(dtype)
    assert(dtype in ["int32","float32","float64","uint64"])
    metawrite(path, meta)
    if np.prod(shape) == 0:
        return np.ndarray(shape, dtype)
    return np.memmap(
            path+".abin",
            dtype=meta["dtype"],
            shape=tuple(meta["shape"]),
            order="C",
            mode="w+")

def write_array(path, array, extrameta={}):
    openwrite(path, array.shape, array.dtype, extrameta)[:] = array

def append(path, data, extrameta={}):
    if os.path.isfile(path+".ameta"):
        meta = metaread(path)
        assert meta["byteorder"] in ("na",sys.byteorder)
        assert meta["dtype"] == data.dtype
        assert(tuple(meta["shape"][1:]) == data.shape[1:])
        start = meta["shape"][0]
        meta["shape"][0] += data.shape[0]
        for k,v in extrameta.items():
            meta[k] = v
        metawrite(path, meta)
        with open(path+".abin", "ab") as f:
            f.write(data.tobytes())
        return start
    else:
        write_array(path, data, extrameta)
        return  0

def write_iter(path, data, extrameta={}):
    try :
        f = openread(path)
        assert(np.array_equal(f[:-data.shape[0]], data))
        start = f.shape[0]-data.shape[0]
    except:
        start = append(path, data, extrameta)
    with open(path+".idx", "ab") as f:
        f.write(np.array([start, start+data.shape[0]], np.uint64).tobytes())

def get_iter(path, i):
    idx = idxread(path)
    return openread(path)[idx[i,0]:idx[i,1]]

if __name__ == "__main__":
    name = sys.argv[1]
    if name.endswith(".abin") : name = name[:-5]
    if name.endswith(".ameta") : name = name[:-6]
    print(metaread(name))
    print(openread(name))
    

