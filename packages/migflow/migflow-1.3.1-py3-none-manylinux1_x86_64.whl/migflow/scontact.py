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

from __future__ import division
from . import VTK
import timeit
import shutil
from math import isqrt
import os
import sys
from collections import defaultdict
import ctypes as c
import json
from ._tools import gmsh, _np2c
from . import abin 
from typing import Tuple, Union, List, Dict
import re

import numpy as np
assert(np.lib.NumpyVersion(np.__version__) >= "1.17.0")

dir_path = os.path.dirname(os.path.realpath(__file__))
lib2 = np.ctypeslib.load_library("libscontact2",dir_path)
lib3 = np.ctypeslib.load_library("libscontact3",dir_path)
is_64bits = sys.maxsize > 2**32

def _arrayc(addr, dtype, readonly=False):
    if addr == 0:
        a = np.ndarray(0, dtype)
    else:
        msize = c.c_size_t.from_address(addr-8).value
        a = np.frombuffer((msize*c.c_char).from_address(addr), dtype)
    if readonly:
        a.flags.writeable = False
    return a


class ParticleProblem :
    """Creates the numerical structure containing all the physical particles that appear in the problem"""
    def parse_type(self, tname):
        f = getattr(self._lib, f"{tname}_introspect")
        f.restype = c.c_char_p
        descr = "".join(f().decode().replace(" ", "").split())
        descr = descr[descr.find("{")+1:descr.rfind("}")]
        tdict = {"i32":np.int32, "f64":np.float64, "usize":np.uint64, "ContactType":np.int32,
                 "Coord":np.dtype((np.float64, self._dim)),
                 "Omega":np.dtype((np.float64,[1])) if self._dim == 2 else np.dtype((np.float64,3))
                 }
        ddict = {"DIMENSION":self._dim}
        result = []
        for field in descr.split(","):
            name, ty = field.split(":")
            dims = []
            while ty[0] =="[":
                p = ty.rfind(";")
                dim = ty[p+1:-1]
                dims = [ddict[dim] if dim in ddict else int(dim)]+dims
                ty = ty[1:p]
            result.append((name, tdict[ty], tuple(dims)))
        return np.dtype(result, align=True)

    def _array(self, name, readonly=False):
        bsize = c.c_size_t()
        csize = c.c_size_t()
        getattr(self._lib,f"ParticleProblem_{name}_get")(self._p, c.byref(bsize), c.byref(csize))
        dtype = self.types[name]
        if dtype == np.float64:
            msize= bsize.value*8
        else:
            msize = bsize.value*dtype.itemsize
        a = np.frombuffer((msize*c.c_char).from_address(csize.value), dtype)
        if readonly:
            a.flags.writeable = False
        return a

    def _array_set(self, name, v):
        bsize = c.c_size_t(v.size)
        getattr(self._lib,f"ParticleProblem_{name}_set")(self._p, bsize, _np2c(v, v.dtype))

    def _array_push(self, name, **args):
        p = np.zeros(1, self.types[name])
        for k, v in args.items():
            p[k] = v
        f = getattr(self._lib,f"ParticleProblem_{name}_push")
        f.restype = c.c_size_t
        return f(self._p, c.c_void_p(p.ctypes.data))
    
    def __init__(self, dim:int) :
        """Builds the particle problem structure.

        Args:
            dim: Dimension of the problem
        Raises:
            ValueError: If the dimension differs from 2 or 3
            NameError: If C builder cannot be found
        """
        
        self._dim = dim
        self.contact_detection_d = None
        if dim == 2 :
            self._lib = lib2
            self._coord_type = c.c_double*2
        elif dim == 3 :
            self._lib = lib3
            self._coord_type = c.c_double*3
        else :
            raise ValueError("Dimension should be 2 or 3.")
        self._lib.particle_problem_new.restype = c.c_void_p
        self.types = {
                "bodies":self.parse_type("Body"),
                "particles":self.parse_type("Particle"),
                "contacts":self.parse_type("Contact"),
                "segments":self.parse_type("Segment"),
                "periodic_entities":self.parse_type("PeriodicEntity"),
                "periodic_points":self.parse_type("PeriodicPoint"),
                "periodic_segments":self.parse_type("PeriodicSegment"),
                "mu": np.float64,
                "contact_forces": np.float64 }
        if self._dim == 3:
            self.types["triangles"] = self.parse_type("Triangle")
            self.types["periodic_triangles"] = self.parse_type("PeriodicTriangle")
        self._lib.particle_problem_new.restype = c.c_void_p
        self._p = c.c_void_p(self._lib.particle_problem_new())
        self._contacttypename = {"particle_particle":0, "particle_segment":1, "particle_triangle":2}
        self.material2id = {}
        self.tag2id = {}
        self.id2tag = []
        self.id2material = []

    def __del__(self):
        """Deletes the particle solver structure."""
        if(self._p is not None) :
            self._lib.particle_problem_free(self._p)

    def set_fixed_contact_geometry(self, flag:bool):
        """Sets the management of the contact geometry, either fixed (default) or changing each time the contact is solved. 

        Args:
            flag: True for fixed False for changing.
        """
        self._lib.particle_problem_set_fixed_contact_geometry(self._p, c.c_int(flag))

    def volume(self) -> np.ndarray:
        """Returns the volumes of the particles.
        Returns:
            np.ndarray : Array of the particle volumes
        """
        if self._dim == 2 :
            return np.pi * self._array("particles")["radius"].reshape(-1,1)**2
        else :
            return 4./3.*np.pi * self._array("particles")["radius"].reshape(-1,1)**3

    def r(self) -> np.ndarray:
        """Returns the raddi of the particles.
        Returns:
            np.ndarray : Array of the particle radii
        """
        return self._array("particles")["radius"].reshape(-1,1)
 
    def id(self) -> np.ndarray:
        """Returns the ids of the particles.
        Returns:
            np.ndarray : Array of the particle ids
        """
        return self._array("particles")["tag"].reshape(-1,1)

    def body_invert_mass(self) -> np.ndarray:
        """Returns the invert mases of the bodies.
        Returns:
            np.ndarray : Array of the body invert masses
        """
        return self._array("bodies")["imass"][:,None]

    def body_invert_inertia(self) -> np.ndarray:
        """Returns the invert inertias of the bodies.
        Returns:
            np.ndarray : Array of the body invert inertias
        """
        return self._array("bodies")["iinertia"][:,None]

    def body_position(self) -> np.ndarray:
        """Returns the positions of the bodies.
        Returns:
            np.ndarray : Array of the body positions
        """
        return self._array("bodies")["position"]

    def body_velocity(self) -> np.ndarray:
        """Returns the velocities of the bodies.
        Returns:
            np.ndarray : Array of the body velocities
        """
        return self._array("bodies")["velocity"]

    def body_omega(self) -> np.ndarray:
        """Returns the angular velocities of the bodies.
        Returns:
            np.ndarray : Array of the body angular velocities
        """ 
        return self._array("bodies")["omega"]

    def body_theta(self) -> np.ndarray:
        """Returns the array of the body angles.
        Returns:
            np.ndarray : Array of the body angles
        """
        return self._array("bodies")["theta"][:,None]


    def position(self) -> np.ndarray:
        """Returns the positions of the particles.
        Returns:
            np.ndarray : Array of the particle positions
        """
        ppos = np.zeros((self.n_particles(),self._dim))
        self._lib.particle_problem_get_particles_position(self._p, _np2c(ppos))
        ppos.flags.writeable = False
        return ppos

    def velocity(self) -> np.ndarray:
        """Returns the velocities of the particles.
        Returns:
            np.ndarray : Array of the particle velocities
        """
        pvel = np.zeros((self.n_particles(),self._dim))
        self._lib.particle_problem_get_particles_velocity(self._p, _np2c(pvel))
        pvel.flags.writeable = False
        return pvel

    def particle_body(self) -> np.ndarray:
        """Returns the bodies associated to each particle

        Returns:
            np.ndarray: body id
        """
        return self._array("particles", readonly=True)["body"]

    def delassus(self) -> np.ndarray:
        """Returns the delassus operators of the particles.
        Returns:
            np.ndarray : Array of the particle delassus operators
        """
        delassus = np.zeros((self.n_particles(),self._dim,self._dim))
        self._lib.particle_problem_get_delassus(self._p,_np2c(delassus))
        return delassus

    def contact_forces(self) -> np.ndarray:
        """Returns the contact forces on each particle.
        Returns:
            np.ndarray : Array of the particle contact forces
        """
        f = self._array("contact_forces").reshape(-1, self._dim)
        p = self._array("particles")
        if f.shape[0] != p.shape[0]:
            f = np.zeros((p.shape[0], self._dim))
        return f

    def save_state(self) :
        """Saves the current state of the particle problem.
        """
        self._saved_velocity = np.copy(self.body_velocity())
        self._saved_position = np.copy(self.body_position())
        self._saved_segments = np.copy(self.segments())
        if self.dim() == 3 :
            self._saved_triangles = np.copy(self.triangles())
        self._saved_omega = np.copy(self.body_omega())
        self._saved_theta = np.copy(self.body_theta())

    def restore_state(self) :
        """Restores the saved state of the particle problem.
        """
        self.body_velocity()[:] = self._saved_velocity
        self.body_position()[:] = self._saved_position
        self.body_omega()[:] = self._saved_omega
        self.body_theta()[:] = self._saved_theta
        self.segments()[:] = self._saved_segments
        if self.dim() == 3 :
            self.triangles()[:] = self._saved_triangles

    def material(self) -> np.ndarray:
        """Returns the materials of the particles.
        Returns:
            np.ndarray : Array of the particle materials
        """
        return self._array("particles")["material"].reshape(-1,1)

    def get_tag_id(self, tag:str="default") -> int:
        """Returns the number associated to a string tag.
        Args:
            tag : string tag.
        Returns:
            int : number associated to the string tag
        """
        if tag not in self.tag2id.keys():
            n = len(self.tag2id)
            self.tag2id[tag] = n
            self.id2tag.append(tag)
            return n
        return self.tag2id[tag]

    def get_material_id(self, material:str) -> int:
        """Returns the number associated to a string material.
        Args:
            material : string material.
        Returns:
            int : number associated to the string material
        """
        if material not in self.material2id:
            n = len(self.material2id)
            self.material2id[material] = n
            self._lib.particle_problem_allocate_material(self._p, c.c_int(n+1))
            self.id2material.append(material)
            return n
        return self.material2id[material]

    def n_particles(self) -> int:
        """Returns the number of particles.
        Returns:
            int : number of particles
        """
        return self._array("particles").shape[0]

    def n_bodies(self) -> int:
        """Returns the number of bodies.
        Returns:
            int : number of bodies
        """
        return self._array("bodies").shape[0]

    def mu(self) -> np.ndarray:
        """Returns the array of the friction coefficients between materials.
        Returns:
            np.ndarray : Array of the friction coefficients between materials.
        """
        mu = self._array("mu")
        n = isqrt(mu.size)
        return mu.reshape(n, n)

    def segments(self) -> np.ndarray:
        """Returns the array of boundary segments.
        Returns:
            np.ndarray : Array of boundary segments
        """
        return self._array("segments")

    def periodic_entity(self) -> np.ndarray:
        """Returns the array of periodic entities.
        Returns:
            np.ndarray : Array of periodic entities
        """
        return self._array("periodic_entities")

    def periodic_points(self) -> np.ndarray:
        """Returns the array of periodic points.
        Returns:
            np.ndarray : Array of periodic points
        """
        return self._array("periodic_points")

    def periodic_segments(self) -> np.ndarray:
        """Returns the array of periodic segments.
        """
        return self._array("periodic_segments")

    def periodic_triangles(self) -> np.ndarray:
        """Returns the array of periodic triangles.
        Returns:
            np.ndarray : Array of periodic segments
        """
        if self._dim == 2:
            return np.ndarray((0),self._periodicTriangletype)
        return self._array("periodic_triangles")

    def triangles(self) -> np.ndarray:
        """Returns the array of boundary triangles.
        Returns:
            np.ndarray : Array of boundary triangles
        """
        if self._dim == 2:
            return np.ndarray((0),self._triangletype)
        return self._array("triangles")

    def get_boundary_forces(self,tag:str="default") -> np.ndarray:
        """Returns the forces acting on a boundary because of the contacts in the global basis.
        Args:
            tag:  Name of the boundary
        Returns:
            np.ndarray : Array of forces on boundary named tag 
        """
        f = np.zeros(self.dim())
        itag = self.get_tag_id(tag)
        contacts = self.contacts()
        contacts_pp = contacts[contacts["contact_type"] == self._contacttypename["particle_particle"]]
        bnd_tag = self._array("particles")[contacts_pp["o"][:,0]]["tag"]
        f += np.sum(contacts_pp[bnd_tag==itag]["reaction"], axis=0)
        bnd_tag = self._array("particles")[contacts_pp["o"][:,1]]["tag"]
        f -= np.sum(contacts_pp[bnd_tag==itag]["reaction"], axis=0)

        contacts_seg = contacts[contacts["contact_type"]==self._contacttypename["particle_segment"]]
        bnd_tag = self.segments()[contacts_seg["o"][:,0]]["tag"]
        f += np.sum(contacts_seg[bnd_tag==itag]["reaction"], axis=0)
        if self._dim == 3:
            contacts_tri = contacts[contacts["contact_type"]==self._contacttypename["particle_triangle"]]
            bnd_tag = self.triangles()[contacts_tri["o"][:,0]]["tag"]
            f += np.sum(contacts_tri[bnd_tag==itag]["reaction"], axis=0)
        return -f


    def set_boundary_velocity(self, tag:str, v:np.ndarray) :
        """Sets the velocity of a boundary to a given value.
        Args:
            tag:  Name of the boundary
            v:  Velocity vector to be given to the boundary
        """
        itag = self.get_tag_id(tag)
        bodies = self.segments()[self.segments()["tag"]==itag]["body"] 
        if self._dim == 3:
          bodies = np.concatenate((bodies,self.triangles()[self.triangles()["tag"]==itag]["body"] ) )
        self.body_velocity()[bodies,:] = v

    def set_friction_coefficient(self, mu:float, mat0:str="default",mat1:str="default") :
        """ Sets the friction coefficient between two materials.

        Args:
            mu:  Value of the friction coefficient
            mat0:  First material
            mat1:  Second material
        """
        imat0 = self.get_material_id(mat0)
        imat1 = self.get_material_id(mat1)
        n = len(self.material2id)
        a = self._array("mu")
        a[imat0*n+imat1] = a[imat1*n+imat0] = mu

    def iterate(self, dt:float, forces:np.ndarray, body_forces:np.ndarray=None,tol:float=1e-8,force_motion:int=0) :
        """Computes iteratively the set of velocities that respect the non-interpenetration constrain.
           Returns 1 if the computation converged, 0 otherwise.
        
        Args:
            dt:  Numerical time step
            forces:  List of vectors containing the forces applied on the particles
            body_forces : List of forces applied to the bodies
            tol:  Optional argument defining the interpenetration tolerance to stop the NLGS iterations of the NSCD
            force_motion:  Optional argument allowing to move the grains if convergence has not been reached when set to 1
        """ 
        body_forces = body_forces if body_forces is not None else np.zeros_like(self.body_velocity())
        if body_forces.shape[0] != self.n_bodies() or body_forces.shape[1] != self.dim():
            raise ValueError("Body forces do not have the proper shape")
        alert = self.contact_detection_d if self.contact_detection_d is not None else np.max(self.r()) if self.r().size != 0 else tol
        self._lib.particle_problem_iterate.restype = c.c_int
        return self._lib.particle_problem_iterate(
                self._p, c.c_double(alert), c.c_double(dt), c.c_double(tol),
                c.c_int(-1), c.c_int(force_motion), _np2c(forces), _np2c(body_forces))

    def contacts(self) -> np.ndarray:
        """Gives the contacts between the bodies.
        Returns:
            np.ndarray : Array of contact forces between the particles
        """
        return self._array("contacts")

    def computeStressTensor(self, nodes:np.ndarray, radius:float) -> np.ndarray:
        """Computes the stress tensor of the granular material
        Args:
            nodes:  Array of nodes at which to compute the stress tensor
            r:  Radius within which the contact forces will be averaged 
        Returns:
            np.ndarray : Array of stresses on the nodes of the grid
        """
        n_nodes = len(nodes[:,0])
        s = np.ndarray((n_nodes,self._dim**2))
        self._lib.particle_problem_compute_stress_tensor(
                self._p,_np2c(nodes[:,:self._dim]),
                c.c_double(radius), c.c_int(n_nodes), _np2c(s))
        return s

    def write_mig(self, output_dir:str, t:float, extra_fields:Dict[str, np.ndarray]={}) :
        """Writes output files for post-visualization.
        Args:
            output_dir:  Directory in which to write the file (expected to end in ".mig")
            t:  Time at which the simulation is 
            extra_fields : extra field as a dictionnary {name : values}
        """      
        fields_list = []
        efields_list = []
        abin.append(output_dir+"/solid/time", np.array([t],np.float64))
        for aname in self.types.keys():
            data = self._array(aname)
            path = aname.replace("_","/")
            if data.dtype == np.float64:
                fields_list.append(path)
                abin.write_iter(output_dir+"/solid/"+path, data)
            else:
                for fname in data.dtype.names:
                    if len(fname) == 0: continue
                    fields_list.append(path+"/"+fname)
                    abin.write_iter(output_dir+"/solid/"+path+"/"+fname, data[fname])
        for key, field in zip(extra_fields.keys(), extra_fields.values()):
            field = field.reshape(-1,1) if field.ndim==1 else field
            efields_list.append(key)
            abin.write_iter(output_dir+"/solid/particles/"+key, np.asarray(field, np.float64))

        with open(output_dir+"/solid.migs", "w", encoding="utf-8") as f:
            data = {"fields":fields_list,
                    "extra_fields":efields_list,
                    "version":"1.0",
                    "tags":self.id2tag,
                    "materials":self.id2material,
                    "contact_types":self._contacttypename}
            f.write(json.dumps(data, indent=2, sort_keys=True))


    def read_mig(self, odir:str, t:float):
        """Reads output files.
        Args:
            odir:  Directory in which to read the file
            t:  Time at which to read the file
        """
        dirname = odir + '/solid/'
        time = abin.openread(dirname + "time")[:]
        itime = np.searchsorted(time, t)
        with open (odir+"/solid.migs") as finfo:
            info = json.load(finfo)
        self.id2tag = info['tags']
        self.tag2id = dict((name, i) for i, name in enumerate(self.id2tag))
        self.id2material = info['materials']
        self.material2id = dict((name,i) for i,name in enumerate(self.id2material))
        for aname, dtype in self.types.items():
            path = aname.replace("_","/")+"/"
            if not os.path.isdir(dirname+path): continue
            for i, fname in enumerate(dtype.names):
                d = abin.get_iter(dirname+path+fname, itime)
                if i == 0:
                    o = np.empty(d.shape[0], dtype)
                o[fname][:] = d
            self._array_set(aname, o)

    def add_boundary_periodic_entity(self, dim:int, transform:np.ndarray):
        """Adds a periodic entity.

        Args:
            dim:  dimension of the entity
            transform:  array of the transformation to applied to the periodic entity
        """
        return self._array_push("periodic_entities", dimension=dim, transformation=transform)

    def add_boundary_periodic_point(self, x:np.ndarray, tag:int) :
        """Adds a boundary periodic point.

        Args:
            x:  array of the coordinates of the point
            tag:  entity tag
        """
        return self._array_push("periodic_points", entity=tag, position=x);

    def add_boundary_periodic_segment(self, x0:np.ndarray, x1:np.ndarray, tag:int) :
        """Adds a boundary periodic segment.

        Args:
            x0:  array of the coordinates of the first endpoint
            x1:  array of the coordinates of the second endpoint
            tag:  entity tag
        """
        return self._array_push("periodic_segments", entity=tag, position=[x0,x1]);

    def add_boundary_periodic_triangle(self, x0:np.ndarray, x1:np.ndarray, x2:np.ndarray, tag:int):
        """Adds a boundary periodic triangle.

        Args:
            x0:  array of the coordinates of the first summit 
            x1:  array of the coordinates of the second summit 
            x2:  array of the coordinates of the third summit 
            tag:  tag of the periodic entity 
        """
        if self._dim != 3 :
            raise NameError("Triangle boundaries only available in 3D")
        return self._array_push("periodic_triangles", entity=tag, position=[x0, x1, x2]);

    def add_boundary_segment(self, x0:np.ndarray, x1:np.ndarray, tag:str, material:str="default") :
        """Adds a boundary segment.

        Args:
            x0:  array of the coordinates of the first endpoint
            x1:  array of the coordinates of the second endpoint
            tag:  segment tag
            material:  segment material
        """
        imat = self.get_material_id(material)
        itag = self.get_tag_id(tag)
        xm = (np.asarray(x0)+np.asarray(x1))/2
        body = self.add_body(xm, 0, 0)
        return self._array_push("segments", relative_position=[x0-xm, x1-xm], tag=itag, body=body, material=imat)

    def add_boundary_triangle(self, x0:np.ndarray, x1:np.ndarray, x2:np.ndarray, tag:str, material:str="default") :
        """Adds a boundary triangle.

        Args:
            x0:  array of the coordinates of the first summit 
            x1:  array of the coordinates of the second summit 
            x2:  array of the coordinates of the third summit 
            tag:  triangle tag
            material:  triangle material
        """
        if self._dim != 3 :
            raise NameError("Triangle boundaries only available in 3D")
        imat = self.get_material_id(material)
        itag = self.get_tag_id(tag)
        xm = (np.asarray(x0)+np.asarray(x1)+np.asarray(x2))/3
        body = self.add_body(xm, 0, 0)
        return self._array_push("triangles", relative_position=[x0-xm, x1-xm, x2-xm], tag=itag, body=body, material=imat)

    def add_body(self, x:np.ndarray, invertM:float, invertI:float)->int:
        """Adds a body in the particle problem. --- Only in 2D

        Args:
            x:  array of the position of the body
            InvertM:  inverse mass of the body
            InvertI:  inverse inertia of the body

        Returns:
            int : body id
        """
        return self._array_push("bodies", position=x, imass=invertM, iinertia=invertI)

    def add_entities(self, xbody:np.ndarray, invertM:float=0.0, invertI:float=0.0, 
    particles_coordinates:np.ndarray=None, particles_radius:Union[np.ndarray, float]=None, particles_materials:Union[str, List[str]]="default", 
    segments_coordinates:np.ndarray=None, segments_tags:Union[str, List[str]]=None, segments_materials:Union[str, List[str]]="default",
    triangles_coordinates:np.ndarray=None, triangles_tags:str=None, triangles_materials:Union[str, List[str]]="default", is_relative_position=True) -> int:
        """Adds entities (either particles, segments or triangles) to a body described by its position, inverse of mass and inverse of inertia.

        Args:
            xbody (np.ndarray): position of the body
            invertM (float, optional): inverse mass of the body. Defaults to 0.
            invertI (float, optional): inverse inertia of the body. Defaults to 0.
            particles_coordinates (np.ndarray, optional): position of the particles. Defaults to None.
            particles_radius (Union[np.ndarray, float], optional): array of the particles radii. Defaults to None.
            particles_materials (Union[str, List[str]], optional): array of the particles material. Defaults to "default".
            segments_coordinates (np.ndarray, optional): array of the segments coordinates as n_segments x 2 x dimension. Defaults to None.
            segments_tags (Union[str, List[str]], optional): array of the segments tags. Defaults to None.
            segments_materials (Union[str, List[str]], optional): array of the segments materials. Defaults to "default".
            triangles_coordinates (np.ndarray, optional): array of the segments coordinates as n_segments x 3 x dimension. Defaults to None.
            triangles_tags (str, optional): array of the triangles tags. Defaults to None.
            triangles_materials (Union[str, List[str]], optional):array of the triangles materials. Defaults to "default".
            is_relative_position (bool, optional): flag if the given position is the relative position towards the body or the absolute position. Defaults to True.

        Returns:
            int: body id
        """
        imatp = imats = imatt = None
        itags = itagt = None
        n_particles = n_segments = n_triangles = 0
        xbody = np.asarray(xbody, dtype=np.float64)
        if particles_coordinates is not None:
            n_particles = particles_coordinates.shape[0]
            particles_radius = np.asarray(particles_radius, np.float64).reshape(-1)
            if particles_radius.shape[0] == 1:
                particles_radius = np.full(n_particles, particles_radius, np.float64)
            if not is_relative_position:
                particles_coordinates[:,:] -= xbody[None,:]
            if isinstance(particles_materials, list):
                if len(particles_materials) != n_particles:
                    raise(ValueError, "Wrong shape in particles_materials !")
                imatp = [self.get_material_id(m) for m in particles_materials]
            imatp = [self.get_material_id(particles_materials)]*n_particles
        if segments_coordinates is not None:
            n_segments = segments_coordinates.shape[0]
            if not is_relative_position:
                segments_coordinates[:,:,:] -= xbody[None,None,:]
            if isinstance(segments_materials, list):
                if len(segments_materials) != n_segments:
                    raise(ValueError, "Wrong shape in segments_materials !")
                imats = [self.get_material_id(m) for m in segments_materials]
            else:
                imats = [self.get_material_id(segments_materials)]*n_segments
            if segments_tags is None:
                segments_tags = "none"
            if isinstance(segments_tags, list):
                if len(segments_tags) != n_segments:
                    raise(ValueError, "Wrong shape in segments_materials !")
                itags = [self.get_tag_id(t) for t in segments_tags]
            else:
                itags = [self.get_tag_id(segments_tags)]*n_segments

        if triangles_coordinates is not None:
            n_triangles = triangles_coordinates.shape[0]
            if not is_relative_position:
                triangles_coordinates[:,:,:] -= xbody[None,None,:]
            if isinstance(triangles_materials, list):
                if len(triangles_materials) != n_segments:
                    raise(ValueError, "Wrong shape in triangles_materials !")
                imatt = [self.get_material_id(m) for m in triangles_materials]
            else:
                imatt = [self.get_material_id(triangles_materials)]*n_triangles
            if triangles_tags is None:
                triangles_tags = "none"
            if isinstance(triangles_tags, list):
                if len(triangles_tags) != n_triangles:
                    raise(ValueError, "Wrong shape in triangles_materials !")
                itagt = [self.get_tag_id(t) for t in triangles_tags]
            else:
                itagt = [self.get_tag_id(triangles_tags)]*n_triangles

        ibody = self.add_body(xbody, invertM, invertI)
        for x, r, mat in zip(particles_coordinates, particles_radius, imatp):
            self._array_push("particles", radius=r, body=ibody, relative_position=x, material=imat)
        for x, tag, mat in zip(segments_coordinates, itags, imats):
            self._array_push("segments", relative_position=x, body=ibody, tag=tag, material=mat);
        for x, tag, mat in zip(triangles_coordinates, itagt, imatt):
            self._array_push("triangles", relative_position=x, body=ibody, tag=tag, material=mat);
        return ibody

    def add_particle_body(self, positions:np.ndarray,radii:np.ndarray,masses:np.ndarray,material:str="default",forced:bool=False) -> int:
        """Adds a body in the particle problem with a list of constituting particles --- Only in 2D

        Args:
            positions:  positions of the particles constituting the body
            radii:  radii of the particles
            masses:  masses of the particles
            material:  material of the particles
            forced:  Flag indicating whether the body is forced or not

        Returns:
            int : body id
        """
        if self._dim == 3:
          raise NameError("Nonspherical bodies are only supported in 2D")
        if positions.shape[0] != radii.shape[0] or positions.shape[0]!=masses.shape[0] or masses.shape[0]!=radii.shape[0]: 
          raise NameError("Wrong lengths of particle data vectors.")

        x = np.sum(positions*masses.reshape((-1,1)),axis=0)/np.sum(masses)
        I = np.sum(masses*radii**2/2 + np.sum((positions-x)**2,axis=1)*masses)
        invertI = 0 if forced else 1/I
        invertM = 0 if forced else 1/np.sum(masses)
        idd = self.add_body(x, invertM, invertI)
        if not isinstance(material,(list, np.ndarray)):
          material = [material for i in range(positions.shape[0])]
        for i in range(positions.shape[0]):
          self.add_particle_to_body(positions[i,:]-x,radii[i],idd, material[i])
        return idd

    def add_particle_to_body(self, x:np.ndarray, r:float, body:int, material:str="default"):
        """Adds a particle to a body.

        Args:
            x:  array of the particle positon with respect to the body's centre of mass
            r:  Particle radius
            body:  number of the body to which the particle will be added
            material:  Particle material
        """
        imat = self.get_material_id(material)
        if material.lower() == "ignore":
            imat = -1
        return self._array_push("particles", radius=r, body=body, relative_position=x, material=imat)

    def add_segment_to_body(self, x0:np.ndarray, x1:np.ndarray, body:int, tag:str, material:str="default"):
        """Adds a segment to a body.

        Args:
            x0 (np.ndarray): array of the coordinates of the first endpoint
            x1 (np.ndarray): array of the coordinates of the second endpoint
            body (int): body id
            tag (str): boundary id associated to the segment
            material (str): Segment material
        """
        imat = self.get_material_id(material)
        if material.lower() == "ignore":
            imat = -1
        itag = self.get_tag_id(tag)
        if body >= self.n_bodies():
            raise ValueError(f"Body {body} does not exist, no segment can be linked to it !")
        return self._array_push("segments", relative_position=[x0, x1], tag=itag, body=body, material=imat)

    def add_particles(self, x:np.ndarray, r:np.ndarray, m:np.ndarray, tag:str="default",forced:bool=False, inverse_inertia:np.ndarray=None)->np.ndarray:
        """Adds particles in the particle container.

        Args:
            x:  array of tuple to set the centre particle position
            r:  array of particle radius
            m:  array of particle mass
            tag:  particle material
            
        Returns:
            np.ndarray : id of the added bodies
        """
        bodies = np.asarray([], int)
        for xi, ri, mi in zip(xi, ri, mi):
            if (not forced) and inverse_inertia is None:
                inverse_inertia = 2/(mi*ri**2) if self._dim == 2 else 5/(2*mi*ri**2)
            body = self.add_body(x, 0 if forced else 1/mi, 0 if forced else inverse_inertia)
            self.add_particle_to_body([0]*self._dim, ri, body, tag)
            bodies = np.append(bodies, body)
        return bodies


    def add_particle(self, x:np.ndarray, r:float, m:float, tag:str="default",forced:bool=False, inverse_inertia:float=None)->int:
        """Adds a particle in the particle container.

        Args:
            x:  array of the particle position
            r:  particle radius
            m:  particle mass
            tag:  particle material

        Returns:
            int : body id
        """
        if (not forced) and inverse_inertia is None:
            inverse_inertia = 2/(m*r**2) if self._dim == 2 else 5/(2*m*r**2)
        body = self.add_body(x, 0 if forced else 1/m, 0 if forced else inverse_inertia)
        self.add_particle_to_body([0]*self._dim, r, body, tag)
        return body
    
    def set_use_queue(self, use_queue:int=1):
      """Enables the use of the queue if 1 and disables it if 0.
      """
      self._lib.particle_problem_set_use_queue(self._p, c.c_int(use_queue))
      
    def set_compute_contact_forces(self, compute_contact_forces:int=1):
      """Enables the computation of the contact forces on each particle if 1 and disables it if 0.
      """
      self._lib.particle_problem_set_compute_contact_forces(self._p, c.c_int(compute_contact_forces))

    def _save_contacts(self):
      """Saves the contacts from the current time step.
      """
      self._saved_contacts = np.copy(self.contacts())

    def _restore_contacts(self):
      """Restores the saved contacts from the previous time step.
      """
      self._array_set("contacts", self.saved_contacts)

    def remove_bodies_flag(self,flag:np.ndarray) :
      """Removes particles based on given flag.
      Args:
          flag:  flag with the same size as the number of bodies, with 0 for bodies to be removed and 1 for bodies to be kept
      """
      if flag.shape != (self.n_bodies(),) :
          raise NameError("size of flag array should be the number of particles")
      self._lib.particle_problem_remove_bodies(self._p, _np2c(flag,np.int32))

    def load_msh_boundaries(self, filename:str, tags:str=None, shift:np.ndarray=None,material:str="default") :
        """Loads the numerical domain and set the physical boundaries the particles cannot go through.
        
        Args:
            filename:  name of the msh file. If None the current gmsh model is loaded without the need to a msh file.
            tags:  tags of physical boundary defined in the msh file
            shift:  optional argument to shift the numerical domain
            material:  material of the boundary
        """
        if shift is None :
            shift = [0]*self._dim
        shift = np.array(shift)
        if filename is not None:
            if not os.path.isfile(filename):
              print("Error : no such file as " + filename)
              exit(1)
            gmsh.model.add("tmp")
            gmsh.open(filename)
        gmsh.model.mesh.renumber_nodes()
        addv = set()
        adds = set()
        periodic_entities = dict()
        ntag, x, _ = gmsh.model.mesh.get_nodes()
        x = x.reshape([-1,3])[:,:self._dim]
        x = x[np.argsort(ntag)]
        bndbody = self._array_push("bodies")

        def get_entity_name(edim, etag) :
            for tag in  gmsh.model.get_physical_groups_for_entity(edim, etag):
                name = gmsh.model.get_physical_name(edim,tag)
                if name is not None :
                    return name
            return "none"

        def add_disk(t, stag) :
            if t in addv : return
            self.add_particle(x[t]+shift, 0, bndbody, material, forced=True)
            addv.add(t)

        def add_segment(t0, t1, stag) :
            key = (min(t0,t1),max(t0,t1))
            if key in adds : return
            adds.add(key)
            self.add_boundary_segment(x[t0]+shift, x[t1]+shift,
                                      stag, material)

        def add_triangle(t0, t1, t2, stag):
            self.add_boundary_triangle(x[t0]+shift, x[t1]+shift,x[t2]+shift,
                                        stag, material)

        for dim, tag in gmsh.model.get_entities(self._dim-1) :
            ptag, cnodes, pnodes, _ = gmsh.model.mesh.get_periodic_nodes(dim, tag)
            if ptag == tag or len(cnodes) == 0: continue
            trans = x[(pnodes-1)[0]] - x[(cnodes-1)[0]]
            tag_id = self.add_boundary_periodic_entity(dim,trans)
            ptag_id = self.add_boundary_periodic_entity(dim,-trans)
            periodic_entities[(dim, tag)] = trans
            periodic_entities[(dim, ptag)] = -trans
            pmap = dict((int(i)-1,int(j)-1) for i,j in zip (cnodes,pnodes))
            for etype, _, enodes in zip(*gmsh.model.mesh.get_elements(dim,tag)):
                if dim == 1 :
                    if etype != 1 : continue
                    for l in (enodes-1).reshape([-1,2]):
                        self.add_boundary_periodic_segment(
                                x[l[0]]+shift, x[l[1]]+shift, tag_id)
                        self.add_boundary_periodic_segment(
                                x[pmap[l[0]]]+shift, x[pmap[l[1]]]+shift, ptag_id)
                else :
                    if etype != 2 : continue
                    for l in (enodes-1).reshape([-1,3]):
                        self.add_boundary_periodic_triangle(
                                x[l[0]]+shift, x[l[1]]+shift,
                                x[l[2]]+shift, tag_id)
                        self.add_boundary_periodic_triangle(
                                x[pmap[l[0]]]+shift, x[pmap[l[1]]]+shift,
                                x[pmap[l[2]]]+shift, ptag_id)

        sub_periodic = defaultdict(lambda : [])
        for periodic in periodic_entities:
            for bnd in gmsh.model.get_boundary([periodic], oriented=False):
                sub_periodic[bnd] += [periodic]
            if self._dim == 3 :
                for bnd in gmsh.model.get_boundary([periodic], recursive=True, oriented=False):
                    sub_periodic[bnd] += [periodic]
        for bnd, parentlist in sub_periodic.items():
            if len(parentlist) + bnd[0] != self._dim : continue
            trans = np.sum([periodic_entities[e] for e in parentlist], axis=0)
            periodic_entities[bnd] = trans
            bnd_id = self.add_boundary_periodic_entity(bnd[0], trans)
            _, xbnd, _ = gmsh.model.mesh.get_nodes(bnd[0], bnd[1], True, False)
            xbnd = xbnd.reshape(-1,3)[:,:self._dim]
            if bnd[0] == 1 :
                self.add_boundary_periodic_segment(xbnd[0], xbnd[1], bnd_id)
            elif bnd[0] == 0:
                self.add_boundary_periodic_point(xbnd[0], bnd_id)

        for dim, tag in gmsh.model.get_entities(0) :
            stag = get_entity_name(dim,tag)
            if (dim,tag) in periodic_entities : continue
            if not (tags is None or stag in tags) : continue
            for etype, _, enodes in zip(*gmsh.model.mesh.get_elements(dim,tag)):
                if etype != 15 : continue
                for t in enodes-1 :
                    add_disk(t, stag)
        for dim, tag in gmsh.model.get_entities(1) :
            stag = get_entity_name(dim,tag)
            if (dim,tag) in periodic_entities : continue
            if not (tags is None or stag in tags) : continue
            for etype, _, enodes in zip(*gmsh.model.mesh.get_elements(dim,tag)):
                if etype != 1 : continue
                for t in enodes-1 :
                    add_disk(t, stag)
                for l in (enodes-1).reshape([-1,2]):
                    add_segment(l[0], l[1], stag)

        if self._dim == 3 :
            for dim, tag in gmsh.model.get_entities(2) :
                stag = get_entity_name(dim,tag)
                if (dim,tag) in periodic_entities : continue
                if not (tags is None or stag in tags) : continue
                for etype, _, enodes in zip(*gmsh.model.mesh.get_elements(dim,tag)):
                    if etype != 2 : continue
                    for t in enodes-1 :
                        add_disk(t, stag)
                    for v0,v1,v2 in (enodes-1).reshape([-1,3]):
                        add_segment(v0, v1, stag)
                        add_segment(v1, v2, stag)
                        add_segment(v2, v0, stag)
                        add_triangle(v0, v1, v2, stag)
        if filename is not None:
            gmsh.model.remove()
            
    def dim(self) -> int:
        """Returns the dimension of the particle problem.
        Returns:
            int : Dimension of the problem
        """
        return self._dim
    
    def bounding_box(self) -> Tuple[np.ndarray,np.ndarray]:
        """Returns the bounding box of the particle problem.
        Returns:
            Tuple[np.ndarray, np.ndarray]: position of the lower left corner, position of the upper right corner
        """
        bbmin = np.empty(3)
        bbmax = np.empty(3)
        self._lib.particle_problem_bounding_box(self._p, _np2c(bbmin), _np2c(bbmax))
        return bbmin, bbmax
