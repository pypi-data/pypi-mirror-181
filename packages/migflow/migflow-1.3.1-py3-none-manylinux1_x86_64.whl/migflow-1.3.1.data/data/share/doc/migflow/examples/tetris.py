# %%
# Tetris
# ==============================================
# This examples illustrates how to define a particle problem in which bodies are tetriminoes falling into a open box.
import os
import time
import shutil
import random
import numpy as np
from migflow import scontact
random.seed(0)

# %%
# First, let's create the output directory.
outputdir = "output-tetris"
shutil.rmtree(outputdir, True)
os.makedirs(outputdir)

# %%
# Piece Generation
# ----------------
# Let's define a function to generate any piece.
def add_piece(p, r, initial_coord):
    """ Creates a tetrimino piece into the MigFlow particle problem.

        Keyword arguments:
        p -- the particle problem
        r -- particle radius
        initial_coord -- initial coordinates of the body
    """
# %%
# Each piece is defined by its mask over a 2x4 rectangular grid.
    models = [
        [[1, 0, 0, 0],
         [1, 1, 1, 0]],

        [[0, 0, 0, 1],
         [0, 1, 1, 1]],

        [[1, 1, 1, 1],
         [0, 0, 0, 0]],

        [[0, 1, 1, 0],
         [0, 1, 1, 0]],

        [[0, 0, 1, 1],
         [0, 1, 1, 0]],

        [[0, 1, 0, 0],
         [1, 1, 1, 0]],

        [[0, 1, 1, 0],
         [0, 0, 1, 1]]
    ]
# %%
# A piece is randomly selected and its position and initial rotation are prescribed.
    piece = random.choice(models)
    omega = 10*np.pi*(-1+2*random.random())
    y, x = np.where(piece)
    x = r*(initial_coord[0]+2*x)
    y = r*(initial_coord[1]+2*y)
# %%
# A body representing the piece is generated. The body is composed of 4 particles.
    R = np.repeat(r, 4)                                     # particles radii
    coord = np.column_stack([x, y])                         # particles coordinates
    body = p.add_particle_body(coord, R, np.pi*R**2*rho)    # create body and particles
    p.body_omega()[body, 0] = omega                         # Set body rotations

# %%
# Particle Problem
# ----------------
# The particle problem based is created, its dimension has to be provided.
p = scontact.ParticleProblem(2)
# %%
# Let's define the particle properties :
g = np.array([0, -9.81])                                    # gravity
rho = 1000                                                  # particle density
r = 0.05                                                    # particle radius
h = 2                                                       # box height
w = 2                                                       # box width
x0 = np.array([-3, 40])                                     # initial position
# %%
# The open box is defined using three segments.
p.add_boundary_segment([-w/2, -h/2], [-w/2,  h/2], "bnd")
p.add_boundary_segment([ w/2,  h/2], [ w/2, -h/2], "bnd")
p.add_boundary_segment([ w/2, -h/2], [-w/2, -h/2], "bnd")
# %%
# To activate the body contact algorithm the fixed contact geometry flag is set to 0.
p.set_fixed_contact_geometry(0)
# %%
# An initial piece is inserted into the domain :
add_piece(p, r, x0)
# %%
# Time integration
# ----------------
# The numerical parameters is given and the initial conditions are written in the output directory.
# number of iterations between output files
outf = 15
dt = 1e-3                                                   # time step
tEnd = 20                                                   # final time
t = 0                                                       # intial time
ii = 0                                                      # initial iteration
p.write_mig(outputdir, t)                                   # write the intial particle problem
tic = time.process_time()                                   # create a timer
# %%
# The computational loop can start.
while t < tEnd:
    forces = g*(np.pi*p.r()**2*rho)                         # external particle forces
    p.iterate(dt, forces, tol=1e-7)                         # Contact solver
    t += dt
    # Output files writing
    if ii%outf == 0:
        p.write_mig(outputdir, t)                           # write the output data
    ii += 1
    # Add a new piece
    if ii%250 == 0:
        add_piece(p, r, x0)                                 # add a piece
    print("%i : %.2g/%.2g (cpu %.6g)" % (ii, t, tEnd, time.process_time() - tic))
