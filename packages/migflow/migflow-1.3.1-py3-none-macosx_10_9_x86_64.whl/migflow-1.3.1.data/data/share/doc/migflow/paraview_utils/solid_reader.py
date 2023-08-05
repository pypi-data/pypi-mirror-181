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
import json
import os
import sys
sys.path.append(os.path.dirname(__file__))
from mfabin import Abin as abin
import paraview.simple

from paraview.util.vtkAlgorithm import (
        VTKPythonAlgorithmBase,
        smdomain,
        smhint,
        smproperty,
        smproxy
)

from vtkmodules.numpy_interface import dataset_adapter as dsa
from vtkmodules.vtkCommonDataModel import vtkPolyData, vtkUnstructuredGrid
from vtkmodules.vtkCommonCore import vtkDataArraySelection

paraview_plugin_version = "0.1"

def createModifiedCallback(obj):
    import weakref
    weakref_o = weakref.ref(obj)
    obj = None
    def _markmodified(*args, **kwargs):
        o = weakref_o()
        if o is not None:
            o.Modified()
    return _markmodified

def absolute_coord(position_bodies, theta_bodies, bodies, relative_position):
    if relative_position.shape[0] == 0:
        return np.zeros_like(relative_position)
    xb = position_bodies[bodies,None,:]
    ct = np.cos(theta_bodies[bodies])[:,None]
    st = np.sin(theta_bodies[bodies])[:,None]
    dim = relative_position.shape[-1]
    xo = np.empty_like(relative_position)
    xo[:,:,0] = xb[:,:,0]+relative_position[:,:,0]*ct-relative_position[:,:,1]*st
    xo[:,:,1] = xb[:,:,1]+relative_position[:,:,0]*st+relative_position[:,:,1]*ct
    if dim == 3:
        xo[:,:,2] = xb[:,:,2] + relative_position[:,:,2]
    return xo

@smproxy.reader(
        name = "migflow solid reader",
        extensions = ["migs"],
        file_description = "migflow solid output index",
        support_reload=False,
)
@smproperty.xml(xmlstr='''<OutputPort name="Particles" index="0"/>''')
@smproperty.xml(xmlstr='''<OutputPort name="Boundaries" index="1"/>''')
@smproperty.xml(xmlstr='''<OutputPort name="Periodic Boundaries" index="2"/>''')
@smproperty.xml(xmlstr='''<OutputPort name="Contacts" index="3"/>''')
class SolidReader(VTKPythonAlgorithmBase):
    def __init__(self):
        VTKPythonAlgorithmBase.__init__(self, nInputPorts=0, nOutputPorts=4, outputType=['vtkUnstructuredGrid', 'vtkPolyData'])
        self._filename = None
        self._arrayselection_solid = vtkDataArraySelection()
        self._computes_contacts = 0
        self._arrayselection_solid.AddObserver("ModifiedEvent", createModifiedCallback(self))

    def FillOutputPortInformation(self, port, info):
        from vtkmodules.vtkCommonDataModel import vtkDataObject
        if port == 0:
            info.Set(vtkDataObject.DATA_TYPE_NAME(), "vtkPolyData")
        else:
            info.Set(vtkDataObject.DATA_TYPE_NAME(), "vtkUnstructuredGrid")
        return 1

    def GetGlobalIDAsString(self):
        pass

    @smproperty.stringvector(name="FileName")
    @smdomain.filelist()
    @smhint.filechooser(
            extensions=["migs"], file_description="migflow solid output"
    )
    def SetFileName(self, filename):
        if self._filename != filename:
            self._filename = filename
            if filename is not None  and filename != "None":
                info = json.load(open(self._filename))
                self._efields = info["extra_fields"]
                for f in self._efields:
                    self._arrayselection_solid.AddArray(f)
                self._arrayselection_solid.AddArray("body")
                self._arrayselection_solid.AddArray("tag")
                self._arrayselection_solid.AddArray("inertia")
                self._arrayselection_solid.AddArray("mass")
                self._arrayselection_solid.AddArray("material")
                self._arrayselection_solid.AddArray("omega")
                self._arrayselection_solid.AddArray("velocity")
                self._arrayselection_solid.AddArray("radius")
                self.dirname = self._filename.removesuffix(".migs")+"/"
                self._time_steps = abin.openread(self.dirname+"time")[:]
            self.Modified()


    # @smproperty.intvector(name="Computes contacts", number_of_elements=1, default_values=0, BooleanDomain="bool")
    @smproperty.xml(xmlstr= """
                        <IntVectorProperty name="Computes Contacts"
                            command = "SetComputesContacts"
                            number_of_elements="1" 
                            default_values="0">
                        <BooleanDomain name="bool"/>
                    </IntVectorProperty>""")
    def SetComputesContacts(self, c):
        self._computes_contacts = c
        self.Modified()


    @smproperty.intvector(name="contact number of faces", group="contacts", default_values=4)
    def SetThetaSubdivision(self, nf):
        self._nf = nf
        self.Modified()

    @smproperty.doublevector(name="contact radius factor", group="contacts", default_values=5e-4)
    def SetRadius(self, rf):
        self._rf = rf
        self.Modified()

    @smproperty.xml(xmlstr= """<Property name="Set Default" panel_widget="command_button" command="set_default">
                    <Documentation>Set default representation.</Documentation>
                </Property>""")
    def set_default(self, *args):
        view = paraview.simple.GetActiveView()
        source = paraview.simple.GetActiveSource()

        source.Port = 0
        r_particles = paraview.simple.GetRepresentation(source, view)
        r_particles.SetRepresentationType("Point Gaussian")
        r_particles.SetScaleArray = ['POINTS', 'radius'] 
        r_particles.ScaleByArray = 1
        r_particles.UseScaleFunction = 0
        r_particles.GaussianRadius = 1.
        if self._dimension == 2:
            r_particles.Position = [0.0, 0.0, 0.5]

        source.Port= 1
        r_boundaries = paraview.simple.GetRepresentation(source, view)
        r_boundaries.SetRepresentationType("Wireframe")

        source.Port= 2
        r_periodic = paraview.simple.GetRepresentation(source, view)
        r_periodic.SetRepresentationType("Wireframe")

        source.Port= 3
        r_contacts = paraview.simple.GetRepresentation(source, view)
        r_contacts.SetRepresentationType("Surface")

        return 1

    @smproperty.dataarrayselection(name="Solid Fields")
    def GetDataArraySelectionSolid(self):
        return self._arrayselection_solid

    @smproperty.doublevector(name="TimestepValues", information_only="1", si_class="vtkSITimeStepsProperty")
    def GetTimestepValues(self):
        return self._time_steps

    def _load_time_step(self, data_time):
        itime = np.searchsorted(self._time_steps, data_time)
        # Bodies
        self._body_positions = abin.get_iter(self.dirname+"bodies/position", itime)
        self._dimension = self._body_positions.shape[-1] if self._body_positions is not None else 2
        self._body_theta = abin.get_iter(self.dirname+"bodies/theta", itime)
        self._body_omega = abin.get_iter(self.dirname+"bodies/omega", itime)
        self._body_velocity = abin.get_iter(self.dirname+"bodies/velocity", itime)
        self._body_imass = abin.get_iter(self.dirname+"bodies/imass", itime)
        self._body_iinertia = abin.get_iter(self.dirname+"bodies/iinertia", itime)
        # Particles
        self._particle_bodies = abin.get_iter(self.dirname+"particles/body", itime)
        self._particle_radius = abin.get_iter(self.dirname+"particles/radius", itime)
        self._particle_ids = abin.get_iter(self.dirname+"particles/tag", itime)
        self._particle_materials = abin.get_iter(self.dirname+"particles/material", itime)
        self._particle_rel = abin.get_iter(self.dirname+"particles/relative_position", itime)
        self._particle_position = self._body_positions[self._particle_bodies]
        self._particle_omega = self._body_omega[self._particle_bodies]
        self._particle_mass = np.divide(1, self._body_imass[self._particle_bodies], where=self._body_imass[self._particle_bodies]!=0)
        self._particle_inertia = np.divide(1, self._body_iinertia[self._particle_bodies], where=self._body_iinertia[self._particle_bodies]!=0)
        self._particle_absolute_position = absolute_coord(self._body_positions, self._body_theta, self._particle_bodies, self._particle_rel.reshape(-1,1,self._dimension))
        self._particle_absolute_position = self._particle_absolute_position.reshape(-1, self._dimension)
        res = np.zeros_like(self._particle_absolute_position)
        if self._dimension == 2:
            res[:,0] = -self._particle_omega[:,0]*(self._particle_absolute_position[:,1]-self._body_positions[self._particle_bodies,1])
            res[:,1] =  self._particle_omega[:,0]*(self._particle_absolute_position[:,0]-self._body_positions[self._particle_bodies,0])
        self._particle_velocity = self._body_velocity[self._particle_bodies] + res
        self._extra_fields = {}
        for f in self._efields:
            self._extra_fields[f] = abin.get_iter(self.dirname+"particles/"+f, itime)
        # Segments
        self._segment_bodies = abin.get_iter(self.dirname+"segments/body", itime)
        self._segment_rel = abin.get_iter(self.dirname+"segments/relative_position", itime)
        self._segment_x = absolute_coord(self._body_positions, self._body_theta, self._segment_bodies, self._segment_rel)
        self._segment_bodies = np.repeat(self._segment_bodies, 2)
        # Periodic Segments 
        self._psegment_x = abin.get_iter(self.dirname+"periodic/segments/position", itime)
        self._psegment_entity = abin.get_iter(self.dirname+"periodic/segments/entity", itime)
        self._psegment_entity = np.repeat(self._psegment_entity, 2)
        # Triangles && Periodic Triangles
        self._triangle_x = np.zeros((0,0,3))
        self._triangle_bodies = np.zeros((0,))
        self._ptriangle_x = np.zeros((0,0,3))
        self._ptriangle_entity = np.zeros(0)
        if self._dimension == 3:
            self._triangle_bodies = abin.get_iter(self.dirname+"triangles/body", itime)
            self._triangle_rel = abin.get_iter(self.dirname+"triangles/relative_position", itime)
            self._triangle_x = absolute_coord(self._body_positions, self._body_theta, self._triangle_bodies, self._triangle_rel)
            self._triangle_bodies = np.repeat(self._triangle_bodies, 3)
            self._ptriangle_x = abin.get_iter(self.dirname+"periodic/triangles/position", itime)
            self._ptriangle_entity = abin.get_iter(self.dirname+"periodic/triangles/entity", itime)
            self._ptriangle_entity = np.repeat(self._ptriangle_entity, 3)
        # insert dimension for Paraview vector
        if self._dimension == 2:
            self._particle_velocity = np.insert(self._particle_velocity, self._dimension, 0.0, axis=1)
            self._particle_position = np.insert(self._particle_position, self._dimension, 0.0, axis=1)
            self._particle_absolute_position = np.insert(self._particle_absolute_position, self._dimension, 0.0, axis=1)
            self._psegment_x = np.insert(self._psegment_x, self._dimension, 0.0, axis=2)
            self._segment_x = np.insert(self._segment_x, self._dimension, 0.0, axis=2)
        # Contacts
        if self._computes_contacts:
            self._contact_types = json.load(open(self._filename))["contact_types"]
            self._contacts_objects = abin.get_iter(self.dirname+"contacts/o", itime)
            self._contact_type = abin.get_iter(self.dirname+"contacts/contact_type", itime)
            self._contacts_reaction = abin.get_iter(self.dirname+"contacts/reaction", itime)
            self._contacts_basis = abin.get_iter(self.dirname+"contacts/basis", itime)
            self._contact_periodic = abin.get_iter(self.dirname+"contacts/periodic_entity", itime)
            self._periodic_transformations = abin.get_iter(self.dirname+"periodic/entities/transformation", itime)


    def _request_particles(self, output, outInfo):
        output.SetPoints(self._particle_absolute_position)
        output.PointData.append(self._particle_ids, "tag")
        output.PointData.append(self._particle_mass, "mass")
        output.PointData.append(self._particle_bodies, "body")
        output.PointData.append(self._particle_radius, "radius")
        output.PointData.append(self._particle_inertia, "inertia")
        output.PointData.append(self._particle_omega, "omega")
        output.PointData.append(self._particle_velocity, "velocity")
        output.PointData.append(self._particle_materials, "material")
        for f in self._efields:
            output.PointData.append(self._extra_fields[f], f)
        

    def _request_boundaries(self, output, outInfo):
        nsegment = self._segment_x.shape[0]
        ntriangle = self._triangle_x.shape[0]        
        points = np.r_[self._segment_x.reshape(-1,3), self._triangle_x.reshape(-1,3)]
        bodies = np.concatenate([self._segment_bodies, self._triangle_bodies])
        bodies = bodies[bodies!=None]
        segment_cells = np.arange(nsegment*2, dtype=int).reshape(-1,2)
        segment_cells = np.insert(segment_cells, 0, 2, axis=1)
        segment_types = np.full((nsegment), 3, np.ubyte)
        triangle_types = np.full((ntriangle), 5, np.ubyte)
        triangle_cells = 2*nsegment + np.arange(ntriangle*3, dtype=int).reshape(-1,3)
        triangle_cells = np.insert(triangle_cells, 0, 3, axis=1)
        cells = np.concatenate([segment_cells.reshape(-1), triangle_cells.reshape(-1)])
        types = np.concatenate([segment_types, triangle_types])
        locations = np.cumsum(np.repeat([2,3],[nsegment,ntriangle]),dtype=int)
        output.SetPoints(points)
        if np.size(bodies): output.PointData.append(bodies, "body")
        output.SetCells(types, locations, cells)

    def _request_periodic(self, output, outInfo):
        npsegment = self._psegment_x.shape[0]
        psegment_cells = np.arange(npsegment*2, dtype=int).reshape(-1,2)
        psegment_cells = np.insert(psegment_cells, 0, 2, axis=1)
        psegment_types = np.full((npsegment), 3, np.ubyte)
        nptriangle = self._ptriangle_x.shape[0]
        ptriangle_types = np.full((nptriangle), 5, np.ubyte)
        ptriangle_cells = np.arange(nptriangle*3, dtype=int).reshape(-1,3) + 2*npsegment
        ptriangle_cells = np.insert(ptriangle_cells, 0, 3, axis=1)
        points = np.r_[self._psegment_x.reshape(-1,3), self._ptriangle_x.reshape(-1,3)]
        entity = np.concatenate([self._psegment_entity, self._ptriangle_entity])
        entity = entity[entity!=None]
        cells = np.concatenate([psegment_cells.reshape(-1), ptriangle_cells.reshape(-1)])
        types = np.concatenate([psegment_types, ptriangle_types])
        locations = np.cumsum(np.repeat([2,3],[npsegment,nptriangle]),dtype=int)
        output.SetPoints(points)
        if np.size(entity) > 0: output.PointData.append(np.asarray(entity, float), "entity")
        output.SetCells(types, locations, cells)

    def _request_contacts(self, output, outInfo):
        points = np.zeros((0,2,3))
        if self._contacts_objects.size == 0:
            return 0
        for c_type in self._contact_types:
            id = np.where(self._contact_type == self._contact_types[c_type])[0]
            c_o = self._contacts_objects[id]
            is_periodic = self._contact_periodic[id] < self._periodic_transformations.shape[0]
            c_periodic_t = self._periodic_transformations[self._contact_periodic[id][is_periodic]]
            if c_type == "particle_particle":
                x = self._particle_absolute_position[c_o]
                x[is_periodic,1,:c_periodic_t.shape[1]] += c_periodic_t
                points = np.concatenate([points, x], axis=0)
            if c_type == "particle_segment":
                s = self._segment_x[c_o[:,0]]
                p = self._particle_absolute_position[c_o[:,1]]
                p[is_periodic,:c_periodic_t.shape[1]] += c_periodic_t
                t = s[:,1,:] - s[:,0,:]
                t /= ((t[:,0]**2+t[:,1]**2+t[:,2]**2)**0.5)[:,None]
                d = p - s[:,0,:]
                l = np.sum(d*t, axis=1)
                s = s[:,0,:] + l[:,None]*t
                s = np.stack([p, s], axis=1)
                points = np.concatenate([points, s], axis=0)
            if c_type == "particle_triangle" and self._dimension == 3:
                t = self._triangle_x[c_o[:,0]]
                p = self._particle_absolute_position[c_o[:,1]]
                p[is_periodic,:c_periodic_t.shape[1]] += c_periodic_t
                d0 = t[:,1] - t[:,0] 
                d1 = t[:,2] - t[:,0] 
                N = np.cross(d0,d1)
                N /= np.linalg.norm(N,axis=1)[:,None]
                dd = t[:,0] - p
                dist = np.einsum('ij,ij->i', N, dd)
                s = p + N*dist[:,None]
                s = np.stack([p, s], axis=1)
                points = np.concatenate([points, s], axis=0)
        t = points[:,0,:] - points[:,1,:]
        t /= np.linalg.norm(t,axis=1)[:,None]
        ez = np.where(np.abs(t[:,1,None])>np.abs(t[:,2,None]),np.array([[0,0,1]]),np.array([[0,1,0]]))
        n1 = np.cross(t,ez)
        n2 = np.cross(t,n1)
        alphas = np.arange(0,2*np.pi, 2*np.pi/self._nf)
        reaction_nt = np.einsum("cij, cj -> ci", self._contacts_basis, self._contacts_reaction)
        r = np.zeros_like(reaction_nt[:,0])
        tol = 1e-8*np.max(np.abs(reaction_nt[:,0]))
        nonzero = np.abs(reaction_nt[:,0]) > tol
        r[nonzero] = self._rf*reaction_nt[nonzero,0]**(1./2)
        n = points.shape[0]
        points = points[:,None,:,:] \
            +n1[:,None,None,:]*r[:,None,None,None]*np.sin(-alphas)[None,:,None,None] \
            +n2[:,None,None,:]*r[:,None,None,None]*np.cos(-alphas)[None,:,None,None]
        pattern = np.ndarray([self._nf,4], int)
        for i in range(self._nf) :
            j = (i+1)%self._nf
            pattern[i,:] = (i*2,i*2+1,j*2+1,j*2)
        types = np.full([n*self._nf],9,np.uint8)
        locations = np.arange(0,5*n*self._nf,5,np.uint32)
        cells = np.ndarray([n,self._nf,5],np.uint32)
        cells[:,:,0] = 4
        cells[:,:,1:] = np.arange(0,n*self._nf*2,self._nf*2,np.uint32)[:,None,None]+pattern[None,:,:]

        output.SetPoints(points.reshape(-1,3))
        if np.size(reaction_nt) > 0:
            output.PointData.append(np.repeat(reaction_nt[:,0],2*self._nf),"reaction_n")
            output.PointData.append(np.repeat(reaction_nt[:,1],2*self._nf),"reaction_t")
        output.SetCells(types, locations, cells.reshape([-1]))    

    def RequestInformation(self, request, inInfo, outInfoVec):
        executive = self.GetExecutive()
        for numInfo in range(outInfoVec.GetNumberOfInformationObjects()):
            outInfo = outInfoVec.GetInformationObject(numInfo)
            outInfo.Remove(executive.TIME_STEPS())
            outInfo.Remove(executive.TIME_RANGE())
            for t in self._time_steps:
                outInfo.Append(executive.TIME_STEPS(), t)
            outInfo.Append(executive.TIME_RANGE(), self._time_steps[0])
            outInfo.Append(executive.TIME_RANGE(), self._time_steps[-1])
        return 1

    def RequestData(self, request, inInfoVec, outInfoVec):
        if self._filename is None:
            return 1
        data_time = paraview.simple.GetActiveView().ViewTime
        #data_time = max(outInfoVec.GetInformationObject(i).Get(self.GetExecutive().UPDATE_TIME_STEP()) for i in range(nobj))
        self._load_time_step(data_time)
        output_particles = dsa.WrapDataObject(vtkPolyData.GetData(outInfoVec, 0))
        self._request_particles(output_particles, outInfoVec.GetInformationObject(0))
        output_particles.GetInformation().Set(output_particles.DATA_TIME_STEP(), data_time)

        output_boundaries = dsa.WrapDataObject(vtkUnstructuredGrid.GetData(outInfoVec, 1))
        self._request_boundaries(output_boundaries, outInfoVec.GetInformationObject(1))
        output_boundaries.GetInformation().Set(output_boundaries.DATA_TIME_STEP(), data_time)

        output_periodic_boundaries = dsa.WrapDataObject(vtkUnstructuredGrid.GetData(outInfoVec, 2))
        self._request_periodic(output_periodic_boundaries, outInfoVec.GetInformationObject(2))
        output_periodic_boundaries.GetInformation().Set(output_periodic_boundaries.DATA_TIME_STEP(), data_time)
        if self._computes_contacts == 1:
            output_contacts = dsa.WrapDataObject(vtkUnstructuredGrid.GetData(outInfoVec, 3))
            self._request_contacts(output_contacts, outInfoVec.GetInformationObject(3))
            output_contacts.GetInformation().Set(output_contacts.DATA_TIME_STEP(), data_time)
        return 1
