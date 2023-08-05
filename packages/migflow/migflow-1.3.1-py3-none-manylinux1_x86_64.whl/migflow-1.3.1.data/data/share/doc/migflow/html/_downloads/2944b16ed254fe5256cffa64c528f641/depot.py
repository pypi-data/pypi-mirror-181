# %%
# Bidimensional particles sedimentation in fluid
# ==============================================
# This examples illustrates how to define the fluid problem as well as the particles one.
# All the relevant mesh information is directly loaded from the GMSH api.

import os
import time
import gmsh
import shutil
import numpy as np
from migflow import fluid
from migflow import scontact
from migflow import time_integration

# %%
# First, let's create the output directory.
# Define output directory
outputdir = "output-depot"
shutil.rmtree(outputdir,ignore_errors=True)
if not os.path.isdir(outputdir) :
    os.makedirs(outputdir)

# %%
# Mesh generation
# ----------------
# The domain is created through the python GMSH api is loaded to generate the mesh and extract the boundaries.
# The refinement is given by the function set_size_call_back. In this example, a constant mesh size is chosen.

height = 0.6                                    # domain height
width = 0.4                                     # domain width
mesh_size = 0.02                                # mesh size
origin = [-width/2, -height/2]                  # leftmost bottom corner

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

gen_mesh(width, height, mesh_size, [-width/2, -height/2])

# %% 
# Particle Problem
# ----------------
# The particle problem based is created, its dimension has to be provided.
# The boundaries are loaded either from a .msh file or from the current model loaded with the GMSH api (if None as a filename is given). 
p = scontact.ParticleProblem(2)
p.load_msh_boundaries(None, ["Top", "Left","Right","Bottom"])

# %%
# Let's define the particle properties and initialised them on a compact rectangular grid at the top of the domain.
# All the particles are assumed to be spherical.
r    = 2.5e-3                                       # particles radius
rhop = 1500                                         # particles density
h    = 1.5e-1                                       # particles area height
w    = 4e-1                                         # particles area widht
eps  = 1e-8                                         # tolerance
x    = np.arange(r-eps, w-r+eps, 2*r) + origin[0]
y    = np.arange(-r, -h, -2*r) - origin[1]
x, y = np.meshgrid(x,y)
for xi,yi in zip(x.flat,y.flat):
    p.add_particle((xi, yi), r, r**2*np.pi*rhop)

# %%
# Fluid Problem
# -------------
# The fluid is described by its dimension, the external volume force applied, its dynamic viscosity and its density.
# Moreover, in order to have a stable method for compact configuation, an extra-diffusion is activated by the drag_in_stab option.
g   = np.array([0,-9.81])                           # gravity
rho = 1000                                          # fluid density
nu  = 1e-6                                          # kinematic viscosity
mu  = rho*nu                                        # dynamic viscosity
f   = fluid.FluidProblem(2,g,nu*rho,rho,drag_in_stab=0)

# %%
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
# FEM-DEM coupling
# ----------------
# The presence of particles is given to the fluid through the fluid volume fraction, i.e. the porosity and through a drag parametrization.
# All the relevant informations needed for the fluid is given by :  
f.set_particles(p.delassus(), p.volume(), p.position(), p.velocity(), p.contact_forces())


# %%
# Time integration
# ----------------
# The numerical parameters is given and the initial conditions are written in the output directory.
outf = 25                                           # number of iterations between output files
dt   = 1e-3                                         # time step
tEnd = 10                                           # final time
t    =  0                                           # intial time
ii   =  0                                           # initial iteration
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
    t += dt
    # Output files writting
    if ii%outf == 0 :
        p.write_mig(outputdir, t)
        f.write_mig(outputdir, t)
    ii += 1
    print("%i : %.2g/%.2g (cpu %.6g)" % (ii, t, tEnd, time.process_time() - tic))
