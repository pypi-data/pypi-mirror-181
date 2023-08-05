# %%
# Bidimensional elongated particles avalanch into a air-water box.
# ================================================================
# This example described how to initialise a particle problem with elongated bodies with prescribed orientation.
# It also describes how to create a 2-fluids problem into MigFlow, air and water are considered in this example.
import os
import gmsh
import time
import shutil
import random
import numpy as np
from migflow import fluid
from migflow import scontact
from migflow import time_integration

# %%
# First, let's create the output directory.
# Define output directory
outputdir = "output-avalanche"
shutil.rmtree(outputdir,ignore_errors=True)
if not os.path.isdir(outputdir) :
    os.makedirs(outputdir)
# %%
# Domain parameters :
height = 0.3                                                # domain height
width  = 1.0                                                # domain width
# %%
# Body description
# ----------------
# We will see how to create a initial packing with a chosen bodies orientation
# The body is described by its mask over a grid.
model = np.array([[1,1,1,1]])
n_p_b = np.sum(model)                                       # number of particles by body
angle = np.pi/4
# %%
# Lets's define the body and particles properties :
g        = np.array([0, -9.81])                             # gravity
rhop     = 1840                                             # particle density
friction = 0.1                                              # friction coefficient
r        = 2e-3                                             # maximal particle radius
d        = 2*r                                              # maximal particle diameter
b_size   = d*n_p_b                                          # maximal body size
# %%
# Initial disk particles depot 
# ----------------------------
# %%
# First, we consider the falling of bidimensional particles into an open box.
# Each particle has a diameter of the body size.
init_disk = scontact.ParticleProblem(2)
init_disk.set_fixed_contact_geometry(0)
init_disk.set_friction_coefficient(friction)

# %%
# The open box is defined using three segments.
w  = 0.075                                                  # open-box width
h  = 2.5                                                    # open-box height
init_disk.add_boundary_segment([0, 0], [0, h], "left")
init_disk.add_boundary_segment([w, h], [w, 0], "right")
init_disk.add_boundary_segment([w, 0], [0, 0], "bottom")
# %%
# The particles are then generated on a compact rectangular grid of size lx X ly :
x0     = np.array([w/2, h/2])
lx     = .5*w
ly     = .75*h
x      = np.arange(-lx/2, lx/2, b_size) + x0[0]
y      = np.arange(-ly/2, ly/2, b_size) + x0[1]
x,y    = np.meshgrid(x,y)
bodies = np.asarray([], int) 
for xi,yi in zip(x.flat, y.flat):
    ri = .5*np.random.uniform(0.8,1)*b_size
    body = init_disk.add_particle((xi,yi), ri, ri**2*np.pi*rhop)
    bodies = np.append(bodies, body)
# %%
# Time integration
# The numerical parameters is given and the initial conditions are written in the output directory.
outf = 100                                                  # number of iterations between output files
dt   = 1e-3                                                 # time step
t    = 0                                                    # initial time
tEnd = 1.5                                                  # final time
ii   = 0                                                    # interator
tic  = time.process_time()
init_disk.write_mig(outputdir, t)
# %%
# The computational loop can start.
# The external forces given to the particles has to be given at each time step.
while t < tEnd:
    forces = g*np.pi*init_disk.r()**2*rhop
    time_integration.iterate(None, init_disk, dt, 2, 2e-6, forces)
    t  += dt
    ii += 1
    if ii%outf==0:
        init_disk.write_mig(outputdir, t)
    print("%i : %.2g/%.2g (cpu %.6g)" % (ii, t, tEnd, time.process_time() - tic))
t += dt
# %%
# From disks to bodies
# --------------------
# We create a new problem for the bodies.
# The option fixed_contact_geometry has to be put to zero to solve bodies dynamics.
p = scontact.ParticleProblem(2)
p.set_friction_coefficient(friction)
p.set_fixed_contact_geometry(0)
# %%
# The open box is styill defined using three segments.
p.add_boundary_segment([0, 0], [0, h], "left")
p.add_boundary_segment([w, h], [w, 0], "right")
p.add_boundary_segment([w, 0], [0, 0], "bottom")
# %%
# Each body of this new problem will have the position of the initial problem
p_bodies = np.asarray([], int)
for i,body in enumerate(bodies):
    rpi      = init_disk.r()[i]/n_p_b
    x,y      = np.where(model)
    x        = 2*np.stack([x,y],axis=1)
    xb       = rpi*x
    radii    = np.repeat(rpi, n_p_b)
    masses   = radii**2*np.pi*rhop
    p_body   = p.add_particle_body(xb,radii,masses)
    p_bodies = np.append(p_bodies, p_body)
p.body_position()[:] = init_disk.body_position()[:]
p.body_theta()[p_bodies,:] = -angle
# %% 
# First, we will let the bodies falling without any rotation.
# To do so, body inverse inertias are set to zero. 
body_iinvertia = p.body_invert_inertia().copy()
p.body_invert_inertia()[p_bodies] = 0

# %%
# The numerical parameters are modified and the computational loop can start.
outf = 100
dt   = 2.5e-4
tEnd = 2
while t < tEnd:
    forces = g*np.pi*p.r()**2*rhop
    time_integration.iterate(None, p, dt, 2, 2e-6, forces)
    t  += dt
    ii += 1
    if ii%outf==0:
        p.write_mig(outputdir, t)
    print("%i : %.2g/%.2g (cpu %.6g)" % (ii, t, tEnd, time.process_time() - tic))
t += dt

# %%
# Then the rotation are activated by restoring the body inertias :
p.body_invert_inertia()[:] = body_iinvertia
# %%
# The numerical parameters are modified and the computational loop can start.
outf = 100
dt   = 2.5e-4
tEnd = 3.5
while t < tEnd:
    forces = g*np.pi*p.r()**2*rhop
    time_integration.iterate(None, p, dt, 2, 2e-6, forces)
    t  += dt
    ii += 1
    if ii%outf==0:
        p.write_mig(outputdir, t)
    print("ii : %4d"%ii)
t += dt
# %%
# The boundaries is then modified to describe the same domain as the fluid
w, h = width, height
p.body_position()[:3] = 0                               # restore initial boundary body position
p.segments()[0]["relative_position"]  = np.array([[0,0],[0,h]])         # left
p.segments()[1]["relative_position"]  = np.array([[w,h],[w,0]])         # right
p.segments()[2]["relative_position"]  = np.array([[w,0],[0,0]])         # bottom    
p.add_boundary_segment([0,h], [w,h], "top")
# %%
# Mesh generation
# ----------------
# The domain is created through the python GMSH api is loaded to generate the mesh and extract the boundaries.
# The refinement is given by the function set_size_call_back. In this example, a constant mesh size is chosen.
mesh_size = 0.01                                # mesh size
def gen_mesh(width, height, mesh_size, origin=np.array([0,0])):
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
    gmsh.model.add_physical_group(1,get_line(origin+[0,0], origin+[0,h]), name="Left")
    gmsh.model.add_physical_group(1,get_line(origin+[w,0], origin+[w,h]), name="Right")
    gmsh.model.add_physical_group(2,[1], name="domain")
    gmsh.model.mesh.set_size_callback(lambda dim, tag, x, y, z, lc : mesh_size)
    gmsh.model.mesh.generate(2)

gen_mesh(w, h, mesh_size)

# %%
# Fluid Problem
# -------------
# The fluid is described by its dimension, the external volume force applied, its dynamic viscosities and its densities.
# The 2-fluid model is deduced from the length of the densities and viscosities provided.
rho0 = 1                                                # fluid density
nu0  = 1e-5                                             # kinematic viscosity
rho1 = 1000                                             # fluid density
nu1  = 1e-6                                             # kinematic viscosity
mu0  = rho0*nu0                                         # dynamic viscosity 
mu1  = rho1*nu1                                         # dynamic viscosity
f   = fluid.FluidProblem(2,g,[mu0, mu1],[rho0, rho1], model_b=1)

## %%
# The mesh can be loaded through the GMSH api if None is given or through a mesh filename.
# The boundary conditions are described by their physical name.
# To describle fully the pressure, its mean value over all the nodal values is impose to zero.
f.load_msh(None)
f.set_wall_boundary("Bottom")
f.set_wall_boundary("Left")
f.set_wall_boundary("Right")
f.set_wall_boundary("Top")
f.set_mean_pressure(0)
# %%
# The initial air concentration is described by setting the concentration to 1 in the half upper domain. 
x_cg     = f.coordinates()
c0       = np.zeros_like(x_cg[:,0])
x_up     = x_cg[:,1] > h/2 
c0[x_up] = 1
f.set_concentration_cg(c0)

# %%
# FEM-DEM coupling
# ----------------
# The presence of particles is given to the fluid through the fluid volume fraction, i.e. the porosity and through a drag parametrization.
# All the relevant informations needed for the fluid is given by :  
f.set_particles(p.delassus(), p.volume(), p.position(), p.velocity(), p.contact_forces())

# %%
# Time integration
# ----------------
# The numerical parameters is given and the initial conditions are written in the output directory.
outf = 25                                               # number of iterations between output files
dt   = 5e-4                                             # time step
tEnd = 10                                               # final time
ii   =  0                                               # initial iteration
p.write_mig(outputdir, t)
f.write_mig(outputdir, t)
tic = time.process_time()

# %%
# The computational loop can start.
# The particles phase will use sub-iterations to keep a stable method. The minimal number of subiterations is given by min_nsub.
# The external forces given to the particles has to be given at each time step.
# To solve the two scales, first the fluid is solved then the particles are resolved.
# A predictor-corrector method can also be used by imposing the flag to True.
while t < tEnd :
    forces = np.pi*p.r()**2*rhop * g
    time_integration.iterate(f, p, dt, min_nsub=2, external_particles_forces=forces, use_predictor_corrector=False)
    t  += dt
    ii += 1
    # Output files writting
    if ii%outf == 0 :
        p.write_mig(outputdir, t)
        f.write_mig(outputdir, t)
    print("%i : %.2g/%.2g (cpu %.6g)" % (ii, t, tEnd, time.process_time() - tic))