
import numpy as np
import matplotlib.pyplot as plt

# ==========================================================
# 1. System setup
# ==========================================================

N = 35
L = 10.0
dt = 0.01
T = 1000

k = 0.5
rc = 2.0
r0 = 1.5
mass = np.ones(N)

gamma_values = [0.0, 0.05, 0.1, 0.5]

# Steady-state criterion
steady_window = 100       # 100 steps = 1.0 time unit
steady_threshold = 1e-3

# Fixed seed makes the initial state reproducible
rng = np.random.default_rng(42)

# Create one initial state shared by all gamma runs
initial_pos = rng.random((N, 2)) * L
initial_vel = rng.random((N, 2)) * 20.0


# ==========================================================
# 2. Pairwise interactions
# ==========================================================

def pairwise_distances(pos):
    d = pos[:, None, :] - pos[None, :, :]
    dist = np.sqrt(np.sum(d**2, axis=2))

    neighbours = (dist > 0.0) & (dist <= rc)

    return d, dist, neighbours


def pair_forces(pos):
    d, dist, neighbours = pairwise_distances(pos)

    # Unit vectors; avoid division by zero on diagonal
    unit = d / (dist[:, :, None] + 1e-12)

    # Spring force magnitude
    f_mag = -k * (dist - r0) * neighbours

    # Sum contributions from all neighbours
    forces = np.sum(f_mag[:, :, None] * unit, axis=1)

    return forces


def total_forces(pos, vel, gamma):
    spring_force = pair_forces(pos)
    drag_force = -gamma * vel

    return spring_force + drag_force


# ==========================================================
# 3. Reflective walls
# ==========================================================

def walls_reflect(pos, vel):
    # X direction
    left = pos[:, 0] < 0.0
    right = pos[:, 0] > L

    vel[left, 0] *= -1
    vel[right, 0] *= -1

    pos[left, 0] = 0.0
    pos[right, 0] = L

    # Y direction
    bottom = pos[:, 1] < 0.0
    top = pos[:, 1] > L

    vel[bottom, 1] *= -1
    vel[top, 1] *= -1

    pos[bottom, 1] = 0.0
    pos[top, 1] = L

    return pos, vel


# ==========================================================
# 4. Integration
# ==========================================================

def step_smooth(pos, vel, gamma, force_previous):
    if force_previous is None:
        force_previous = total_forces(pos, vel, gamma)

    acceleration_previous = force_previous / mass[:, None]

    # Half-step velocity and position
    vel_half = vel + 0.5 * acceleration_previous * dt
    pos_new = pos + vel_half * dt

    pos_new, vel_half = walls_reflect(pos_new, vel_half)

    # Calculate new force
    force_new = total_forces(pos_new, vel_half, gamma)
    acceleration_new = force_new / mass[:, None]

    # Complete velocity update
    vel_new = vel_half + 0.5 * acceleration_new * dt

    return pos_new, vel_new, force_new


# ==========================================================
# 5. Energy calculations
# ==========================================================

def kinetic_energy(vel):
    return 0.5 * np.sum(mass[:, None] * vel**2)


def potential_energy(pos):
    _, dist, neighbours = pairwise_distances(pos)

    # Pair spring potential
    U_pairs = 0.5 * k * (dist - r0)**2 * neighbours

    # Each pair occurs twice in the symmetric distance matrix
    return 0.5 * np.sum(U_pairs)


def total_energy(pos, vel):
    return kinetic_energy(vel) + potential_energy(pos)


def mean_speed(vel):
    return np.mean(np.sqrt(np.sum(vel**2, axis=1)))


# ==========================================================
# 6. Run one dissipation case
# ==========================================================

def run_simulation(gamma):
    pos = initial_pos.copy()
    vel = initial_vel.copy()

    force = None

    time_values = np.arange(T + 1) * dt

    KE = np.zeros(T + 1)
    PE = np.zeros(T + 1)
    E_total = np.zeros(T + 1)
    heat_lost = np.zeros(T + 1)
    speed_mean = np.zeros(T + 1)

    # Record initial state
    KE[0] = kinetic_energy(vel)
    PE[0] = potential_energy(pos)
    E_total[0] = KE[0] + PE[0]
    speed_mean[0] = mean_speed(vel)

    for step in range(1, T + 1):
        pos, vel, force = step_smooth(pos, vel, gamma, force)

        KE[step] = kinetic_energy(vel)
        PE[step] = potential_energy(pos)
        E_total[step] = KE[step] + PE[step]
        speed_mean[step] = mean_speed(vel)

        # Approximate dissipated energy:
        # H(t) = integral gamma * sum_i(v_i^2) dt
        heat_lost[step] = (
            heat_lost[step - 1]
            + gamma * np.sum(vel**2) * dt
        )

    return {
        "time": time_values,
        "KE": KE,
        "PE": PE,
        "E": E_total,
        "H": heat_lost,
        "mean_speed": speed_mean,
    }


# ==========================================================
# 7. Objective steady-state criterion
# ==========================================================

def find_steady_state(result):
    E = result["E"]
    E0 = E[0]

    # Need a complete window before checking steady state
    for end in range(steady_window, len(E)):
        start = end - steady_window

        window_energy = E[start:end + 1]

        # Maximum variation within this time window,
        # normalized by the initial mechanical energy
        relative_variation = (
            np.max(np.abs(window_energy - window_energy[0]))
            / abs(E0)
        )

        if relative_variation < steady_threshold:
            return result["time"][end]

    return None


# ==========================================================
# 8. Run all gamma values
# ==========================================================

results = {}

for gamma in gamma_values:
    print(f"Running gamma = {gamma} ...")
    results[gamma] = run_simulation(gamma)


# ==========================================================
# 9. Plot K(t), U(t), and E_total(t)
# ==========================================================

fig, axes = plt.subplots(3, 1, figsize=(10, 12), sharex=True)

for gamma, result in results.items():
    axes[0].plot(result["time"], result["KE"], label=f"gamma = {gamma}")
    axes[1].plot(result["time"], result["PE"], label=f"gamma = {gamma}")
    axes[2].plot(result["time"], result["E"], label=f"gamma = {gamma}")

axes[0].set_ylabel("Kinetic Energy K(t)")
axes[1].set_ylabel("Potential Energy U(t)")
axes[2].set_ylabel("Total Energy E(t)")
axes[2].set_xlabel("Time")

axes[0].set_title("Dissipation Experiment: Energy vs Time")

for ax in axes:
    ax.grid(True)
    ax.legend()

plt.tight_layout()
plt.savefig("dissipation_energy_comparison.png", dpi=300)
plt.show()


# ==========================================================
# 10. Plot cumulative heat lost
# ==========================================================

plt.figure(figsize=(10, 6))

for gamma, result in results.items():
    plt.plot(
        result["time"],
        result["H"],
        label=f"gamma = {gamma}"
    )

plt.xlabel("Time")
plt.ylabel("Cumulative dissipated energy H(t)")
plt.title("Cumulative Energy Dissipation")
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.savefig("dissipation_heat_lost.png", dpi=300)
plt.show()


# ==========================================================
# 11. Steady-state summary
# ==========================================================

print("\nSteady-state analysis")
print("---------------------")

for gamma, result in results.items():
    steady_time = find_steady_state(result)

    if steady_time is None:
        print(
            f"gamma = {gamma}: "
            f"steady-state criterion not reached "
            f"within t = {T * dt:.2f}"
        )
    else:
        print(
            f"gamma = {gamma}: "
            f"criterion first satisfied at t = {steady_time:.2f}"
        )

    print(
        f"    Initial energy = {result['E'][0]:.6f}"
    )
    print(
        f"    Final energy   = {result['E'][-1]:.6f}"
    )
    print(
        f"    Final mean speed = {result['mean_speed'][-1]:.6e}"
    )
    print(
        f"    Final heat lost = {result['H'][-1]:.6f}"
    )
