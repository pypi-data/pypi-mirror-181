# %%
# Bidimensional fall of a cloud made of particles in a viscous fluid.
# ===================================================================
# This examples illustrates how to define the fluid problem as well as the particles one.
# All the relevant mesh information is directly loaded from the GMSH api.
import os
import time
import gmsh
import shutil
import ctypes
import numpy as np
from scipy.spatial import KDTree
from migflow import fluid
from migflow import scontact
from migflow import time_integration

use_callback = False

# %%
# First, let's create the output directory.
# Define output directory
outputdir = "output-drop"
shutil.rmtree(outputdir,ignore_errors=True)
if not os.path.isdir(outputdir) :
    os.makedirs(outputdir)

# %%
# Mesh generation
# ---------------
# The mesh geometry is created with the python GMSH api.
height = 2                                      # domain height
width = 0.1                                     # domain width
origin = [-width/2, -height/2]                  # leftmost bottom corner

def gen_geometry(width, height, origin=np.array([0,0])):
    origin = np.asarray(origin)
    gmsh.model.add("box")
    gmsh.model.occ.add_rectangle(origin[0], origin[1], 0, width, height)
    gmsh.model.occ.synchronize()
    def get_line(x0, x1, eps =1e-6):
        r = gmsh.model.get_entities_in_bounding_box(x0[0]-eps, x0[1]-eps, -eps, x1[0]+eps, x1[1]+eps, eps, 1)
        return list(tag for dim, tag in r)
    h, w = height, width
    gmsh.model.add_physical_group(1,get_line(origin+[0,0], origin+[w,0]), name="Bottom")
    gmsh.model.add_physical_group(1,get_line(origin+[0,h], origin+[w,h]), name="Top")
    gmsh.model.add_physical_group(1,get_line(origin+[0,0], origin+[0,h])+get_line(origin+[w,0], origin+[w,h]), name="Lateral")
    gmsh.model.add_physical_group(2,[1], name="domain")
# %%
# The mesh size can be chosen based on three approaches; based on a computed field, based on a callback or based on a uniform mesh size.

# %%
# The mesh size is computed based on the gradient variation. The field is then given to gmsh which will generate the mesh.
def gen_mesh_field(f):
    lcmin = 0.0015/4
    lcmax = 0.015/8   
    grad = f.fields_gradient()
    grad_u, grad_v, grad_p = grad[:,0,:], grad[:,1,:], grad[:,2,:]
    grad_v = np.linalg.norm(grad_v, axis=1)
    grad_v_min = np.min(grad_v)
    grad_v_max = np.max(grad_v)
    lv = (grad_v_max - grad_v_min)/(grad_v-grad_v_min) * lcmin
    size = np.maximum(lv, lcmax)

    x = f.coordinates()[f.elements()]
    size_view = gmsh.view.add("size")
    data = np.c_[x.swapaxes(1,2).reshape(-1,9), size[f.elements()]]
    size_field = gmsh.model.mesh.field.add("PostView")
    gmsh.model.mesh.field.setNumber(size_field, "ViewTag", size_view)
    gmsh.model.mesh.field.setAsBackgroundMesh(size_field)
    gmsh.view.add_list_data(size_view, "ST", data.shape[0], data.reshape(-1))
    gmsh.model.mesh.clear()
    gmsh.model.mesh.generate(2)
    gmsh.view.remove(size_view)

# %%
# The mesh size is computed based on a callback function. Here a refinement is done close to the particles position.
def gen_mesh_callback(xp):
    tree = KDTree(xp)
    def size_f(x):
        dist, _ = tree.query(x[:,:2])
        distmin = 0.01
        lcmin = 0.0015
        lcmax = 0.015
        alpha = np.clip((dist[0]-distmin)/0.1, 0, 1)
        size = lcmin*(1-alpha) + lcmax*alpha
        return size
    gmsh.model.mesh.set_size_callback(lambda dim, tag, x, y, z, lc: size_f(np.array([[x,y]])))
    gmsh.model.mesh.clear()
    gmsh.model.mesh.generate(2)
    gmsh.model.mesh.remove_size_callback()

# %%
# The mesh is generated based on a constant mesh size.
def gen_mesh_uniform(size):
    gmsh.model.mesh.clear()
    gmsh.model.mesh.set_size_callback(lambda dim, tag, x, y, z, lc: size)
    gmsh.model.mesh.generate(2)
    gmsh.model.mesh.remove_size_callback()

# %% 
# Particle Problem
# ----------------
# The particle problem is created and its dimension is provided.
p = scontact.ParticleProblem(2)

# %%
# The particle properties are defined.
# All the particles are assumed to be spherical.
r    = 25e-6                                       # particles radius
rhop = 2450                                         # particles density
compacity = 0.2                                     # solid volume fraction in the drop
rout = 3.3e-3                                       # drop radius

# %%
# The particle positions are initialised randomly in a circular domain to obtain a given compacity.
def genInitialPosition(p, r, rout, rhop, compacity, origin) :
    """Set all the particles centre positions and create the particles objects
    
    Keyword arguments:    
    p -- Particle Problem
    r -- max radius of the particles
    rout -- outer radius of the cloud
    rhop -- particles density        
    compacity -- initial compacity in the cloud
    """
    # Space between the particles to obtain the expected compacity
    N = compacity*(rout/r)**2
    bodies = np.asarray([], int)
    while p.n_particles() < N:
        xyp = np.random.uniform(-rout, rout, 2)
        if np.hypot(xyp[0], xyp[1]) < rout:
            if p.n_particles() == 0:
                d = 1
            else:
                d = np.min(np.linalg.norm(p.position()-xyp[None,:],axis=1))
            if d > 2.1*r:
                body = p.add_particle(xyp, r, r**2 * np.pi * rhop)
                bodies = np.append(bodies,body)
    # Shift of the particles to the top of the box
    p.body_position()[bodies, :] += origin
    return bodies
bodies = genInitialPosition(p, r, rout, rhop, compacity, np.array([0,1.9*height/4]))


# %%
# Fluid Problem
# -------------
# The fluid is described by its dimension, the external volume force applied, its dynamic viscosity and its density.
g   = np.array([0,-9.81])                           # gravity
rho = 1030                                          # fluid density
nu  = 1.17/(2*rho)                                  # kinematic viscosity
mu  = rho*nu                                        # dynamic viscosity
f   = fluid.FluidProblem(2,g,[nu*rho],[rho], usolid=True)

# %%
# The mesh is created with a refinment close to the particles position.
# The boundaries are loaded either from a .msh file or from the current model loaded with the GMSH api (if None as a filename is given). 
gen_geometry(width, height, origin)
if use_callback:
    gen_mesh_callback(p.position()[p.r()[:,0]>0])
else:
    gen_mesh_uniform(0.015)
    f.load_msh(None)
p.load_msh_boundaries(None, ["Bottom","Top","Lateral"])
## %%
# The mesh can be loaded through the GMSH api if None is given or through a mesh filename.
# The boundary conditions are described by their physical name.
# To fully describe the pressure, its mean value over all the nodal values is set to zero.
f.load_msh(None)
f.set_wall_boundary("Bottom")
f.set_wall_boundary("Top")
f.set_wall_boundary("Lateral")
f.set_mean_pressure(0)

# %%
# FEM-DEM coupling
# ----------------
# The presence of particles is given to the fluid through the fluid volume fraction, i.e. the porosity and through a drag parametrization.
# All the relevant informations needed for the fluid is given by :  
f.set_particles(p.delassus(), p.volume(), p.position(), p.velocity(), p.contact_forces())

# %%
# Time integration
# ----------------
# The numerical parameters are defined given and the initial conditions are written in the output directory.
outf = 1                                            # number of iterations between output files
remeshing=5                                         # time step to adapt the mesh
dt   = 1e-2                                         # time step
tEnd = 50                                           # final time
t    =  0                                           # initial time
ii   =  0                                           # initial iteration
number_p = f.n_particles
position_p = f.particle_position()
volume_p = f.particle_volume()

# %%
# Write chosen fields into the output
# -----------------------------------
def get_fields(fluid):
    y = fluid.coordinates_fields()[fluid.pressure_index()][:,1]
    y = y.reshape(-1,1)
    p1_element = fluid.get_p1_element()
    return {"pressure": (fluid.pressure(), p1_element),
            "velocity": (fluid.velocity(), p1_element),
            "porosity": (fluid.porosity(), p1_element),
            "dynamic_pressure":(fluid.pressure()-rho*g[1]*y, p1_element)}

p.write_mig(outputdir, t)
f.write_mig(outputdir, t, get_fields(f))
# %%
# The computational loop can start.
# The particles phase will use sub-iterations to keep a stable method. The minimal number of subiterations is given by min_nsub.
# The external forces given to the particles have to be given at each time step.
# A predictor-corrector method can also be used by setting the flag to True.
tic = time.process_time()

while t < tEnd :
    forces = g*np.pi*p.r()**2*rhop
    time_integration.iterate(f, p, dt, min_nsub=2, external_particles_forces=forces, use_predictor_corrector=False)
    if ((ii+1)%remeshing==0):
        number_p = f.n_particles
        position_p = f.particle_position()
        volume_p = f.particle_volume()
    if (ii%remeshing==0 and ii != 0):
        if use_callback:
            gen_mesh_callback(p.position()[p.r()[:,0]>0])
        else:
            gen_mesh_field(f)
        f.adapt_mesh(old_n_particles=number_p, old_particle_position=position_p, old_particle_volume=volume_p)
        f.set_particles(p.delassus(), p.volume(), p.position(), p.velocity(), p.contact_forces())
    t += dt
    # Output files writting
    if ii%outf == 0 :
        p.write_mig(outputdir, t)
        f.write_mig(outputdir, t, get_fields(f))
    ii += 1
    print("%i : %.2g/%.2g (cpu %.6g)" % (ii, t, tEnd, time.process_time() - tic))

