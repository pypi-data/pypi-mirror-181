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

import time
import atexit
import gmsh
import signal
import numpy as np
import ctypes as c

gmsh.initialize()
gmsh.option.setNumber("General.Terminal",1)

signal.signal(signal.SIGINT, signal.SIG_DFL)

timers = {}

def _np2c(a,dtype=float,order="C") :
    if a is None:
        return None
    tmp = np.require(a,dtype,order)
    r = c.c_void_p(tmp.ctypes.data)
    r.tmp = tmp
    return r

def timeit(func):
    def wrapper(*args, **kwargs):
        self = args[0]
        tic = time.process_time()
        r = func(*args, **kwargs)
        toc = time.process_time()
        name = func.__name__
        timers[name] = timers.get(name, 0) + toc - tic
        return r
    return wrapper

def timeprint(timers) :
    if len(timers) != 0 :
        print(timers)

atexit.register(timeprint, timers)

try :
    from . import mumpslsys
    have_mumps = True
except:
    have_mumps = False

try :
    from . import petsclsys
    have_petsc = True
except :
    have_petsc = False

try :
    from . import petsc4pylsys
    have_petsc4py = True
except :
    have_petsc4py = False

try :
    from . import scipylsys
    have_scipy = True
except :
    have_scipy = False

try :
    from . import pardisolsys
    have_pardiso = True
except :
    have_pardiso = False

def get_linear_system_package(choices=None):
    if choices is None:
        choices = ["pardiso","mumps","petsc","petsc4py","scipy"]
    if isinstance(choices, str):
        choices = [choices]
    for choice in choices:
        if have_mumps and choice=="mumps":
            print("using mumps linear system")
            return mumpslsys.LinearSystem
        if have_petsc and choice=="petsc":
            print("using petsc linear system")
            return petsclsys.LinearSystem
        if have_scipy and choice=="scipy":
            print("using scipy linear system")
            return scipylsys.LinearSystem
        if have_petsc4py and choice=="petsc4py":
            print("using petsc4py linear system")
            return petsc4pylsys.LinearSystem
        if have_pardiso and choice=="pardiso":
            print("using pardiso linear system")
            return pardisolsys.LinearSystem
    raise ValueError("linear system not available")

