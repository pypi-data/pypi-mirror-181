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

"""Model for Immersed Granular Flow: Fluid user interface

    Contact: jonathan.lambrechts@uclouvain.be
    Webpage: www.migflow.be

    MigFlow computes immersed granular flows using an unresolved FEM-DEM model.
    The continuous phase (mixture) is computed by solving averaged Navier-Stokes equations on unstructured meshes with the continuous finite element method.
"""

from ctypes import *
import ctypes as c
import numpy as np
import os
import sys
import json
import subprocess
from . import VTK, abin
from ._tools import gmsh, get_linear_system_package, _np2c, timeit
from typing import Union, List, Dict

dir_path = os.path.dirname(os.path.realpath(__file__))
lib2 = np.ctypeslib.load_library("libmbfluid2",dir_path)
lib3 = np.ctypeslib.load_library("libmbfluid3",dir_path)

BNDCB = CFUNCTYPE(None,c_int,POINTER(c_double),POINTER(c_double))
class _Bnd :
    def __init__(self, b, dim) :
        self._b = b
        self._dim = dim
    def apply(self, n, xp, vp) :
        nv = len(self._b)
        x = np.frombuffer(cast(xp, POINTER(int(n)*self._dim*c_double)).contents).reshape([n,-1])
        v = np.frombuffer(cast(vp, POINTER(int(n)*nv*c_double)).contents).reshape([n,nv])
        for i in range(nv):
            if callable(self._b[i]) :
                v[:,i] = self._b[i](x)
            else :
                v[:,i] = self._b[i]

def removeprefix(str:str, prefix:str)->str:
    return str[len(prefix):] if str.startswith(prefix) else str

def _is_string(s) :
    if sys.version_info >= (3, 0):
        return isinstance(s, str)
    else :
        return isinstance(s, basestring)

def _load_msh(mesh_file_name, lib, dim) :
    """
    mesh_file_name: Name of the mesh.msh file containing information about the domain
    """
    etype = 2 if dim == 2 else 4
    betype = 1 if dim == 2 else 2
    if mesh_file_name is not None:
        gmsh.model.add("tmp")
        gmsh.open(mesh_file_name)
    gmsh.model.mesh.renumberNodes()
    ntags, x, _ = gmsh.model.mesh.getNodes()
    x = x.reshape([-1,3])
    x[ntags-1] = x
    _, el = gmsh.model.mesh.getElementsByType(etype)
    el = (el-1).reshape([-1,dim+1])
    bnd = []
    btag = []
    bname = []
    periodic_nodes = []
    for edim, etag  in gmsh.model.getEntities() :
        ptag, cnodes, pnodes, _ = gmsh.model.mesh.getPeriodicNodes(edim, etag)
        if ptag == etag or len(cnodes) == 0: continue
        periodic_nodes.extend(zip(cnodes,pnodes))
    for ip,(pdim, ptag)  in enumerate(gmsh.model.getPhysicalGroups(dim-1)) :
        bname.append(gmsh.model.getPhysicalName(pdim,ptag))
        for etag in gmsh.model.getEntitiesForPhysicalGroup(pdim, ptag):
            for eltype, _, elnodes in zip(*gmsh.model.mesh.getElements(pdim,etag)):
                if eltype != betype:
                    continue
                bnd.append(elnodes-1)
                btag.append(np.full((elnodes.shape[0]//dim), ip))
    periodic_nodes = np.array(periodic_nodes,dtype=np.int32).reshape([-1,2])-1
    bnd = np.hstack(bnd).reshape([-1,dim])
    btag = np.hstack(btag)
    cbname = (c_char_p*len(bname))(*(i.encode() for i in bname))

    # remove nodes and boundaries not connected to elements
    keepnodes = np.full(x.shape[0], False, bool)
    keepnodes[el] = True
    newidx = np.cumsum(keepnodes)-1
    el = newidx[el]
    x = x[keepnodes,:]
    periodic_nodes = newidx[periodic_nodes]
    keepbnd = np.full(bnd.shape[0], True, bool)
    for i in range(dim) :
        keepbnd = np.logical_and(keepbnd, keepnodes[bnd[:,i]])
    bnd = newidx[bnd][keepbnd,:]
    btag = btag[keepbnd]
    is_parent = np.full([x.shape[0]],True, bool)
    is_parent[periodic_nodes[:,0]] = False
    periodic_parent = np.cumsum(is_parent)-1
    periodic_parent[periodic_nodes[:,0]] = periodic_parent[periodic_nodes[:,1]]
    lib.mesh_new_from_elements.restype = c_void_p
    return c_void_p(lib.mesh_new_from_elements(
            c_int(x.shape[0]),_np2c(x,np.float64),
            c_int(el.shape[0]),_np2c(el,np.int32),
            c_int(bnd.shape[0]),_np2c(bnd,np.int32),
            _np2c(btag,np.int32),c_int(len(cbname)),cbname,
            _np2c(periodic_parent,np.int32)))


class FluidProblem :
    """Creates the numerical representation of the fluid."""

    def __init__(self, dim:int, g:np.ndarray, mu:list, rho:list, sigma:float=0, coeff_stab:float=0.01, volume_drag:float=0., quadratic_drag:float=0., solver:str=None, solver_options:str="", drag_in_stab:int=1, drag_coefficient_factor:int=1, temporal:bool=True, advection:bool=True, usolid:bool=False, p2p1:bool=False, full_implicit:bool=False, model_b:bool=False) -> None:
        """Builds the fluid structure.

        Args:
            dim: Dimension of the problem
            g: Gravity vector
            mu: List of fluid phases dynamic viscosities (this should be a vector whom dimension specify if there is one or two fluid)
            rho: List of fluid phases densities (this should be a vector whom dimension specify if there is one or two fluid)
            sigma: Surface tension (only when there are two fluids)
            coeff_stab: Optional argument used as coefficient for extra diffusivity added to stabilise the advection of concentration (only for two fluid problem)
            volume_drag: Enables volumetric drag : -volume_drag * u[i] 
            quadratic_drag: Enables quadratic drag : -quadratic_drag*||uold|| * u[i]
            solver: possible solver are "mumps", "petsc", "petsc4py", "scipy"
            solver_options: Optional argument to specify solver option
            drag_in_stab: States if the drag force is in the stabilisation term
            drag_coefficient_factor: Factor multiplicating the drag coefficient
            temporal: Enables d/dt (i.e. False = steady)
            advection: Enables advective terms (i.e. False = Stokes, True = Navier-Stokes
            usolid: if False, div.u_solid is evaluated = (porosity-old_porosity)/dt
            p2p1: if True, use P2 element for velocity fields and P1 element for pressure field, else a stabilised P1-P1 formulation is used
            full_implicit: If False, the linearised averaged Navier-Stokes equation are considered else a fully implicit formulation is used
            model_b: If True, the buoyancy term is assumed to be expressed as an additional drag 
        Raises:
            ValueError: If the dimension differs from 2 or 3
            NameError: If C builder cannot be found
        """
        self.linear_system_package = get_linear_system_package(solver)
        self.solver_options = solver_options
        self.strong_cb_ref = []
        self.weak_cb_ref = {}
        self.sys = None
        self.mean_pressure = None
        self.full_implicit = full_implicit
        self.constraint_value = []
        self.constraint_index = []
        if dim == 2 :
            self._lib = lib2
        elif dim == 3 :
            self._lib = lib3
        else :
            raise ValueError("dim should be 2 or 3.")
        self._lib.fluid_problem_new.restype = c_void_p
        n_fluids = np.require(rho,"float","C").reshape([-1]).shape[0]
        self._n_fluids = n_fluids
        self._dim = dim
        self._fp = c_void_p(self._lib.fluid_problem_new(_np2c(g), c_int(n_fluids), _np2c(mu), _np2c(rho), c_double(sigma), c_double(coeff_stab), c_double(volume_drag), c_double(quadratic_drag), c_int(drag_in_stab), c_double(drag_coefficient_factor),c_int(temporal), c_int(advection), c_int(usolid), c_int(p2p1), c_int(full_implicit), c_int(model_b)))
        if self._fp == None :
            raise NameError("Cannot create fluid problem.")

    def __del__(self):
        """Deletes the fluid structure."""
        if(self._fp is not None) :
            self._lib.fluid_problem_free(self._fp)

    def set_coordinates(self, x:np.ndarray):
        """Sets the coordinates of the mesh nodes

        Args:
            x: new nodes positions
        """
        self._lib.fluid_problem_set_coordinates(self._fp, _np2c(x))


    def set_mesh(self, nodes:np.ndarray, elements:np.ndarray, boundaries:list) :
        """Sets the domain geometry for the fluid computation.

        Args:
            nodes: (n_node, dimension) numpy float array of the nodes coordinates
            elements: (n_elements, dimension+1) numpy int array of the elements
            boundaries: [(name, (n_elements, dimension))] list of pair of name (string)
            and numpy int array with the corresponding boundary elements
        """
        assert (len(nodes.shape) == 2 and nodes.shape[1] == 3)
        assert (len(elements.shape) == 2 and elements.shape[1] == self.dimension()+1)
        bndnodes = []
        bndtags = []
        bndnames = []
        for i,(n, e) in enumerate(boundaries):
            assert (len(e.shape) == 2 and e.shape[1] == self.dimension())
            bndnames.append(n)
            bndnodes.append(e)
            bndtags.append(np.full(e.shape[0],i))
        bndnodes = np.row_stack(bndnodes)
        bndtags = np.hstack(bndtags)
        cbname = (c_char_p*len(bndnames))(*(i.encode() for i in bndnames))
        self._lib.mesh_new_from_elements.restype = c_void_p
        mesh = c_void_p(self._lib.mesh_new_from_elements(
                c_int(nodes.shape[0]),_np2c(nodes,np.float64),
                c_int(elements.shape[0]),_np2c(elements,np.int32),
                c_int(bndnodes.shape[0]),_np2c(bndnodes,np.int32),
                _np2c(bndtags,np.int32),c_int(len(cbname)),cbname,
                None))
        self._lib.fluid_problem_set_mesh(self._fp, mesh)
        self.sys = None

    def load_msh(self, filename:str) :
        """Sets the domain geometry for the fluid computation.

        Args:
            filename: Name of the msh file. If None the current gmsh model is loaded without the need to a msh file.
        """
        mesh = _load_msh(filename, self._lib, self.dimension())
        self._lib.fluid_problem_set_mesh(self._fp, mesh)
        self.sys = None
        if filename is not None:
            gmsh.model.remove()

    def set_mean_pressure(self, mean_pressure:float):
        """Enables the nodal mean pressure constraint and imposes its value. 

        Args:
            mean_pressure: add a constraint to impose \sum_i vol_i p_i = mean_pressure*volume
        """
        self.mean_pressure = mean_pressure
        self.sys = None

    def set_weak_boundary(self, tag:Union[str, List[str]], pressure:Union[float, callable]=None, velocity:Union[float, callable]=None, concentration:Union[float, callable]=None, viscous_flag:bool=None):
        """Sets the weak boundaries (=normal fluxes) for the fluid problem.

        Args:
            tag: Physical tag (or list of tags), set in the mesh, of the weak boundaries
            pressure: The pressure value if imposed (callback or number)
            velocity: The velocity value if imposed (callback or number)
            concentration: Concentration outside the boundary
            viscous_flag: Flag to compute the viscous term at the boundary
        """
        if not _is_string(tag) :
            for t in tag :
                self.set_weak_boundary(t,pressure, velocity, viscous_flag)
            return
        type = 0 if pressure is None and velocity is None else 1
        if viscous_flag is None:
            viscous_flag = 1 if velocity is not None or pressure is not None else 0
        vid=pid=cid=aid=-1
        cb_or_value=[]
        is_nodal_values=None
        if pressure is not None:
            pressure=np.asarray(pressure)
            is_nodal_values = pressure.ndim > 0
            pid = len(cb_or_value)
            cb_or_value.append(pressure)
        if velocity is not None:
            velocity = np.asarray(velocity)
            assert(((velocity.ndim > 1) == is_nodal_values) or (is_nodal_values is None))
            if velocity.ndim > 1:
                is_nodal_values = True
            vid = len(cb_or_value)
            for i in range(self._dim):
                cb_or_value.append(velocity[...,i])
        if self._n_fluids == 2 and concentration is not None:
            concentration = np.asarray(concentration)
            assert(((concentration.ndim > 0) == is_nodal_values) or (is_nodal_values is None))
            if concentration.ndim > 1:
                is_nodal_values = True
            aid = len(cb_or_value)
            cb_or_value.append(concentration)
        if is_nodal_values:
            values = np.stack(cb_or_value, axis=2)
            assert(values.ndim == 3 and np.all(values.shape[:2]==self.mesh_boundaries()[tag.encode()].shape))
            bndcb = None
        else:
            values = None
            cb_or_value = [cbv.tolist() for cbv in cb_or_value]
            bndcb = BNDCB(_Bnd(cb_or_value,self._dim).apply)
        self.weak_cb_ref[tag] = (bndcb, values)
        self._lib.fluid_problem_set_weak_boundary(self._fp,tag.encode(), c_int(type), bndcb, _np2c(values), c_int(vid), c_int(pid), c_int(cid), c_int(aid), c_int(int(viscous_flag)))

    def set_wall_boundary(self, tag:Union[str, List[str]], pressure:Union[float, callable]=None, velocity:Union[float, callable]=None, viscous_flag:bool=None) :
        """Sets the weak wall boundaries (=normal fluxes) for the fluid problem.

        Args:
            tag: Physical tag (or list of tags), set in the mesh, of the wall boundaries
            pressure: The pressure value if imposed (callback or number)
            velocity: The velocity value if imposed (callback or number)
            viscous_flag: Flag to compute the viscous term at the boundary
        """
        if not _is_string(tag) :
            for t in tag :
                self.set_wall_boundary(t,pressure, velocity, viscous_flag)
            return
        pid = -1
        vid = -1
        if viscous_flag is None:
            viscous_flag = 1 if velocity is not None else 0
        cb_or_value = []
        is_nodal_values = None
        if pressure is not None:
            pressure = np.asarray(pressure)
            is_nodal_values = pressure.ndim > 0
            pid = len(cb_or_value)
            cb_or_value.append(pressure)

        if velocity is not None:
            velocity = np.asarray(velocity)
            assert(((velocity.ndim > 1) == is_nodal_values) or (is_nodal_values is None))
            if velocity.ndim > 1:
                is_nodal_values = True
            vid = len(cb_or_value)
            for i in range(self._dim):
                cb_or_value.append(velocity[...,i])

        if is_nodal_values:
            values = np.stack(cb_or_value, axis=2)
            assert(values.ndim == 3 and np.all(values.shape[:2]==self.mesh_boundaries()[tag.encode()].shape))
            bndcb = None
        else:
            values = None
            cb_or_value = [cbv.tolist() for cbv in cb_or_value]
            bndcb = BNDCB(_Bnd(cb_or_value,self._dim).apply)

        self.weak_cb_ref[tag] = (bndcb, values)
        self._lib.fluid_problem_set_weak_boundary(self._fp,tag.encode(), c_int(0), bndcb, _np2c(values), c_int(vid), c_int(pid), c_int(-1), c_int(-1), c_int(int(viscous_flag)))

    def set_symmetry_boundary(self, tag:Union[str,List[str]], pressure:Union[float, callable]=None):
        """Sets the weak symmetry boundaries (=normal fluxes) for the fluid problem.

        Args:
            tag: Physical tag (or list of tags), set in the mesh file, of the symmetry boundaries
            pressure: The pressure value if imposed (callback or number)
        """
        if not _is_string(tag):
            for t in tag:
                self.set_symmetry_boundary(t,pressure)
            return
        pid = -1
        vid = -1
        cb_or_value = []
        is_nodal_values = None
        if pressure is not None:
            pressure = np.asarray(pressure)
            is_nodal_values = pressure.ndim > 0
            pid = len(cb_or_value)
            cb_or_value.append(pressure)

        if is_nodal_values:
            values = np.stack(cb_or_value, axis=2)
            assert(values.ndim == 3 and np.all(values.shape[:2]==self.mesh_boundaries()[tag.encode()].shape))
            bndcb = None
        else:
            values = None
            bndcb = BNDCB(_Bnd(cb_or_value,self._dim).apply)

        self.weak_cb_ref[tag] = (bndcb, values)
        self._lib.fluid_problem_set_weak_boundary(self._fp,tag.encode(), c_int(0), bndcb, _np2c(values), c_int(vid), c_int(pid), c_int(-1), c_int(-1), c_int(-1))

    def set_open_boundary(self, tag:Union[str, List[str]], velocity:Union[float, callable]=None, pressure:Union[float, callable]=None, concentration:Union[float, callable]=None, viscous_flag:bool=1):
        """Sets the weak open boundaries (=normal fluxes) for the fluid problem.

        Args:
            tag: Physical tag (or list of tags), set in the mesh, of the open boundaries
            velocity: The velocity value if imposed (callback or number)
            pressure: The pressure value if imposed (callback or number)
            concentration: Concentration outside the boundary
            viscous_flag: Flag to compute the viscous term at the boundary
        """
        if not _is_string(tag) :
            for t in tag :
                self.set_open_boundary(t,velocity, pressure, concentration, viscous_flag)
            return
        pid = -1
        vid = -1
        aid = -1
        cb_or_value = []
        is_nodal_values = None
        if pressure is not None:
            pressure = np.asarray(pressure)
            is_nodal_values = pressure.ndim > 0
            pid = len(cb_or_value)
            cb_or_value.append(pressure)

        if velocity is not None:
            velocity = np.asarray(velocity)
            assert(((velocity.ndim > 1) == is_nodal_values) or (is_nodal_values is None))
            if velocity.ndim > 1:
                is_nodal_values = True
            vid = len(cb_or_value)
            for i in range(self._dim):
                cb_or_value.append(velocity[...,i])

        if self._n_fluids == 2 and concentration is not None:
            concentration = np.asarray(concentration)
            assert(((concentration.ndim > 0) == is_nodal_values) or (is_nodal_values is None))
            if concentration.ndim > 1:
                is_nodal_values = True
            aid = len(cb_or_value)
            cb_or_value.append(concentration)

        if is_nodal_values:
            values = np.stack(cb_or_value, axis=2)
            assert(values.ndim == 3 and np.all(values.shape[:2]==self.mesh_boundaries()[tag.encode()].shape))
            bndcb = None
        else:
            values = None
            cb_or_value = [cbv.tolist() for cbv in cb_or_value]
            bndcb = BNDCB(_Bnd(cb_or_value,self._dim).apply)
        self.weak_cb_ref[tag] = (bndcb, values)
        self._lib.fluid_problem_set_weak_boundary(self._fp,tag.encode(), c_int(1), bndcb, _np2c(values), c_int(vid), c_int(pid), c_int(-1), c_int(aid), c_int(int(viscous_flag)))

    def set_weak_boundary_nodal_values(self, tag:str, values:np.ndarray):
        """Set the nodal values to use for the weak boundary instead of using a callback or a prescribed value. Only available for p1p1 formulation.

        Args:
            tag : Physical tag (or list of tags), set in the mesh
            values : nodal values imposed on the boundary
        
        Raises :
            ValueError: if the tag is not found
        """
        
        try:
            _, old_values = self.weak_cb_ref[tag]
        except:
            raise(ValueError("Tag not found !"))
        self.weak_cb_ref[tag] = (None, values.reshape(old_values.shape))
        self._lib.fluid_problem_set_nodal_values(self._fp, tag.encode(), _np2c(values))

    def set_strong_boundary(self, tag:str, pressure:Union[float, callable]=None, velocity:Union[float, callable]=None, velocity_x:Union[float, callable]=None, velocity_y:Union[float, callable]=None, velocity_z:Union[float, callable]=None, solution:Union[float, callable]=None):
        """Sets the strong boundaries (=constrains) for the fluid problem.

        Args:
            tag: Physical tag (set in the mesh) of the boundary on which the constraint is added
            pressure: value or callback assigned to the pressure field
            velocity: value or callback assigned to the velocity field
            velocity_x: value or callback assigned to the velocity_x field
            velocity_y: value or callback assigned to the velocity_y field
            velocity_z: value or callback assigned to the velocity_z field
            solution: value or callback assigned to the solution field
        """
        if solution is not None and (velocity is not None or pressure is not None or velocity_x is not None or velocity_y is not None or velocity_z is not None):
            print("Error in set_strong_boundary : solution cannot be imposed with another field !")
            exit(0) 
        if velocity is not None and (velocity_x is not None or velocity_y is not None or velocity_z is not None):
            print("Error in set_strong_boundary : velocity vector and its component cannot be imposed during the same call !")
            exit(0) 
        if pressure is not None:
            bndcb = BNDCB(_Bnd([pressure], self._dim).apply)
            self.strong_cb_ref.append(bndcb)
            self._lib.fluid_problem_set_strong_boundary(self._fp, tag.encode(), c_int(self._dim), bndcb)
        if velocity_x is not None:
            bndcb = BNDCB(_Bnd([velocity_x], self._dim).apply)
            self.strong_cb_ref.append(bndcb)
            self._lib.fluid_problem_set_strong_boundary(self._fp, tag.encode(), c_int(0), bndcb)
        if velocity_y is not None:
            bndcb = BNDCB(_Bnd([velocity_y], self._dim).apply)
            self.strong_cb_ref.append(bndcb)
            self._lib.fluid_problem_set_strong_boundary(self._fp, tag.encode(), c_int(1), bndcb)
        if velocity_z is not None and self._dim == 3:
            bndcb = BNDCB(_Bnd([velocity_z], self._dim).apply)
            self.strong_cb_ref.append(bndcb)
            self._lib.fluid_problem_set_strong_boundary(self._fp, tag.encode(), c_int(2), bndcb)
        if velocity is not None:
            if callable(velocity):
                print("Velocity cannot be callable ! You should prescribe a list of callable or value")
                exit(0)
            else:
                for i,v in enumerate(velocity):
                    bndcb = BNDCB(_Bnd([v], self._dim).apply)
                    self.strong_cb_ref.append(bndcb)
                    self._lib.fluid_problem_set_strong_boundary(self._fp, tag.encode(), c_int(i), bndcb)
        if solution is not None:
            if callable(solution):
                print("Solution cannot be callable ! You should prescribe a list of callable or value")
                exit(0)
            else:
                for i,s in enumerate(solution):
                    bndcb = BNDCB(_Bnd([s], self._dim).apply)
                    self.strong_cb_ref.append(bndcb)
                    self._lib.fluid_problem_set_strong_boundary(self._fp, tag.encode(), c_int(i), bndcb)

    def adapt_mesh(self, path_to_mesh:str="adapt/mesh", lcmax:float=None, lcmin:float=None, n_el:int=None, old_n_particles:int=0, old_particle_position:np.ndarray=None, old_particle_volume:np.ndarray=None) :
        """Adapts the mesh.

        Args:
            old_n_particles: Number of particles at the previous time step
            old_particle_position: Position of the particles at the previous time step
            old_particle_volume: Volume of the particles at the previous time step
        """
        mesh = _load_msh(None, self._lib, self.dimension())
        self._lib.fluid_problem_adapt_mesh(self._fp, mesh, c_int(old_n_particles), _np2c(old_particle_position), _np2c(old_particle_volume))
        self.sys = None

    def mesh_boundaries(self) -> dict:
        """ Returns the mesh boundaries information as a dictionnary : {boundary_number : edges}
        Returns:
            dict: Mesh  information : {boundary_number : edges}
        """
        n = self._lib.fluid_problem_mesh_n_boundaries(self._fp)
        bnds = {}
        for i in range(n) :
            bsize = c_int()
            bname = c_char_p()
            self._lib.fluid_problem_mesh_boundary_info(self._fp, c_int(i),byref(bname),byref(bsize))
            nodes = np.ndarray([bsize.value,self._dim],np.int32)
            self._lib.fluid_problem_mesh_boundary_interface_nodes(self._fp,c_int(i),c_void_p(nodes.ctypes.data))
            bnds[bname.value] = nodes
        return bnds

    def get_p1_element(self)->str:
        """Returns the P1 element used -> "triangle_p1" or "tetrahedron_p1"

        Returns:
            str: "triangle_p1"
        """
        self._lib.fluid_problem_get_p1_element.restype = c.c_char_p
        return self._lib.fluid_problem_get_p1_element(self._fp)

    def get_pressure_element(self)->str:
        """Returns the discretisation element of the pressure field
        Returns:
            str: pressure element
        """
        return self.get_p1_element()

    def get_velocity_element(self)->str:
        """Returns the discretisation element of the velocity field
        Returns:
            str: velocity element
        """
        self._lib.fluid_problem_get_velocity_element.restype = c.c_char_p
        return self._lib.fluid_problem_get_velocity_element(self._fp)


    def get_default_export(self, dtype=np.float64)->dict:
        """Returns the default fields to write in your output as a dictionnary {field : (values, discretisation_element)}
        Args:
            dtype: numpy representation. Defaults to np.float64.

        Returns:
            dict: default fields
        """
        p1_element = self.get_p1_element()
        velocity_element = self.get_velocity_element()
        fields = {"pressure":(self.pressure().astype(dtype, copy=False), p1_element),
                  "porosity":(self.porosity().astype(dtype, copy=False), p1_element),
                  "old_porosity":(self.old_porosity().astype(dtype, copy=False), p1_element),
                  "velocity":(self.velocity().astype(dtype, copy=False), velocity_element),
                  "u_solid":(self.u_solid().astype(dtype, copy=False), p1_element),
                  "u_mesh":(self.mesh_velocity().astype(dtype, copy=False), p1_element)
                }
        if self.n_fluids() == 2:
            fields["concentration"] = (self.concentration_dg().reshape(-1,1).astype(dtype, copy=False), p1_element+b"_dg")
        return fields

    def write_mig(self, output_dir:str, t:float, fields:dict=None, mesh_dtype:np.dtype=np.float64):
        """ Writes the output files for post-visualization. Metadata are stored into a file called "fluid.migf" while the data are stored into the "fluid" directory. 
        Args:
            output_dir : Output directory
            t : Computational time
            extra_fields : extra field as a dictionnary {name : values at p1 degree of freedom}
        """
        exported_mappings = []
        field_list = {} 
        def write_field(name, v, element):
            meta = {"element":element.decode()}
            etype = {b"p1":"P1",b"p1_dg":"P1DG",b"p2":"P2",b"p2_dg":"P2DG"}[element[element.find(b"_")+1:]]
            field_list[removeprefix(name,"data/")] = etype
            if etype not in exported_mappings:
                exported_mappings.append(etype)
                abin.write_iter(odir+"/mappings/"+element.decode(), self.get_mapping(etype))
            abin.write_iter(odir+"/"+name, v, meta)
        odir = (output_dir+"/fluid")
        bnd_nodes = self.mesh_boundaries().values()
        bnd_tag = np.hstack([np.repeat(i, bnd.shape[0]) for i,bnd in enumerate(bnd_nodes)])
        bnd_nodes = np.concatenate(list(bnd_nodes))
        bnd = np.concatenate([bnd_nodes, bnd_tag.reshape(-1,1)], axis=1)
        abin.write_iter(odir+"/mesh/topology", self.elements())
        abin.write_iter(odir+"/mesh/geometry", self.coordinates().astype(mesh_dtype, copy=False))
        abin.write_iter(odir+"/mesh/boundary", bnd.astype(np.int32))
        abin.write_iter(odir+"/mesh/periodic", self.parent_nodes())
        abin.append(odir+"/time", np.array([t],np.float64))
        if fields is None:
            fields = self.get_default_export()
        for key, value in zip(fields.keys(), fields.values()):
            write_field("data/"+key, value[0], value[1])
        with open(output_dir+"/fluid.migf", "w", encoding="utf-8") as f:
            tagname = list(self.mesh_boundaries().keys())
            bnd = [name.decode("utf-8") for name in tagname]
            data = {"fields":field_list,
                    "version":"1.0",
                    "dimension":self._dim,
                    "boundary_names":bnd}
            f.write(json.dumps(data, indent=2, sort_keys=True))

    def read_mig(self, odir:str, t:float):
        """Reads output file to reload computation.

        Args:
            odir:  Directory in which to read the file
            t:  Time at which to read the file
        """
        dirname = odir+'/fluid/'
        time = abin.openread(dirname + "time")[:]
        itime = np.searchsorted(time, t)
        with open(odir+"/fluid.migf") as f:
            info = json.load(f)
        bnd = info["boundary_names"]
        topo = abin.get_iter(dirname+"mesh/topology", itime)
        nodes = abin.get_iter(dirname+"mesh/geometry", itime)
        parent_nodes = abin.get_iter(dirname+"mesh/periodic", itime)
        bnd_data = abin.get_iter(dirname+"mesh/boundary", itime)
        bnds = bnd_data[:,:self._dim]
        bnd_tags = bnd_data[:,self._dim]
        tagmap = {tag:i for i,tag in enumerate(np.unique(bnd_tags))}
        bnd_tags = np.array([tagmap[tag] for tag in bnd_tags], np.int32)
        cbnd_names = (c_char_p*len(bnd))(*(i.encode() for i in bnd))
        self._lib.mesh_new_from_elements.restype = c_void_p
        _mesh = c_void_p(self._lib.mesh_new_from_elements(
                c_int(nodes.shape[0]),_np2c(nodes,np.float64),
                c_int(topo.shape[0]),_np2c(topo,np.int32),
                c_int(bnds.shape[0]),_np2c(bnds,np.int32),
                _np2c(bnd_tags,np.int32),c_int(len(cbnd_names)),cbnd_names,
                _np2c(parent_nodes, np.int32)))
        self._lib.fluid_problem_set_mesh(self._fp, _mesh)
        sol = self.solution()
        idxP = self.pressure_index().reshape(-1)
        idxU = self.velocity_index().reshape(-1)
        sol[idxU] = abin.get_iter(dirname+"data/velocity", itime)[:,:self._dim].reshape(-1)
        sol[idxP] = abin.get_iter(dirname+"data/pressure", itime).reshape(-1)
        self.porosity()[:] = abin.get_iter(dirname+"data/porosity", itime)
        self.old_porosity()[:] = abin.get_iter(dirname+"data/old_porosity", itime)
        if self._n_fluids == 2 :
            a = abin.get_iter(dirname+"data/concentration", itime)
            self.concentration_dg()[:] = a.reshape(-1,self._dim+1)
        self.sys = None

    def write_vtk(self, output_dir, it ,t):
        """(DEPRECATED) Writes output file for post-visualization.
        Args:
            output_dir: Output directory
            it: Computation iteration
            t: Computation time
        """
        print("WRITE_VTK IS DEPRECATED : USE WRITE_MIG INSTEAD ! \n")
        da = self.concentration_dg_grad()
        cell_data = []
        v = self.solution()[self.velocity_index()]
        p = self.solution()[self.pressure_index()]
        if self._dim == 2 :
            da = np.insert(da,self._dim,0,axis=1)
            v  = np.insert(v,self._dim,0,axis=1)
        data = [
            ("pressure",p.reshape(-1,1)),
            ("porosity",self.porosity()),
            ("old_porosity",self.old_porosity()),
            ("parent_node_id", self.parent_nodes())
            ]
        if self._n_fluids == 2 :
            data.append(("grad",da))
            cell_data.append(("curvature",self.curvature()))
            cell_data.append(("concentration",self.concentration_dg()))
            cell_data.append(("stab",self._get_matrix("stab_param",self.n_elements(),1)))
        field_data = [(b"Boundary %s"%(name), nodes) for name,nodes in self.mesh_boundaries().items()]
        connectivity = self.elements()
        types = np.repeat([5 if self._dim == 2 else 10],connectivity.shape[0])
        offsets = np.cumsum(np.repeat([self._dim+1],connectivity.shape[0])).astype(np.int32)
        isp2p1 = v.shape[0] != p.shape[0]
        if isp2p1 :
            pass
        else:
            data.append(("velocity", v))
        VTK.write(output_dir+"/fluid",it,t,(types,connectivity,offsets),self.coordinates(),data,field_data,cell_data)

    def read_vtk(self, dirname, i):
        """(DEPRECATED) Reads output file to reload computation.

        Args:
            filename: Name of the file to read
        """
        print("READ_VTK IS DEPRECATED : USE READ_MIG INSTEAD ! \n")
        filename = dirname + "/fluid_%05d.vtu"%i
        x,cells,data,cdata,fdata = VTK.read(filename)
        mesh_boundaries = {name[9:]:nodes for name,nodes in fdata.items() if name.startswith("Boundary ")}
        cbnd_names = (c_char_p*len(mesh_boundaries))(*(i.encode() for i in mesh_boundaries.keys()))
        el = cells["connectivity"].reshape([-1,self._dim+1])
        nbnd = len(mesh_boundaries)
        bnds = np.vstack(list(mesh_boundaries.values()))
        bnd_tags = np.repeat(list(range(nbnd)),list([v.shape[0] for v in mesh_boundaries.values()]))
        bnd_tags = np.require(bnd_tags,np.int32,"C")
        self._lib.mesh_new_from_elements.restype = c_void_p
        _mesh = c_void_p(self._lib.mesh_new_from_elements(
                c_int(x.shape[0]),_np2c(x,np.float64),
                c_int(el.shape[0]),_np2c(el,np.int32),
                c_int(bnds.shape[0]),_np2c(bnds,np.int32),
                _np2c(bnd_tags,np.int32),c_int(len(cbnd_names)),cbnd_names,
                _np2c(data["parent_node_id"],np.int32) if "parent_node_id"  in data else None))
        self._lib.fluid_problem_set_mesh(self._fp, _mesh)
        sol = self.solution()
        idxP = self.pressure_index()
        idxU = self.velocity_index()
        isp2p1 = idxP.shape[0] != idxU.shape[0]
        velocity = fdata['velocity'] if isp2p1 else data["velocity"]
        sol[idxU] = velocity[:,:self._dim]
        sol[idxP] = data["pressure"][:,0]
        if self._n_fluids == 2 :
            self.concentration_dg()[:] = cdata["concentration"]
        self.porosity()[:] = data["porosity"].reshape(-1)
        self.old_porosity()[:] = data["old_porosity"]
        self.sys = None

    def compute_node_force(self, dt:float) :
        """Computes the forces to apply on each grain resulting from the fluid motion.

        Args:
            dt: Computation time step
        """
        forces = np.ndarray([self.n_particles,self._dim],"d",order="C")
        self._lib.fluid_problem_compute_node_particle_force(self._fp, c_double(dt), c_void_p(forces.ctypes.data))
        return forces

    def compute_node_torque(self, dt:float) :
        """Computes the angular drags to apply on each grain resulting from the fluid motion.
        Only in 2D
        Args:
            dt: Computation time step
        """
        torques = np.ndarray([self.n_particles,1],"d",order="C")

        self._lib.fluid_problem_compute_node_particle_torque(self._fp, c_double(dt), c_void_p(torques.ctypes.data))
        return torques        
    
    def add_constraint(self, constraint_index, constraint_value):
        self.constraint_index.append(constraint_index)
        self.constraint_value.append(constraint_value)

    @timeit
    def full_implicit_euler(self, dt:float, tol:float=1e-6, reduced_gravity:int=0, stab_param:float=0., initial_guess:np.ndarray=None, itermax:int=100) :
        """Solves the fluid equations using a Newton-Raphson method.

        Args:
            dt: Computation time step
            tol: tolerance to stop the iterative method if the residual norm is smaller than this value
            reduced_graviy: If True simulations are run with a reduced gravity (not to use in two fluids simulations)
            stab_param: If zero pspg/supg/lsic stabilisation is computed otherwise the value is used as a coefficient for a pressure laplacian stabilisation term
            initial_guess: initial candidate for the Newton-Raphson method
            itermax : maximal number of iteration of the Newton-Raphson method
        """
        it = 0
        self._lib.fluid_problem_set_reduced_gravity(self._fp,c_int(reduced_gravity))
        self._lib.fluid_problem_set_stab_param(self._fp,c_double(stab_param))
        self._lib.fluid_problem_apply_boundary_conditions(self._fp)
        solution_old = self.solution().copy()
        if initial_guess is not None:
            self.solution()[:] = initial_guess
        idx = self.global_map().reshape(self.n_elements(),-1)
        res_norm = tol+1
        while res_norm > tol and it < itermax:
            self._lib.fluid_problem_reset_boundary_force(self._fp)
            self._lib.fluid_problem_compute_stab_parameters(self._fp,c_double(dt))
            if self.sys is None :
                constraints = self.constraint_index.copy()
                if self.mean_pressure is not None:
                    constraint = self.pressure_index()
                    constraints.append(constraint)
                self.sys = self.linear_system_package(self.elements(), idx, self.n_fields(), self.solver_options, constraints, (self.velocity_index(), self.pressure_index()))
            sys = self.sys
            localv = np.ndarray([self.local_size()*self.n_elements()])
            localm = np.ndarray([self.local_size()**2*self.n_elements()])
            self._lib.fluid_problem_assemble_system(self._fp,_np2c(solution_old),c_double(dt),_np2c(localv),_np2c(localm))
            constraint_value = self.constraint_value.copy()
            if self.mean_pressure is not None:
                constraint_value.append((self.node_volume().reshape([-1]), -self.mean_pressure*np.sum(self.node_volume())))
            rhs = sys.local_to_global(localv, localm, self.solution(), constraint_value)
            s = sys.solve(rhs)
            self.solution()[:] -= s
            it +=1
            self._lib.fluid_problem_assemble_system(self._fp,_np2c(solution_old),c_double(dt),_np2c(localv),_np2c(localm))
            print(constraint_value)
            residual = sys.local_to_global(localv,localm,self.solution().reshape([-1]),constraint_value)
            res_norm = np.linalg.norm(residual)
            self._lib.fluid_problem_node_force_volume(self._fp,_np2c(solution_old),c_double(dt),None,None)
            print(f"solution displacement {np.linalg.norm(s)} ----- residual norm : {res_norm}")

    @timeit
    def implicit_euler(self, dt:float, check_residual_norm:float=-1, reduced_gravity:int=0, stab_param:float=0.) :
        """Solves the fluid equations.

        Args:
            dt: Computation time step
            check_residual_norm: If > 0, checks the residual norm after the system resolution
            reduced_graviy: If True simulations are run with a reduced gravity (not to use in two fluids simulations)
            stab_param: If zero pspg/supg/lsic stabilisation is computed otherwise the value is used as a coefficient for a pressure laplacian stabilisation term
        """
        self._lib.fluid_problem_set_reduced_gravity(self._fp,c_int(reduced_gravity))
        self._lib.fluid_problem_set_stab_param(self._fp,c_double(stab_param))
        self._lib.fluid_problem_apply_boundary_conditions(self._fp)
        solution_old = self.solution().copy()
        self._lib.fluid_problem_reset_boundary_force(self._fp)
        self._lib.fluid_problem_compute_stab_parameters(self._fp,c_double(dt))
        idx = self.global_map().reshape(self.n_elements(),-1)

        if self.sys is None :
            constraints = self.constraint_index.copy()
            if self.mean_pressure is not None:
                constraint = self.pressure_index()
                constraints.append(constraint)
            self.sys = self.linear_system_package(self.elements(), idx, self.n_fields(), self.solver_options, constraints, (self.velocity_index(), self.pressure_index()))
        sys = self.sys
        localv = np.ndarray([self.local_size()*self.n_elements()])
        localm = np.ndarray([self.local_size()**2*self.n_elements()])
        self._lib.fluid_problem_assemble_system(self._fp,_np2c(solution_old),c_double(dt),_np2c(localv),_np2c(localm))

        constraint_value = self.constraint_value.copy()
        if self.mean_pressure is not None:
            constraint_value.append((self.node_volume().reshape([-1]), -self.mean_pressure*np.sum(self.node_volume())))
        
        rhs = sys.local_to_global(localv, localm, self.solution(), constraint_value)
        self.solution()[:] -= sys.solve(rhs)
        if check_residual_norm > 0 :
            self._lib.fluid_problem_reset_boundary_force(self._fp)
            self._lib.fluid_problem_assemble_system(self._fp,_np2c(solution_old),c_double(dt),_np2c(localv),_np2c(localm))
            rhs = sys.local_to_global(localv,localm,self.solution().reshape([-1]),constraint_value)
            norm = np.linalg.norm(rhs)
            print("norm",norm)
            if norm > check_residual_norm :
                raise ValueError("wrong derivative or linear system precision")
        self._lib.fluid_problem_node_force_volume(self._fp,_np2c(solution_old),c_double(dt),None,None)

    def compute_cfl(self):
        """Computes the CFL number divided by the time step

        """
        sol = self.solution()
        nv = np.linalg.norm(sol[self.velocity_index()], axis=1)
        nvmax = np.max(nv)
        h = self._get_matrix("element_size",self.n_elements(),1)
        cfl = nvmax / (0.1*h)
        return np.max(cfl)

    def advance_concentration(self,dt:float):
        """Solves the advection equation for the concentration using the current velocity field.

        Args:
            dt: Computation time step
        """
        if self._n_fluids == 2 :
            cfl = self.compute_cfl()
            nsub = int(cfl*dt+1)
            if (nsub != 1) :
                print("sub-iterating advection for cfl : %i sub-iterations"%nsub)
            for i in range(nsub) :
                self._lib.fluid_problem_advance_concentration(self._fp,c_double(dt/nsub))

    def set_particles(self, delassus:np.ndarray, volume:np.ndarray, position:np.ndarray, velocity:np.ndarray, contact:np.ndarray):
        """Set location of the grains in the mesh and compute the porosity in each cell.

        Args:
            delassus: List of particles delassus operators
            volume: List of particles volume
            position: List of particles centre positions
            velocity: List of particles velocity
            contact: List of particles contact resultant forces
        """
        self.n_particles = delassus.shape[0]
        self._lib.fluid_problem_set_particles(self._fp,c_int(delassus.shape[0]),_np2c(delassus),_np2c(volume),_np2c(position), _np2c(velocity),_np2c(contact))

    def move_particles(self, position:np.ndarray, velocity:np.ndarray, contact:np.ndarray):
        """Set location of the grains in the mesh and compute the porosity in each cell.

        Args:
            position: List of particles centre positions
            velocity: List of particles velocity
            contact: List of particles contact resultant forces
        """
        self._lib.fluid_problem_move_particles(self._fp,c_int(velocity.shape[0]),_np2c(position),_np2c(velocity),_np2c(contact))

    def _get_matrix(self, f_name, nrow, ncol,typec=c_double) :
        f = getattr(self._lib,"fluid_problem_"+f_name)
        f.restype = POINTER(typec)
        return np.ctypeslib.as_array(f(self._fp),shape=(nrow,ncol))
        
    def mesh_velocity(self) -> np.ndarray:
        """Give access to the mesh velocity value at the mesh nodes.

        Returns:
            np.ndarray: mesh velocities at the mesh nodes
        """
        return self._get_matrix("mesh_velocity", self.get_mapping("P1").max()+1, self._dim)

    def solution(self)-> np.ndarray:
        """Gives access to the fluid field value at each degree of freedom as a flat array.

        Returns:
            np.ndarray: fluid solution
        """

        isize = c_int()
        solp = POINTER(c_double)()
        self._lib.fluid_problem_solution(self._fp, byref(isize), byref(solp))
        return np.ctypeslib.as_array(solp, shape=(isize.value,))

    def field_index(self, ifield:int)-> np.ndarray:
        """Gives access to all the index of a field into the solution vector.

        Args:
            ifield: field index (0,..,dimension-1) is a velocity, dimension gives the pressure.

        Returns:
            np.ndarray: index array.
        """
        isize = c_int()
        idxp = POINTER(c_int)()
        self._lib.fluid_problem_field_index(self._fp, c_int(ifield), byref(isize), byref(idxp))
        return np.ctypeslib.as_array(idxp, shape=(isize.value,))

    def velocity_index(self)-> np.ndarray:
        """Returns the index of the velocities into the solution vector as a bidimensionnal array.

        Returns:
            np.ndarray: velocities index array
        """
        return np.column_stack(list(self.field_index(i) for i in range(self._dim)))

    def pressure_index(self)-> np.ndarray:
        """Returns the index of the pressure field into the solution vector.

        Returns:
            np.ndarray: pressure index array
        """

        return self.field_index(self._dim)

    def boundary_force(self)-> np.ndarray:
        """Give access to force exerted by the fluid on the boundaries.
        
        Returns:
            np.ndarray: Forces exerted by the fluid on the boundaries. 
 
        """
        return self._get_matrix("boundary_force", self._lib.fluid_problem_mesh_n_boundaries(self._fp), self._dim)

    def coordinates(self)-> np.ndarray:
        """Gives access to the coordinate of the mesh nodes.

        Returns:
            np.ndarray: mesh nodal coordinates

        """
        return self._get_matrix("coordinates",self.n_nodes(), 3)

    def parent_nodes(self)-> np.ndarray:
        """Gives access to the parent nodes of each node.
        
        Returns:
            np.ndarray: The parent nodes mapping
        """
        return self._get_matrix("periodic_mapping", self.n_nodes(),1, typec=c_int32)

    def n_fluids(self)->int:
        """Returns the number of fluids (only one or two).

        Returns:
            int: Number of fluids 
        """
        return self._n_fluids

    def elements(self)-> np.ndarray:
        """Gives read-only access to the elements of the mesh.

        Returns:
            np.ndarray: mesh elements 
        """
        return self._get_matrix("elements", self.n_elements(), self._dim+1,c_int)

    def n_elements(self)->int:
        """Returns the number of mesh elements.

        Returns:
            int: number of elements 
        """
        self._lib.fluid_problem_n_elements.restype = c_int
        return self._lib.fluid_problem_n_elements(self._fp)

    def n_fields(self)->int:
        """Returns the number of fluid fields.

        Returns:
            int: number of fields 
        """
        self._lib.fluid_problem_n_fields.restype = c_int
        return self._lib.fluid_problem_n_fields(self._fp)

    def n_nodes(self)->int:
        """Returns the number of mesh nodes.

        Returns:
            int: number of nodes 
        """
        self._lib.fluid_problem_n_nodes.restype = c_int
        return self._lib.fluid_problem_n_nodes(self._fp)

    def porosity(self)-> np.ndarray:
        """Returns the porosity at independant nodes.

        Returns:
            np.ndarray: volume fluid fraction 
        """
        return self._get_matrix("porosity", self.get_mapping("P1").max()+1, 1)

    def set_concentration_cg(self,concentration:np.ndarray):
        """Sets the concentration at nodes.
        Args:
            concentration: concentration field
        """
        concentration = concentration.reshape((self.n_nodes(),1))
        self._lib.fluid_problem_set_concentration_cg(self._fp,_np2c(concentration))

    def concentration_dg(self)-> np.ndarray:
        """Returns the concentration at discontinuous nodes.

        Returns:
            np.ndarray: concentration field
        """
        return self._get_matrix("concentration_dg", self.n_elements(), self._dim+1)

    def concentration_dg_grad(self)-> np.ndarray:
        """Returns the gradient of the concentration field at discontinuous nodes.

        Returns:
            np.ndarray: concentration gradient
        """
        return self._get_matrix("concentration_dg_grad", self.get_mapping("P1").max()+1, self._dim)

    def curvature(self)-> np.ndarray:
        """Returns the curvature at each element.

        Returns:
            np.ndarray: curvature
        """

        return self._get_matrix("curvature", self.n_elements(), 1)

    def old_porosity(self)-> np.ndarray:
        """Returns the old porosity.
        
        Returns:
            np.ndarray: old porosity
        """
        return self._get_matrix("old_porosity", self.get_mapping("P1").max()+1, 1)

    def volume_flux(self, bnd_tag)->float:
        """Computes the integral of the (outgoing) normal velocity through boundary with tag bnd_tag.
        
        Returns:
            float : volume flux
        """
        self._lib.fluid_problem_volume_flux.restype = c_double
        return self._lib.fluid_problem_volume_flux(self._fp,bnd_tag.encode())

    def particle_element_id(self)-> np.ndarray:
        """Returns the id of the mesh cell in which particles are located.
        
        Returns:
            np.ndarray : particle element id
        """
        f = getattr(self._lib,"fluid_problem_particle_element_id")
        f.restype = c_void_p
        fs = getattr(self._lib,"fluid_problem_n_particles")
        fs.restype = c_int
        ptr = f(self._fp)
        size = fs(self._fp)
        buf = (size*c_int).from_address(ptr)
        return np.ctypeslib.as_array(buf)

    def particle_uvw(self)-> np.ndarray:
        """Returns the coordinates of the particles inside their element
        Returns:
            np.ndarray : parametric coordinates of the particles
        """
        return self._get_matrix("particle_uvw",self.n_particles,self._dim)

    def particle_position(self)-> np.ndarray:
        """Gives access to the particles position.
        Returns:
            np.ndarray : particles position
        """
        return self._get_matrix("particle_position", self.n_particles, self._dim)

    def particle_velocity(self)-> np.ndarray:
        """Gives access to the particles velocity.
        Returns:
            np.ndarray : particles velocity
        """
        return self._get_matrix("particle_velocity", self.n_particles, self._dim)

    def particle_volume(self)-> np.ndarray:
        """Gives access to the particles volume.
        Returns:
            np.ndarray : particles volume
        """
        return self._get_matrix("particle_volume", self.n_particles, 1)

    def bulk_force(self)-> np.ndarray :
        """Gives access to the volume force at fluid nodes.
        Returns:
            np.ndarray : Bulk force
        """
        return self._get_matrix("bulk_force", self.get_mapping("P1").max()+1, self._dim)

    def node_volume(self)-> np.ndarray:
        """Returns the volume associated with each node.
        Returns:
            np.ndarray : node volume
        """
        return self._get_matrix("node_volume",self.get_mapping("P1").max()+1,1)

    def local_size(self)->int:
        """Returns the number of degree of freedom by element.

        Returns:
            int: number of degree of freedom by element
        """
        self._lib.fluid_problem_local_size.restype = c_int
        return self._lib.fluid_problem_local_size(self._fp)

    def global_map(self)-> np.ndarray:
        """Gives access to the map of all the degrees of freedom.

        Returns:
            np.ndarray: global mapping
        """
        return self._get_matrix("global_map", self.n_elements(), self.local_size(), c_int)

    def _n_physicals(self):
        f = self._lib.fluid_problem_private_n_physical
        f.restype = c_int
        return f(self._fp)

    def _physical(self,ibnd):
        f = self._lib.fluid_problem_private_physical
        phys_dim = c_int()
        phys_id = c_int()
        phys_n_nodes = c_int()
        phys_nodes = POINTER(c_int)()
        phys_name = c_char_p()
        phys_n_boundaries = c_int()
        phys_boundaries = POINTER(c_int)()
        f(self._fp,c_int(ibnd),byref(phys_name),byref(phys_dim),byref(phys_id),byref(phys_n_nodes),byref(phys_nodes),byref(phys_n_boundaries),byref(phys_boundaries))
        nodes = np.ctypeslib.as_array(phys_nodes,shape=(phys_n_nodes.value,)) if phys_nodes else np.ndarray([0],np.int32)
        bnd = np.ctypeslib.as_array(phys_boundaries,shape=(phys_n_boundaries.value,2)) if phys_boundaries else np.ndarray([2,0],np.int32)
        return phys_name.value,phys_dim.value,phys_id.value,nodes,bnd

    def dimension(self)->int:
        """Returns the dimension of the problem

        Returns:
            int: dimension
        """
        return self._dim

    def velocity(self)-> np.ndarray:
        """ Reads the velocity solution. 
        
        Returns:
            np.ndarray: velocity
        """
        return self.solution()[self.velocity_index()]

    def pressure(self)-> np.ndarray:
        """ Reads the pressure solution. 

        Returns:
            np.ndarray: pressure
        """
        return self.solution()[self.pressure_index()].reshape(-1,1)

    def get_mapping(self, etype:str)-> np.ndarray:
        """Get mapping associated to an element.

        Args:
            etype: element type ("P1", "P1DG", "P2", "P2DG")

        Returns:
            np.ndarray: mapping associated to the element type.
        """
        ptr = c.POINTER(c.c_int)()
        s = c.c_int32()
        self._lib.fluid_problem_get_mapping(self._fp, etype.encode(), c.byref(s), c.byref(ptr))
        return np.ctypeslib.as_array(ptr, shape=(s.value,)).reshape(self.elements().shape[0], -1)

    def u_solid(self)-> np.ndarray:
        """ Returns the solid velocity as a p1-continuous field.
        
        Returns:
            np.ndarray : solid velocity
        """
        us = np.empty((self.get_mapping("P1").max()+1,self.dimension()))
        self._lib.fluid_problem_u_solid(self._fp, _np2c(us))
        return us

    def _parametric_coordinates(self, ifield):
        f = getattr(self._lib,"fluid_problem_fe_element_xi")
        f.restype = POINTER(c_double)
        self._lib.fluid_problem_fe_element_local_size.restype = c_int
        local_size = self._lib.fluid_problem_fe_element_local_size(self._fp, c_int(ifield))
        xi = np.ctypeslib.as_array(f(self._fp, c_int(ifield)), shape=(local_size,self._dim))
        return xi

    def coordinates_fields(self)-> np.ndarray:
        """ Returns the coordinates of each degree of freedom of the solution.
        
        Returns:
            np.ndarray : fields coordinates
        """
        gmap = self.global_map()
        x = self.coordinates()[self.elements(),:self._dim]
        xi = [self._parametric_coordinates(ifield) for ifield in range(self.n_fields())]
        phi = np.vstack([np.stack([1-xif[:,0]-xif[:,1], xif[:,0], xif[:,1]],axis=1) for xif in xi]) if self._dim == 2 \
            else np.vstack([np.stack([1-xif[:,0]-xif[:,1]-xif[:,2], xif[:,0], xif[:,1], xif[:,2]],axis=1) for xif in xi])
        xf = np.zeros((self.solution().shape[0], self._dim))
        xf[gmap] = np.sum(phi[None,:,:,None]*x[:,None,:,:], axis=2)
        return xf

    def interpolate(self, solution:Union[np.ndarray, callable]=None, velocity:Union[np.ndarray, callable]=None, velocity_x:Union[np.ndarray, callable]=None, velocity_y:Union[np.ndarray, callable]=None, velocity_z:Union[np.ndarray, callable]=None, pressure:Union[np.ndarray, callable]=None):
        """Imposes the solution (or the field) to the prescribed value. 
        If a callback is given, the solution (or field) is estimated at its local position.
        The solution (or field) is strongly imposed (not weakly).

        Args:
            solution : imposed solution vector
            velocity  : imposed velocity vector.
            velocity_x  : imposed horizontal velocity component.
            velocity_y  : imposed horizontal velocity component.
            velocity_z  : imposed horizontal velocity component.
            pressure  : imposed pressure field.
        """
        if solution is not None and (velocity is not None or pressure is not None or velocity_x is not None or velocity_y is not None or velocity_z is not None):
            print("Error in interpolate : solution cannot be imposed with another field !")
            exit(0) 
        if velocity is not None and (velocity_x is not None or velocity_y is not None or velocity_z is not None):
            print("Error in interpolate : velocity vector and its component cannot be imposed during the same call !")
            exit(0) 

        x = self.coordinates_fields()
        ind_u = self.velocity_index()
        ind_p = self.pressure_index()
        xu = x[ind_u[:,0]]
        if pressure is not None:
            self.solution()[ind_p] = pressure(x[ind_p]) if callable(pressure) else pressure
        if velocity is not None:
            if callable(velocity):
                s = velocity(xu)
                for i in range(self._dim):
                    self.solution()[ind_u[:,i]] = s[i]
            else:
                for i,v in enumerate(velocity):
                    self.solution()[ind_u[:,i]] = v(xu) if callable(v) else v
        if velocity_x is not None:
            self.solution()[ind_u[:,0]] = velocity_x(xu) if callable(velocity_x) else velocity_x
        if velocity_y is not None:
            self.solution()[ind_u[:,1]] = velocity_y(xu) if callable(velocity_y) else velocity_y
        if self._dim > 2 and velocity_z is not None:
            self.solution()[ind_u[:,2]] = velocity_z(xu) if callable(velocity_z) else velocity_z
        if solution is not None:
            if callable(solution):
                su = solution(xu)
                sp = solution(x[ind_p])
                self.solution()[ind_p] = sp[-1]
                for i in range(self._dim):
                    self.solution()[ind_u[:,i]] = su[i]
            else:
                for i,s in enumerate(solution):
                    ind = self.field_index(i)
                    self.solution()[ind] = s(x[ind]) if callable(s) else s

    def solution_at_coordinates(self, x:np.ndarray) -> np.ndarray:
        """Returns the solution vector interpolated at the given coordinates.
        
        Args:
            x: coordinates
        Returns:
            np.ndarray : solution at given coordinates
        """
        s = np.zeros((x.shape[0], self.n_fields()))
        self._lib.fluid_problem_interpolate_solution(self._fp, c_int(x.shape[0]), _np2c(x), _np2c(s))
        return s

    def fields_gradient(self) -> np.ndarray:
        """Returns an continuous gradient estimation of each field on a P1 mesh.

        Returns:
            np.ndarray: Fields_gradient
        """
        ndofp1 = self.get_mapping("P1").max()+1
        grad = np.zeros((ndofp1, self.n_fields(), self._dim), dtype=np.float64)
        self._lib.fluid_problem_get_field_gradient(self._fp, _np2c(grad))
        return grad
