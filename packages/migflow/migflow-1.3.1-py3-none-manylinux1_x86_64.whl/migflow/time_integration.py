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
def _advance_particles(particles, f:np.ndarray, dt:float, min_nsub:int,contact_tol:float,max_nsub:int=None,after_sub_iter:callable=None,n_divide:int=None, fbody:np.ndarray=None):
    """Contact solver for the grains

    Args:
        particles: particles structure
        f: external forces on particles
        dt: time step
        min_nsub: minimal nsub for the particles iterations
        contact_tol: tolerance for the contact solver
        after_sub_iter: callback to execute once a sub iteration has been made
    """
    # Compute free velocities of the grains
    v = particles.velocity()
    if f is None:
        f = np.zeros_like(v)
    if fbody is None:
        fbody = np.zeros_like(particles.body_velocity())
    # Estimation of the solid sub-time steps
    nsub = 1
    vmax = 0
    if particles.r() is not None and particles.r().size != 0:
        ftot = f + fbody[particles.particle_body()]
        vn = v + ftot*dt*np.amax(particles.body_invert_mass())
        vmax = np.max(np.linalg.norm(vn,axis=1))
        nonzero = particles.r()>0
        if np.sum(nonzero) > 0:
            nsub = int(max(min_nsub, int(np.ceil((vmax * dt * 8)/min(particles.r()[nonzero])))))
    if max_nsub is None:
      max_nsub = min_nsub*2
    print("NSUB", nsub,"VMAX",vmax, "VMAX * dt", vmax * dt, "r", min(particles.r()) if (particles.r() is not None and particles.r().size !=0) else 0 )
    if n_divide is None:
      n_divide = nsub
    else:
      n_divide *= nsub
    #If time step was split too many times, ignore the convergence and move the grains
    if min_nsub > max_nsub:
      for i in range(nsub) :
        particles.iterate(dt/nsub, f, fbody, tol=contact_tol,force_motion=1)
        if after_sub_iter :
            after_sub_iter(n_divide)
      return
    # For each sub-time step solve contacts (do NLGS iterations) and move the grains
    for i in range(nsub) :
        if not particles.iterate(dt/nsub, f, fbody, tol=contact_tol):
          print("Splitting time-step")
          _advance_particles(particles,f,dt/nsub,min_nsub*2,contact_tol/2,max_nsub/nsub,after_sub_iter=after_sub_iter,n_divide=n_divide, fbody=fbody)
          print("Convergence reached for subinvervals")
        else :
            if after_sub_iter :
                after_sub_iter(n_divide)

def predictor_corrector_iterate(fluid, particles, dt:float, min_nsub:int=1, contact_tol:float=1e-8, external_particles_forces:np.ndarray=None, alpha:float=0.5,after_sub_iter:callable=None,max_nsub:int=None,check_residual_norm:float=-1) :
    """Predictor-corrector scheme to solve fluid and grains.

    Args:
        fluid: fluid structure
        particles: particles structure
        dt: time step
        min_nsub: minimal nsub for the particles iterations
        contact_tol: tolerance for the contact solver
        external_particles_forces: external forces applied on the particles
        alpha: parametre of the predictor-corrector scheme [alpha*f(n)+(1-alpha)*f(n+1)]
        after_sub_iter: callback to execute once a sub iteration has been made
        max_split: maximum number of times the time step can be further split if convergence is not reached
        check_residual_norm : check if the fluid solver has converged to the specified norm
    """
    fluid.move_particles(particles.position(), particles.velocity(), particles.contact_forces())
    particles.save_state()
    if external_particles_forces is None:
        external_particles_forces = np.zeros_like(particles.velocity())
    # Copy the fluid solution of the previous time step before computing the prediction
    sf0 = np.copy(fluid.solution())
    # Predictor
    #
    # Compute the fluid solution and keep a copy of this solution and the forces applied by the fluid on the grains
    fluid.implicit_euler(dt,check_residual_norm)
    sf1 = np.copy(fluid.solution())
    f0 = np.copy(fluid.compute_node_force(dt))+external_particles_forces
    _advance_particles(particles,f0,dt,min_nsub,contact_tol,max_nsub=max_nsub)
    # Keep same contact forces and positions while giving to the fluid the predicted solid velocities to compute the correction
    fluid.particle_velocity()[:] = particles.velocity()
    # Corrector
    #
    # Compute the fluid solution from the previous time-step one using the predicted solid velocities in the fluid-grain interaction force
    fluid.solution()[:] = sf0
    fluid.implicit_euler(dt, check_residual_norm)
    # Fluid solution is a weighted average of the predicted one and the corrected one.
    # The alpha parametre is the weight
    fluid.solution()[:] = (alpha*fluid.solution()+(1-alpha)*sf1)
    f1 = np.copy(fluid.compute_node_force(dt))+external_particles_forces
    # For two fluids flows, advance the concentration field with the fluid velocity.
    # The number of sub-time steps for the advection is automatically computed.
    if fluid.n_fluids() == 2 :
        fluid.advance_concentration(dt)
    # Reset solid velocities
    particles.restore_state()
    _advance_particles(particles,(alpha*f0+(1-alpha)*f1),dt,min_nsub,contact_tol,after_sub_iter=after_sub_iter,max_nsub=max_nsub)
    # Give to the fluid the solid information

def iterate(fluid, particles, dt:float, min_nsub:int=1, contact_tol:float=1e-8, external_particles_forces:np.ndarray=None, fixed_grains:bool=False, after_sub_iter:callable=None,max_nsub:int=None,check_residual_norm:float=-1, use_predictor_corrector:bool=True) :
    """Migflow solver: the solver type depends on the fluid and particles given as arguments.

    Args:
        fluid: fluid structure
        particles: particles structure
        dt: time step
        min_nsub: minimal nsub for the particles iterations
        contact_tol: tolerance for the contact solver
        external_particles_forces: vector of external forces applied on the particles
        fixed_grains: boolean variable specifying if the grains are fixed in the fluid
        after_sub_iter: callback to execute once a sub iteration has been made
        max_nsub: maximum number of times the time step can be further split if conergence is not reached
        check_residual_norm : check if the fluid solver has converged to the specified norm
        use_predictor_corrector : boolean variable specifying if the predictor-corrector scheme is used
    Raises:
        ValueError: fluid and particles cannot be both None
        ValueError: external_particles_forces must have shape (number of particles,dimension)
    """
    if particles is None and fluid is None:
        raise ValueError("fluid and particles are both None: not possible to iterate!")
    if particles is not None and external_particles_forces is not None:
        if external_particles_forces.shape!=(particles.n_particles(),particles.dim()):
            raise ValueError("external_particles_forces must have shape (number of particles,dimension!")
    if (particles is None or particles.r() is None or particles.r().size == 0) and fluid is not None:
        fluid.implicit_euler(dt, check_residual_norm)
        # For two fluids flows, advance the concentration field with the fluid velocity.
        # The number of sub-time steps for the advection is automatically computed.
        if fluid.n_fluids() == 2 :
            fluid.advance_concentration(dt)
    if particles is not None and fluid is None:
        _advance_particles(particles,external_particles_forces,dt,min_nsub,contact_tol,after_sub_iter=after_sub_iter,max_nsub=max_nsub)
    if fluid is not None and particles is not None and particles.r() is not None and particles.r().size !=0:
        if fixed_grains:
            fluid.move_particles(particles.position(), particles.velocity(),-fluid.compute_node_force(dt))
            fluid.implicit_euler(dt, check_residual_norm)
            if fluid.n_fluids() == 2 :
                fluid.advance_concentration(dt)
        else:
            if use_predictor_corrector:
                predictor_corrector_iterate(fluid,particles,dt,min_nsub,contact_tol,external_particles_forces,
                    after_sub_iter=after_sub_iter,max_nsub=max_nsub,check_residual_norm=check_residual_norm)
            else:
                fluid.move_particles(particles.position(), particles.velocity(), particles.contact_forces())
                fluid.implicit_euler(dt,check_residual_norm)
                f0 = fluid.compute_node_force(dt)+external_particles_forces
                _advance_particles(particles,f0,dt,min_nsub,contact_tol,max_nsub=max_nsub)
                if fluid.n_fluids() == 2 :
                    fluid.advance_concentration(dt)
