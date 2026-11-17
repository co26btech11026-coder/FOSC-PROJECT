# physics.py
import numpy as np

def process_physics_frame(positions, velocities, number_of_molecules, k=0.25, mass=1.0, dt=0.01):
    positions = positions[:number_of_molecules]
    velocities = velocities[:number_of_molecules]

    # --- 1. Vectorized Inter-ball Spring Forces ---
    diff = positions[:, np.newaxis, :] - positions[np.newaxis, :, :]
    dist_matrix = np.sqrt(np.sum(diff**2, axis=-1))


    with np.errstate(divide='ignore', invalid='ignore'):
        directions = diff / dist_matrix[:, :, np.newaxis]
        directions[np.isnan(directions)] = 0.0

    rest_length = 0.8
    force_magnitude = -0.5 * k * (dist_matrix - rest_length)
    np.fill_diagonal(force_magnitude, 0.0)

    pairwise_force_vectors = force_magnitude[:, :, np.newaxis] * directions
    net_force = np.sum(pairwise_force_vectors, axis=1)
    accleration = net_force / mass
    
    # --- 2. Update Positions and Velocities via Timestep integration ---
    velocities += accleration * dt
    positions += velocities * dt
    
    # --- 4. Wall Bound Collision Inversions ---
    for dim in range(3):
        mask_max = positions[:, dim] >= 5.8
        positions[mask_max, dim] = 5.8
        velocities[mask_max, dim] *= -1
        
        mask_min = positions[:, dim] <= -5.8
        positions[mask_min, dim] = -5.8
        velocities[mask_min, dim] *= -1

    return positions, velocities
