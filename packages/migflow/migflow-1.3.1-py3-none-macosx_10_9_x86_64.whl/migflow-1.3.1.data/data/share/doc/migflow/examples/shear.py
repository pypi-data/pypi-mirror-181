# %%
# Bidimensional shear of a dry granular material
# ==============================================
import os
import time
import gmsh
import shutil
import sys
import numpy as np
from migflow import scontact
from migflow import time_integration

np.random.seed(0)
# %%
# First, let's create the output directory.
# Define output directory
outputdir = "output-shear"
shutil.rmtree(outputdir,ignore_errors=True)
if not os.path.isdir(outputdir) :
    os.makedirs(outputdir)
# %% 
# Particle Problem
# ----------------
# The particle problem is created and its dimension is provided.
p = scontact.ParticleProblem(2)
p.set_fixed_contact_geometry(0)
# %%
# The domain geometry is defined.
h = 0.1           # domain height
w = 0.2           # domain width
# %%
# The physical parameters are defined.
g =  np.array([0.,0.])                              # gravity
rhop = 1000                                         # particle density
r = 1e-3                                            # particle radius
gamma = 100                                         # shear rate
Pp = 0.05                                           # confining pressure
eps = 1e-4
lx = w/2-r                                          # particle area width
ly = h/2-r-eps                                      # particle area height
cmax=0.2                                            # compacity of the initial particle area
# %%
# Top and bottom boundaries are added to the particle problem.
x0 = np.array([-w/2-w/10, 0])
x1 = np.array([ w/2+w/10, 0])
x_segment = np.row_stack([x0, x1])
top_body = p.add_entities(xbody=np.array([0, h/2]), invertM=1/Pp, segments_coordinates=x_segment[None,:,:], segments_tags="Top", segments_materials="wall")
bottom_body = p.add_entities(xbody=np.array([0, -h/2]), segments_coordinates=x_segment[None,:,:], segments_tags="Bottom", segments_materials="wall")
# %%
# Periodic left and right boundaries are added.
trans = np.array([w,0])
p.add_boundary_periodic_entity(1,0, trans)
p.add_boundary_periodic_entity(1,1,-trans)
p.add_boundary_periodic_segment((-w/2, h/2), (-w/2,-h/2), 0)
p.add_boundary_periodic_segment(( w/2, h/2), ( w/2,-h/2), 1)
# %%
# The confining pressure, the shear rate and the friction coefficients are prescribed
p.body_velocity()[top_body, 0] = gamma*h 
p.set_friction_coefficient(0.5, "wall", "sand")
p.set_friction_coefficient(0.1 , "sand", "sand")
# %%
# The particles are added at random positions in the given area with the given compacity.
c=0
pbodies = np.asarray([], np.int32)
while c < cmax:
  xp = np.random.uniform(np.array([-lx, -ly]), np.array([lx, ly]))
  if p.n_particles() == 0:
    d = 4*r
  else:
    d = np.min(np.linalg.norm(p.position()-xp[None,:],axis=1))
  if d > 2*(r+eps):
    ri = np.random.uniform(0.8,1.0)*r
    body = p.add_particle(xp, ri, ri**2 * np.pi * rhop,"sand")
    pbodies = np.append(pbodies, body)
  c = np.sum(p.volume())/(h*w)
  print(f"Initialisation %1.1f"%(100*c/cmax) + r'%' + " ready", end="\r")
print('')
# %%
# Time integration
# ----------------
# The numerical parameters are defined given and the initial conditions are written in the output directory.
outf = 25                                           # number of iterations between output files
dt   = 2.5e-5                                       # time step
tEnd =  0.5                                         # final time
t    =  0                                           # initial time
ii   =  0                                           # initial iteration
p.write_mig(outputdir, 0)
# %% 
# Useful functions. 
# The first one moves particles that cross the periodic boundaries accordingly, and the second one allows to measure the force on boundaries.
def periodic_map(w, bodies):
    p.body_position()[bodies,0] = np.remainder(p.body_position()[bodies,0]+3*w/2,w)-w/2

def accumulate(f_contacts, n_divide):
    f_contacts[0] += p.get_boundary_forces("Top")/n_divide
    f_contacts[1] += p.get_boundary_forces("Bottom")/n_divide

tic = time.time()
forces_particles = np.zeros_like(p.velocity())
forces_body = np.zeros_like(p.body_velocity())
forces_body[top_body, 1] = -500 
xold = p.body_position()[0,:].copy()
# %%
# The computational loop can start.
# The external forces given to the particles have to be given at each time step.
# A lambda function is given as after_sub_iter argument so that the forces on the boundary can be computed even if the time interval is split.
while t < tEnd:
    # map the positions of the particles which crossed the periodic boundaries
    periodic_map(w, pbodies)
    # reset the velocity and position of the Top boundary
    p.body_position()[top_body,0] = xold[0]
    p.body_velocity()[top_body, 0] = gamma*h 
    # initialise the vector of the forces on the boundaries
    f_contacts = np.zeros((2,2))
    # solve the particle problem
    time_integration._advance_particles(p,forces_particles,dt,min_nsub=1,contact_tol=1e-6,after_sub_iter=lambda n_divide: accumulate(f_contacts, n_divide), max_nsub=5, fbody=forces_body)
    t += dt
    # Output files writing
    if ii%outf == 0:
        print(f"iteration : {ii} ---- t : {t} / {tEnd}")
        p.write_mig(outputdir, t)
    ii += 1