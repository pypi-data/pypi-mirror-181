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

import zlib
import struct
import numpy as np
from base64 import b64decode,b64encode
from xml.etree import ElementTree as ET
import os.path
import os

def _write_array(f,anc,attr) :
    a = np.ascontiguousarray(anc)
    tname = {
            np.dtype('<i4'):b"Int32",
            np.dtype('<i8'):b"Int64",
            np.dtype('<f4'):b"Float32",
            np.dtype('<f8'):b"Float64",
            np.dtype('uint8'):b"UInt8",
            np.dtype('uint64'):b"UInt64"
            }[a.dtype]
    f.write(b'<DataArray %s type="%s" format="binary">\n'%(attr,tname))
    data = zlib.compress(a,2)
    f.write(b64encode(struct.pack("iiii",1,a.nbytes,0,len(data))) + b64encode(data))
    f.write(b"\n</DataArray>\n")

def _read_array(a) :
    raw = a.text.strip()
    typename = a.attrib["type"]
    dtype = {"UInt8":np.uint8,"Float64":np.float64,"Float32":np.float32,"Int64":np.int64,"Int32":np.int32,"UInt64":np.uint64}[typename]
    _,n,_,s = struct.unpack("iiii",b64decode(raw[:24]))
    data = zlib.decompress(b64decode(raw[24:24-(-s//3)*4]))
    nc,nt = -1,-1
    if "NumberOfComponents" in a.attrib :
        nc = int(a.attrib["NumberOfComponents"])
    if "NumberOfTuples" in a.attrib :
        nt = int(a.attrib["NumberOfTuples"])
    v = np.frombuffer(data,dtype)
    if nc != -1 or nt != -1 :
        v = v.reshape(nt,nc)
    return v

def _write_index(idxname,filename,i,t,reset_index) :
    if reset_index is None : reset_index = (i==0 or not os.path.isfile(idxname))
    with open(idxname,"wb" if reset_index else "rb+") as f :
        if reset_index :
            f.write(b'<?xml version="1.0"?>\n')
            f.write(b'<VTKFile type="Collection" version="0.1" byte_order="LittleEndian">\n')
            f.write(b'<Collection>\n')
        else:
            f.seek(-25,os.SEEK_END)
        f.write(b'<DataSet timestep="%.16g" group="" part="0" file="%s"/>\n'%(t,filename.encode()))
        f.write(b'</Collection>\n')
        f.write(b'</VTKFile>\n')
        f.close()

def write(basename,i,t,elements,x,data=None,field_data=None,cell_data=None,reset_index=None,vtktype="vtu") :
    """Write VTK UnstructuredMesh (vtu) or PolyData (vtp) files.
    The arrays are written in base64-encoded gzipped binary format.

    Keyword arguments:
    basename -- file path without the extension and the output number 
                e.g. "dir/file" becomes "dir/file_00012.vtp" and a collection vtk file "dir/file.pvd" will be created
    i -- output number (will be appended to the filename and used as index in the collection)
    t -- output time
    elements -- list of elements. It can be None, otherwise it should be a tupple (types,connectivity,offsets)
                where:
                types -- is a vector of int with the type of each element 
                    3:line,4:polyline,5:triangle,7:polygon,9:quad,10:tetra,12:hexahedron,...
                    see https://www.vtk.org/VTK/img/file-formats.pdf for a complete list
                connectivity  -- vector of int containing the indices of all elements nodes. Indices starts at 0.
                offsets -- vector of int with the position of the *END* of the list of each element nodes inside the
                    connectivity vector
    x -- two-dimensionnal array of float with the nodes coordinates, [[x0,y0,z0],[x1,y1,z1],...]].
         it should have 3 columns, even for 2-dimensional meshes
    node_data -- vector of pairs [(name0,data0),(name1,data1),...] with the name (as a string) and the fields attached
                to the nodes. The field data should be two-dimensional arrays even if they have only one column.
    cell_data -- like node_data, for the fields attached to the cells
    field_data -- like node_data for the fields attached neither to cells or nodes.
    reset_index -- boolean flag determining if the collection ".pvd" file index will be overwritten or appended.
                if not specified, the .pvd is overwritten if i == 0.
    vtktype -- "vtu" for UnstructuredMesh or "vtp" for PolyData. (The only difference seems to be that PolyData cannot
                have 3-dimensional elements.)
    """

    filename = "%s_%05d.%s"%(basename,i,vtktype)
    if not os.path.exists(os.path.dirname(filename)):
        os.makedirs(os.path.dirname(filename))
    with open(filename,"wb") as f :
        f.write(b'<?xml version="1.0"?>\n')
        vtkdescr = b"UnstructuredGrid" if vtktype=="vtu" else b"PolyData"
        f.write(b'<VTKFile type="%s" format="0.1" compressor="vtkZLibDataCompressor">\n' % vtkdescr)
        f.write(b'<%s>\n'%vtkdescr)
        nel = elements[0].shape[0] if elements is not None else 0
        npt = x.shape[0]
        f.write(b'<Piece NumberOfPoints="%i" NumberOfCells="%i">\n'%(npt,nel))
        f.write(b'<Points>\n')
        _write_array(f,x,b'NumberOfComponents="3"')
        f.write(b'</Points>\n')
        if elements is not None:
            (types,connectivity,offsets) = elements
            f.write(b'<Cells>\n')
            _write_array(f,connectivity,b'Name="connectivity"')
            _write_array(f,offsets,b'Name="offsets"')
            _write_array(f,types,b'Name="types"')
            f.write(b'</Cells>\n')
        if data is not None :
            f.write(b'<PointData>\n')
            for name,v in data :
                _write_array(f,v,b'Name="%s" NumberOfComponents="%i"' % (name.encode("utf8"),v.shape[-1]))
            f.write(b'</PointData>\n')
        if cell_data is not None :
            f.write(b'<CellData>\n')
            for name,v in cell_data :
                _write_array(f,v,b'Name="%s" NumberOfComponents="%i"' % (name.encode("utf8"),v.shape[-1]))
            f.write(b'</CellData>\n')
        f.write(b'</Piece>\n')
        if field_data is not None :
            f.write(b'<FieldData>\n');
            for name,v in field_data :
                _write_array(f,v,b'Name="%s" NumberOfTuples="%i" NumberOfComponents="%i"' % (name,v.shape[0],v.shape[1]))
            f.write(b'</FieldData>\n');
        f.write(b'</%s>\n' % vtkdescr)
        f.write(b'</VTKFile>\n')
        f.close()
    _write_index(basename+".pvd",os.path.basename(filename),i,t,reset_index)

def read(fname) :
    """Read VTK UnstructuredMesh (vtu) or PolyData (vtp) files written by the write function
    all arrays are returned as numpy array

    Keyword arguments :
    fname -- complete file path

    Return (points,cells,node_data,cell_data,field_data) :
    points -- nodes coordinates
    cells -- dictionary with three entries : "connectivity", "offsets" and "types"
            see the "write" function for a description of those arrays
    node_data,cell_data,field_data -- dictionaries whose keys are the name of the node,cell and field data.
    """

    with open(fname,"rb") as f : 
        root = ET.parse(f).getroot()
        ftype = root.attrib["type"]
        grid = root.find(ftype)
        piece = grid.find("Piece")
        x = _read_array(piece.find("Points/DataArray"))
        cells = piece.find("Cells")
        fd = grid.find("FieldData")
        cd = piece.find("CellData")
        pd = piece.find("PointData")
        c  = dict((f.attrib["Name"],_read_array(f)) for f in cells) if cells else None
        fdata = dict((f.attrib["Name"],_read_array(f)) for f in fd) if fd else None
        cdata = dict((f.attrib["Name"],_read_array(f)) for f in cd) if cd else None
        pdata = dict((f.attrib["Name"],_read_array(f)) for f in pd) if pd else None
    return x,c,pdata,cdata,fdata

def read_index(fname) :
    with open(fname,"rb") as f : 
        dss = ET.parse(f).getroot().find("Collection").findall("DataSet")
        return list([(ds.get("file"),int(ds.get("file")[:-4].split("_")[-1]),float(ds.get("timestep"))) for ds in dss])

def write_multipart(basename,parts,i,t,reset_index=None):
    """Write VTK MultiBlockDataSet (vtm) files.

    Keyword arguments:
    basename -- file path without the extension and the output number 
                e.g. "dir/file" becomes "dir/file_00012.vtm" and a collection vtk file "dir/file.pvd" will be created
    i -- output number (will be appended to the filename and used as index in the collection)
    t -- output time
    parts -- list of data file paths
    reset_index -- boolean flag determining if the collection ".pvd" file index will be overwritten or appended.
                if not specified, the .pvd is overwritten if i == 0.
    """
    filename = basename+"_%05d.vtm"%i
    if not os.path.exists(os.path.dirname(filename)):
        os.makedirs(os.path.dirname(filename))
    with open(filename,"wb") as f :
        f.write(b'<?xml version="1.0"?>\n')
        f.write(b'<VTKFile type="vtkMultiBlockDataSet" version="1.0" byte_order="LittleEndian">\n');
        f.write(b'<vtkMultiBlockDataSet>\n');
        for ip,n in enumerate(parts):
            f.write(b'<DataSet index="%i" file="%s"/>\n'%(ip,n.encode()));
        f.write(b'</vtkMultiBlockDataSet>\n');
        f.write(b'</VTKFile>\n');
        _write_index(basename+".pvd",os.path.basename(filename),i,t,reset_index)


def string_array_encode(a) :
    joined = b"".join(a)
    fmt = b"i%ii%is"%(len(a),len(joined))
    r = struct.pack(fmt,len(a),*(len(i) for i in a),joined)
    return np.array(list((i for i in r)),dtype="u1").reshape([-1,1])

def string_array_decode(e) :
    n = struct.unpack("i",e[:4])[0]
    l = struct.unpack("%ii"%n,e[4:4+4*n])
    return struct.unpack("".join("%is"%i for i in l), e[4+n*4:])


