# graph.py
from vpython import *
import numpy as np

class EnergyTracker:
    def __init__(self):
        # Create a dedicated plot canvas below the main window view layout
        self.plot_window = graph(
            title="System Energy Matrix Profiles Over Time",
            xtitle="Elapsed Simulation Time (seconds)",
            ytitle="Energy Quantities (Joules)",
            width=800,
            height=400,
            background=color.black
        )
        
        # Instantiate continuous trace series profiles
        self.ke_curve = gcurve(graph=self.plot_window, color=color.cyan, label="Kinetic Energy (KE)")
        self.pe_curve = gcurve(graph=self.plot_window, color=color.orange, label="Potential Energy (PE)")
        self.me_curve = gcurve(graph=self.plot_window, color=color.white, label="Total Mechanical Energy (ME)")

    def calculate_and_plot(self, positions, velocities, number_of_molecules, k, current_time):
        pos = positions[:number_of_molecules]
        vel = velocities[:number_of_molecules]
        
        # 1. Kinetic Energy calculation matrix: Sum(0.5 * m * v^2) assuming mass=1.0
        ke_total = 0.5 * np.sum(vel**2)
        
        # 2. Pairwise Potential Energy calculation: Inter-molecular Spring Elastic Energy
        diff = pos[:, np.newaxis, :] - pos[np.newaxis, :, :]
        dist_matrix = np.sqrt(np.sum(diff**2, axis=-1))
        
        rest_length = 0.8
        displacement = dist_matrix - rest_length
        
        # Extract lower triangle elements to calculate unique pair interactions once
        i_lower, j_lower = np.tril_indices(number_of_molecules, k=-1)
        pairwise_pe = 0.5 * (0.5 * k * (displacement[i_lower, j_lower]**2))
        pe_total = np.sum(pairwise_pe)
        
        # 3. Combined Total System Mechanical Energy Portfolio
        me_total = ke_total + pe_total
        
        # Update live visual graphics timelines arrays
        self.ke_curve.plot(current_time, ke_total)
        self.pe_curve.plot(current_time, pe_total)
        self.me_curve.plot(current_time, me_total)

    def reset_graph(self):
        """Clears out data arrays from graph curves entirely."""
        self.ke_curve.delete()
        self.pe_curve.delete()
        self.me_curve.delete()
