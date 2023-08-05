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

from paraview.util.vtkAlgorithm import (
        VTKPythonAlgorithmBase,
        smdomain,
        smhint,
        smproperty,
        smproxy
)

from vtkmodules.numpy_interface import dataset_adapter as dsa
from vtkmodules.vtkCommonDataModel import vtkUnstructuredGrid
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


@smproxy.reader(
        name = "migflow fluid reader",
        extensions = ["migf"],
        file_description = "migflow output directory",
        support_reload=False,
)
# @smproperty.xml(xmlstr='''<OutputPort name="Fluid" index="0"/>''')
class FluidReader(VTKPythonAlgorithmBase):
    def __init__(self):
        VTKPythonAlgorithmBase.__init__(self, nInputPorts=0, nOutputPorts=1, outputType="vtkUnstructuredGrid")
        self._filename = None
        self._arrayselection_fluid = vtkDataArraySelection()
        self._arrayselection_fluid.AddObserver("ModifiedEvent", createModifiedCallback(self))

    @smproperty.stringvector(name="FileName")
    @smdomain.filelist()
    @smhint.filechooser(
            extensions=["migf"], file_description="migflow fluid output"
    )
    def SetFileName(self, filename):
        if self._filename != filename:
            self._filename = filename
            if filename is not None  and filename != "None":
                info = json.load(open(self._filename))
                self._fields = info["fields"]
                for f in self._fields.keys():
                    self._arrayselection_fluid.AddArray(f)
                self.dirname = self._filename.removesuffix(".migf")+"/"
                self._time_steps = abin.openread(self.dirname+"time")[:]
            self.Modified()

    @smproperty.dataarrayselection(name="Fluid Fields")
    def GetDataArraySelectionFluid(self):
        return self._arrayselection_fluid

    @smproperty.doublevector(name="TimestepValues", information_only="1", si_class="vtkSITimeStepsProperty")
    def GetTimestepValues(self):
        return self._time_steps

    def RequestInformation(self, request, inInfo, outInfoVec):
        executive = self.GetExecutive()
        outInfo = outInfoVec.GetInformationObject(0)
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
        executive = self.GetExecutive()
        data_time = outInfoVec.GetInformationObject(0).Get(executive.UPDATE_TIME_STEP())
        itime = np.searchsorted(self._time_steps, data_time)
        dirn = self.dirname

        topo = abin.get_iter(dirn+"mesh/topology", itime)
        if topo is None:
            return 0
        dimension = topo.shape[1]-1
        n_elements = topo.shape[0]
        nodes = abin.get_iter(dirn+"mesh/geometry", itime)
        output = dsa.WrapDataObject(vtkUnstructuredGrid.GetData(outInfoVec))

        def get_data_at_discrete(data, mapping):
            datam = data[mapping]
            if self._discretization == "P1":
                if datam.shape[1] == dimension+1:
                    return datam.reshape(-1, data.shape[1])
                else:
                    return datam[:,:dimension+1].reshape(-1, data.shape[1])
            elif self._discretization == "P2":
                if datam.shape[1] == 2*(2*dimension-1):
                    if dimension == 3:
                        datam[:,[8,9]] = datam[:,[9,8]]
                    return datam.reshape(-1, data.shape[1])
                else:
                    datam = np.insert(datam, [dimension+1]*3*(dimension-1), 0, axis=1)
                    cl = np.c_[np.arange(3), np.arange(1,4)%3]
                    if dimension==3 : cl = np.r_[cl, np.c_[np.arange(3), np.full(3,3)]]
                    ndata = datam[:,:dimension+1]
                    datam[:,dimension+1:] = np.mean(ndata[:,cl], axis=2)
                    return datam.reshape(-1, data.shape[1])

        if self._discretization == "P1":
            cell_types = np.full([n_elements], 5 if dimension == 2 else 10, dtype=np.ubyte)
            cell_offsets = np.arange(0, (n_elements+1)*(dimension+1), dimension+1, dtype=int)
            els = np.empty((n_elements,dimension+2))
            els[:,0] = dimension+1
            els[:,1:] = np.arange(n_elements*(dimension+1)).reshape(-1, dimension+1)
            dnodes = nodes[topo].reshape(-1,3)
        if self._discretization == "P2":
            cell_types = np.full([n_elements], 22 if dimension == 2 else 24, dtype=np.ubyte)
            cell_offsets = np.arange(0, (n_elements+1)*(dimension+1), dimension+1, dtype=int)
            els = np.empty((n_elements,4*dimension-1))
            els[:,0] = 4*dimension-2
            els[:,1:] = np.arange(n_elements*(4*dimension-2)).reshape(-1, 4*dimension-2)
            dnodes = get_data_at_discrete(nodes, topo).reshape(-1,3)
        output.SetPoints(dnodes)
        output.SetCells(cell_types, cell_offsets, els)
        for field,element in self._fields.items():
            if self._arrayselection_fluid.ArrayIsEnabled(field) :
                element = abin.metaread(dirn + "/data/"+field)["element"]
                fieldd = abin.get_iter(dirn + "/data/"+field, itime)
                mapping = abin.get_iter(dirn+"/mappings/"+element, itime)
                datam = get_data_at_discrete(fieldd, mapping)
                if datam.shape[1] == 2:
                    datam = np.insert(datam,2,0,axis=1)
                output.PointData.append(datam, field)
        output.GetInformation().Set(output.DATA_TIME_STEP(), data_time)
        return 1

    @smproperty.stringvector(name="DiscretizationChoices",number_of_elements=4, information_only="1")
    def GetDiscretizationChoices(self):
        return ["P1","P2"]

    @smproperty.stringvector(name="Discretization", number_of_elements="1", port_index=0, index=0, port=0)
    @smdomain.xml(\
        """<StringListDomain name="list">
                <RequiredProperties>
                    <Property name="DiscretizationChoices" function="DiscretizationChoices"/>
                </RequiredProperties>
            </StringListDomain>
        """)
    def SetDiscretization(self, value):
        self._discretization = value
        self.Modified()

