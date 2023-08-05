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

from pylmgc90 import chipy
import numpy as np
from . import VTK
import os
import math
import sys

class ParticleProblem(object):
  """
  A class definition holding data of lmgc90
  in a compatible form to use coupling with
  gmsh
  
  Attributs are :

  - number of objects (disks|sphere) 
  - volume of objects (disks|sphere)
  - reference map on objects to models (diskx2rbdy2 | spher2rbdy3)

  The methods are :
  
  - iterate()  : do one time iteration
  - position() : give back position of all spher
  - velocity() : give back velocity of all spher
  - externalForces() : update external forces on particles
  
  - getMeanRadius() : return the mean radius of particles
  - getVolume() : give back the volume of all spher 

  - writeHeader() : write header file for plot
  """

  def __init__(self,dim,period=0,xp=0,yp=0,restart=0) :
      """
      Initialize lmgc90
      """

      self._dim=dim
      self._fc = None
      
      chipy.Initialize()
      
      chipy.checkDirectories()
      
      chipy.SetDimension(dim)
      chipy.TimeEvolution_SetTimeStep(0.)      
      chipy.Integrator_InitTheta(0.5)

      chipy.utilities_logMes('READ BEHAVIOURS')
      chipy.ReadBehaviours()
      
      chipy.utilities_logMes('READ BODIES')
      chipy.ReadBodies()
      
      chipy.utilities_logMes('LOAD BEHAVIOURS')
      chipy.LoadBehaviours()
      
      chipy.utilities_logMes('READ INI DOF')
      chipy.ReadIniDof(restart)
      
      chipy.utilities_logMes('READ DRIVEN DOF')
      chipy.ReadDrivenDof()
      
      chipy.utilities_logMes('LOAD TACTORS')
      chipy.LoadTactors()
      
      chipy.utilities_logMes('READ INI Vloc Rloc')
      chipy.ReadIniVlocRloc(restart)

      if (period):
        chipy.SetPeriodicCondition(xperiod=xp,yperiod=yp)
      
      chipy.PRPRx_UseCpCundallDetection(30)

      chipy.OpenPostproFiles()
      chipy.OpenDisplayFiles(restart+1)
      
      #chipy.WriteDisplayFiles()

      chipy.ComputeMass()

      if dim == 2 :

        self._nbDisk   = chipy.DISKx_GetNbDISKx()
        self._d2bMap   = chipy.DISKx_GetPtrDISKx2RBDY2()
        self._p2bMap = chipy.POLYG_GetPtrPOLYG2RBDY2()
        self._position = np.zeros([self._nbDisk,3], 'd')
        self._velocity = np.zeros([self._nbDisk,3], 'd')
        self._externalF= np.zeros([self._nbDisk,3], 'd')
        self._volume   = np.zeros([self._nbDisk,1], 'd')
        self._mass   = np.zeros([self._nbDisk,1], 'd')
        self._r   = np.zeros([self._nbDisk,1], 'd')
        for i in range(self._nbDisk):
          self._r[i] = chipy.DISKx_GetContactorRadius(i+1)
          self._mass[i] = chipy.RBDY2_GetBodyMass(int(self._d2bMap[i,0]))
        self._volume = np.pi * self._r**2 
        self._tag2bnd = {}
        self._tag2id = {}
        for i in range(chipy.RBDY2_GetNbRBDY2()):
            for t in range(chipy.RBDY2_GetNbContactor(i+1)):
                tag = chipy.RBDY2_GetContactorColor(i+1,1).rstrip('_')
                self._tag2id.setdefault(tag, []).append(i)
              
        self._refRadius=np.amin(self._r)
      
      elif dim == 3:  
      
        self._nbSpher   = chipy.SPHER_GetNbSPHER()
        self._d2bMap   = chipy.SPHER_GetPtrSPHER2BDYTY()
        self._position = np.zeros([self._nbSpher,3], 'd')
        self._velocity = np.zeros([self._nbSpher,6], 'd')
        self._externalF= np.zeros([self._nbSpher,6], 'd')
        self._volume   = np.zeros([self._nbSpher,1], 'd')
        self._mass   = np.zeros([self._nbSpher,1], 'd')
        self._r   = np.zeros([self._nbSpher,1], 'd')      
        for i in range(self._nbSpher):
          self._r[i] = chipy.SPHER_GetContactorRadius(i+1)
          self._volume[i] = np.pi * chipy.SPHER_GetContactorRadius(i+1)**3 * 4./3
          self._mass[i] = chipy.RBDY3_GetMass(int(self._d2bMap[i,0]))

        self._refRadius=np.amin(self._r)
        
        self._tag2bnd = {}
        self._tag2id = {}
        for i in range(chipy.RBDY3_GetNbRBDY3()):
            for t in range(chipy.RBDY3_GetNbContactor(i+1)):
                tag = chipy.RBDY3_GetContactorColor(i+1,1).rstrip('_')
                self._tag2id.setdefault(tag, []).append(i)

      else :
        chipy.utilities_logMes('dim must be 2 or 3')
        sys.exit()
                
      self._freq_detect   = 1
      self._solver_params = { 'type'  :'Stored_Delassus_Loops         ',
                              'norm'  : 'Quad ',
                              'conv'  : 1e-5,
                              'relax' : 1.,
                              'gsit1' : 200,
                              'gsit2' : 20
                            }
   
  def set_boundary_velocity(self, tag, v) :
      self._tag2bnd[tag] = v

  def contact_forces(self):
        if self._fc is None:
            self._fc = np.zeros_like(self.velocity())
        return(self._fc)

  def write_vtk(self, odir, iiter, t) :
      v = self.velocity()
      x = self.position()
      if self._dim == 2 :
          v = np.insert(v,2,0,axis=1)
          x = np.insert(x,2,0,axis=1)
      data = [("Mass",self.mass()), ("Radius",self.r()),("Velocity",v)]
      VTK.write(odir+"/particles",iiter,t,None,x,data,vtktype="vtp")

      lmgcids = ("POLYG","PLANx","POLYR")
      vtkids = (7,12,13)
      def CHIPY(lid,fct) :
          return getattr(chipy,lid+"_"+fct)()
      def getx(l) :
          x = CHIPY(l,"InitOutlines")
          s = CHIPY(l,"InitScalarFields")          
          CHIPY(l,"UpdatePostdata")
          if x.shape[1] == 2 : x = np.insert(x,2,0,axis=1)
          return x.reshape((-1,3))
      x = np.vstack(list(getx(l) for l in lmgcids))
      connectivity = np.arange(0,x.shape[0],dtype=np.int32)
      n = np.hstack(list(CHIPY(l,"GetNbPointOutlines")[1:]-CHIPY(l,"GetNbPointOutlines")[:-1] for l in lmgcids))
      offsets = np.cumsum(n)
      types = np.repeat(vtkids,list(CHIPY(l,"GetNb"+l) for l in lmgcids))
      VTK.write(odir+"/boundaries",iiter,t,(types,connectivity,offsets),x)
      # 2D: DKDKx_ID, DKJCx_ID, PLPLx_ID, PLJCx_ID, DKPLx_ID, DKKDx_ID
      # 3D:  SPSPx_ID, PRPRx_ID, PRPLx_ID, SPPLx_ID ...
      def get_contacts(contact_type,map0,map1) :
          n = chipy.inter_handler_2D_getNb(contact_type)
          if n > 0 :
              # coorx,coory,nx,ny,fn,ft,g
              contacts = chipy.inter_handler_2D_getAll(contact_type)
              contactids = list(chipy.inter_handler_2D_getIdBodies(contact_type,i) for i in range(1,n+1))
              contactids = np.array(list((map0[i[1]],map1[i[0]]) for i in contactids))
          else :
              contacts = np.ndarray((0,1),np.float64)
              contactids = np.ndarray((0,2),np.uint64)
          return contacts,contactids
      fdata = []
      dmap = dict((v[0],i) for i,v in enumerate(self._d2bMap))
      pmap = dict((v[0],i) for i,v in enumerate(self._p2bMap))
      dkdk,dkdkid = get_contacts(chipy.DKDKx_ID,dmap,dmap)
      dkpl,dkplid = get_contacts(chipy.DKPLx_ID,pmap,dmap)
      fdata.append((b"particle_particle",dkdk[:,[4]]))
      fdata.append((b"particle_particle_t",np.zeros((dkdk.shape[0],1))))
      fdata.append((b"particle_particle_idx",dkdkid))
      fdata.append((b"particle_segment",dkpl[:,[4]]))
      fdata.append((b"particle_segment_t",np.zeros((dkpl.shape[0],1))))
      fdata.append((b"particle_segment_idx",dkplid))
      fdata.append((b"particle_disk",np.ndarray((0,1),np.float64)))
      fdata.append((b"particle_disk_t",np.ndarray((0,1),np.float64)))
      fdata.append((b"particle_disk_idx",np.ndarray((0,2),np.uint64)))
      x = np.array([[0.,0.,0.]])
      i = iiter
      VTK.write(odir+"/contacts",i,t,None,x,field_data=fdata,vtktype="vtp")
      VTK.write_multipart(odir+"/particle_problem",["particles_%05d.vtp"%i,"boundaries_%05d.vtu"%i,"contacts_%05d.vtp"%i],i,t)



  def write_vtk_lmgc(self, filemame, i, t) :
    # chipy.WriteOutDof(1)
    # chipy.WriteOutVlocRloc(1)
    chipy.WritePostproFiles()
    chipy.WriteDisplayFiles(1, self._refRadius)

  def iterate(self, dt, forces, tol=None, gsit1=None, gsit2=None, freqWrite=0):
      """
      Do one step of a lmgc90 computation.
      """

      if tol is not None : self._solver_params['conv'] = tol          
      if gsit1 is not None : self._solver_params['gsit1'] = gsit1
      if gsit2 is not None : self._solver_params['gsit2'] = gsit2          

      vn = self.velocity().copy()
      chipy.TimeEvolution_SetTimeStep(dt)

      self._externalF[:,:self._dim] = forces

      chipy.IncrementStep()
      chipy.ComputeFext()
      if (self._dim == 3):
        for tag, v in self._tag2bnd.items() :
            for i in self._tag2id[tag] :
                for j, iv in enumerate(v):
                  chipy.RBDY3_SetVlocyDrivenDof(i+1,j+1,iv)
  

        for i in range(self._nbSpher):
          chipy.RBDY3_PutBodyVector('Fext_', int(self._d2bMap[i,0]), self._externalF[i,:])

      elif (self._dim == 2):
        for tag, v in self._tag2bnd.items() :
           for i in self._tag2id[tag] :
              for j, iv in enumerate(v):
                 chipy.RBDY2_SetVlocyDrivenDof(i+1,j+1,iv)
  

        for i in range(self._nbDisk):
          chipy.RBDY2_PutBodyVector('Fext_', int(self._d2bMap[i,0]), self._externalF[i,:])        

      chipy.ComputeBulk()
        
      chipy.ComputeFreeVelocity()
  
      chipy.SelectProxTactors(self._freq_detect)
  
      chipy.RecupRloc()
      chipy.ExSolver(**self._solver_params)
      chipy.StockRloc()
  
      chipy.ComputeDof()
  
      chipy.UpdateStep()

      if freqWrite :
        chipy.WriteOutDof(freqWrite)
        chipy.WriteOutVlocRloc(freqWrite)

      self._fc = (self.velocity()-vn)*self.mass()/dt - forces
      
  def volume(self):
      """ Return the volume of the  particles """
      return self._volume

  def mass(self):
      """ Return the mass of the  particles """
      return self._mass

  def r(self):
      """ Return the radius of the  particles """
      return self._r

  def position(self):
      """ Get current position of contactors and return it """

      if self._dim == 3:
        for i in range(self._nbSpher):
          self._position[i,:] = chipy.SPHER_GetContactorCoor(i+1)[:3]
        return self._position
      
      elif  self._dim == 2:
        for i in range(self._nbDisk):
          self._position[i,:] = chipy.RBDY2_GetBodyVector('Coor_',int(self._d2bMap[i,0]))
        self._position[i,2] = 0.
        return self._position[:,:2]
      
  def velocity(self):
      """ Get current velocity of body of contactor and return it
      Beware : it should not work very well with clusters !
      """
      if self._dim == 3:
        for i in range(self._nbSpher):
          self._velocity[i,:] = chipy.RBDY3_GetBodyVector('V____',int(self._d2bMap[i,0]))
        return self._velocity[:,:3]

      elif self._dim==2:
        for i in range(self._nbDisk):
          self._velocity[i,:] = chipy.RBDY2_GetBodyVector('V____',int(self._d2bMap[i,0]))
        self._velocity[i,2] = 0.
        return self._velocity[:,:2]
        
      
  def externalForces(self):
      """ Get an external forces array
      """
      return self._externalF[:,:self._dim]

  def __del__(self):
      """
      """
      chipy.ClosePostproFiles()
      chipy.CloseDisplayFiles()
      chipy.Finalize()

def scontactTolmgc90(dirname, dim, it=0, fric = 0., assume_box=False):
    from migflow import scontact
    from pylmgc90 import pre
    datbox_path = 'DATBOX'
    if not os.path.isdir(datbox_path):
      os.mkdir(datbox_path)

    sc = scontact.ParticleProblem(dim)
    sc.read_vtk(dirname,it)

    x = sc.position()
    v = sc.velocity()
    v[:] = 0.

    r = sc.r()
    vol = sc.volume()

    rho_particle = np.mean(sc.mass()/vol)

    avs = pre.avatars()
    mat = pre.materials()
    mod = pre.models()
    svs = pre.see_tables()
    tac = pre.tact_behavs()


    if dim == 3 :
    
      mater = pre.material(name='STONE',materialType='RIGID',density=rho_particle)
      model = pre.model(name='rigid', physics='MECAx', element='Rxx3D',dimension=3)
      mat.addMaterial(mater)
      mod.addModel(model)

      for i in range(r.size) :
         P = pre.rigidSphere( r=r[i], center=x[i], model=model, material=mater, color='INxxx')
         P.imposeInitValue(component=[1,2,3],value=list(v[i,:]))
         avs.addAvatar(P)

      clb_fric = pre.tact_behav(name='iqsc0',law='IQS_CLB',fric=fric)
      tac     += clb_fric

      svs += pre.see_table(CorpsCandidat   ="RBDY3", candidat   ="SPHER", colorCandidat   ='INxxx',
                           CorpsAntagoniste="RBDY3", antagoniste="SPHER", colorAntagoniste='INxxx',
                           behav=clb_fric, alert=r.min())
       
      ep=np.amin(r)   
      tri = sc.triangles()

      if (assume_box) :
        xmin=min(np.amin(tri[:,0]),np.amin(tri[:,3]), np.amin(tri[:,6]))
        xmax=min(np.amax(tri[:,0]),np.amax(tri[:,3]), np.amax(tri[:,6]))       
        ymin=min(np.amin(tri[:,1]),np.amin(tri[:,4]), np.amin(tri[:,7]))
        ymax=min(np.amax(tri[:,1]),np.amax(tri[:,4]), np.amax(tri[:,7]))       
        zmin=min(np.amin(tri[:,2]),np.amin(tri[:,5]), np.amin(tri[:,8]))
        zmax=min(np.amax(tri[:,3]),np.amax(tri[:,5]), np.amax(tri[:,8]))

        lx = xmax - xmin
        ly = ymax - ymin
        lz = zmax - zmin

        pxmin = pre.rigidPlan(axe1=lz*0.505, axe2=ly*0.505, axe3=ep, \
                              center=[xmin-ep,ymin+0.5*ly,zmin+0.5*lz],
                              model=model, material=mater, color='WALLx')
        pxmin.rotate(description='axis',center=pxmin.nodes[1].coor,axis=[0.,1.,0.],alpha=math.pi*0.5)
        pxmin.imposeDrivenDof(component=[1,2,3,4,5,6],dofty='vlocy')
        avs+=pxmin
        pxmax = pre.rigidPlan(axe1=lz*0.505, axe2=ly*0.505, axe3=ep, \
                              center=[xmax+ep,ymin+0.5*ly,zmin+0.5*lz],
                              model=model, material=mater, color='WALLx')
        pxmax.rotate(description='axis',center=pxmax.nodes[1].coor,axis=[0.,1.,0.],alpha=math.pi*0.5)
        pxmax.imposeDrivenDof(component=[1,2,3,4,5,6],dofty='vlocy')      
        avs+=pxmax

        pymin = pre.rigidPlan(axe1=lx*0.505, axe2=lz*0.505, axe3=ep, \
                              center=[xmin+0.5*lx,ymin-ep,zmin+0.5*lz],
                              model=model, material=mater, color='WALLx')
        pymin.rotate(description='axis',center=pymin.nodes[1].coor,axis=[1.,0.,0.],alpha=math.pi*0.5)
        pymin.imposeDrivenDof(component=[1,2,3,4,5,6],dofty='vlocy')      
        avs+=pymin
        
        pymax = pre.rigidPlan(axe1=lx*0.505, axe2=lz*0.505, axe3=ep, \
                              center=[xmin+0.5*lx,ymax+ep,zmin+0.5*lz],
                              model=model, material=mater, color='WALLx')
        pymax.rotate(description='axis',center=pymax.nodes[1].coor,axis=[1.,0.,0.],alpha=math.pi*0.5)
        pymax.imposeDrivenDof(component=[1,2,3,4,5,6],dofty='vlocy')      
        avs+=pymax
      
        pzmin = pre.rigidPlan(axe1=lx*0.505, axe2=ly*0.505, axe3=ep, \
                             center=[xmin+0.5*lx,ymin+0.5*ly,zmin-ep],
                             model=model, material=mater, color='WALLx')
        pzmin.imposeDrivenDof(component=[1,2,3,4,5,6],dofty='vlocy')      
        avs+=pzmin
        
        pzmax = pre.rigidPlan(axe1=lx*0.505, axe2=ly*0.505, axe3=ep, \
                              center=[xmin+0.5*lx,ymin+0.5*ly,zmax+ep],
                              model=model, material=mater, color='WALLx')
        pzmax.imposeDrivenDof(component=[1,2,3,4,5,6],dofty='vlocy')      
        avs+=pzmax
      
      
        svs += pre.see_table(CorpsCandidat   ="RBDY3", candidat   ="SPHER", colorCandidat   ='INxxx',
                             CorpsAntagoniste="RBDY3", antagoniste="PLANx", colorAntagoniste='WALLx',
                             behav=clb_fric, alert=r.min())
      else :
        bndtags = set()
        for i in range(tri.shape[0]) :
          x0 = np.array(tri[i, 0:3])
          x1 = np.array(tri[i, 3:6])
          x2 = np.array(tri[i, 6:9])
          tag = 'xxxxx'
          tag += "_" * (5 - len(tag))
          bndtags.add(tag)
          t0 = (x0 - x1)/np.linalg.norm(x0 - x1)
          t1 = (x0 - x2)/np.linalg.norm(x0 - x2)
          n = np.cross(t0, t1)
          n *= ep / np.linalg.norm(n)

          vs = np.array([x0-n, x1 - n, x2 - n, x0 + n, x1 + n, x2 + n])
          fs = np.array([[0, 2, 1], [3, 4, 5], [0, 1, 3], [3, 1, 4], [1, 5, 4], [1, 2, 5], [0, 3, 2], [3, 5, 2]]) + 1
          av = pre.rigidPolyhedron(model,mater,np.zeros([3]),color=tag,generation_type="full",vertices=vs, faces=fs)
          av.imposeDrivenDof(component=[1,2,3,4,5,6],dofty='vlocy')
          avs.addAvatar(av)
  
        for tag in bndtags :
          svs += pre.see_table(CorpsCandidat   ="RBDY3", candidat   ="SPHER", colorCandidat   ='INxxx',
                               CorpsAntagoniste="RBDY3", antagoniste="POLYR", colorAntagoniste=tag,
                               behav=clb_fric, alert=r.min())

    elif dim==2 :
      
      mater = pre.material(name='STONE',materialType='RIGID',density=rho_particle)
      model = pre.model(name='rigid', physics='MECAx', element='Rxx2D',dimension=2)
      mat.addMaterial(mater)
      mod.addModel(model)

      for i in range(r.size) :
         P = pre.rigidDisk( r=r[i], center=x[i], model=model, material=mater, color='INxxx')
         P.imposeInitValue(component=[1,2],value=list(v[i,:]))
         avs.addAvatar(P)

      seg = sc.segments()
      bndtags = set()
      for i in range(seg.shape[0]) :
        x0 = np.array(seg[i, 0:2])
        x1 = np.array(seg[i, 2:4])
        tag = 'xxxxx'
        tag += "_" * (5 - len(tag))
        bndtags.add(tag)
        t = (x0 - x1)/np.linalg.norm(x0 - x1)
        n = np.array([-t[1], t[0]]) * 1e-4
        vs = np.array([x0-2*n, x0, x1, x1 -2*n])
        av = pre.rigidPolygon(model,mater,np.zeros([2]),color=tag,generation_type="full",vertices=vs)
        av.imposeDrivenDof(component=[1,2,3],dofty='vlocy')
        avs.addAvatar(av)
        
      clb_fric = pre.tact_behav(name='iqsc0',law='IQS_CLB',fric=fric)
      tac     += clb_fric

      svs += pre.see_table(CorpsCandidat   ="RBDY2", candidat   ="DISKx", colorCandidat   ='INxxx',
                           CorpsAntagoniste="RBDY2", antagoniste="DISKx", colorAntagoniste='INxxx',
                           behav=clb_fric, alert=r.min())

      for tag in bndtags :
        svs += pre.see_table(CorpsCandidat   ="RBDY2", candidat   ="DISKx", colorCandidat   ='INxxx',
                             CorpsAntagoniste="RBDY2", antagoniste="POLYG", colorAntagoniste=tag,
                             behav=clb_fric, alert=r.min())
          
    # file writting
    pre.writeBodies(avs,chemin=datbox_path)
    pre.writeDrvDof(avs,chemin=datbox_path)
    pre.writeDofIni(avs,chemin=datbox_path)
    pre.writeModels(mod,chemin=datbox_path)
    pre.writeBulkBehav(mat,chemin=datbox_path, gravy=[0.,0.,0.])
    pre.writeTactBehav(tac,svs,chemin=datbox_path)
    pre.writeVlocRlocIni(chemin=datbox_path)
    
    post = pre.postpro_commands()
    post.addCommand(pre.postpro_command(name='SOLVER INFORMATIONS', step=1))
    pre.writePostpro(commands=post, parts=avs, path=datbox_path)
