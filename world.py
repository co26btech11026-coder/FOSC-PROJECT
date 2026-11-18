# main.py
from vpython import *
import numpy as np
import tkinter as tk
from physics import process_physics_frame
from test_profiles import TEST_PROFILES
from graph import EnergyTracker

MAX_CAPACITY = 100
balls = []
rng = np.random.default_rng()
is_re_adjust_count = False
n = 20  
root = tk.Tk()

is_testing_mode = False
test_timer_countdown = 0.0
TEST_DURATION_LIMIT = 60.0  

is_graph_view_active = False
graph_view_timer = 0.0
GRAPH_VIEW_LIMIT = 60.0

min_val, max_val = -5.8, 5.8
vmin, vmax = -2.5, 2.5
dt = 0.01
sim_time = 0.0
k_constant = 0.25

screen_width = root.winfo_screenwidth()
scene = canvas(title='''<script>document.body.style.backgroundColor = "lightblue"; </script>'<div style="text-align: center; font-family: sans-serif;">''<h2>MOLECULAR SIMULATION - SPACE BOUNDS</h2>''</div>''', width=screen_width-30, height=600, background=color.black)
timestamp_label = label(pos=vector(-15, 8, 0), text="Time: 0.00s", box=False, height=20, color=color.white)
count_label = label(pos=vector(15, 8, 0), text=f"Balls: {n}", box=False, height=20, color=color.white)
status_banner = label(pos=vector(0, 8, 0), text="State: Standard Execution Mode", box=True, height=20, color=color.blue, background=color.yellow)

hud_text = (
    "<b>[SIMULATION KEYBINDING INTERACTION MATRIX]</b>\n"
    "Press <b>'a'</b>: Test Case 1 - Wall Boundary Clamping\n"
    "Press <b>'b'</b>: Test Case 2 - Mid-Air Elastic Collision\n"
    "Press <b>'c'</b>: Test Case 3 - Zero-Distance Singularity Explosion\n"
    "Press <b>'d'</b>: Test Case 4 - Corner Simultaneous Multi-Wall Bounce\n"
    "Press <b>'e'</b>: Freeze View and Inspect System Energy Graphs (1 Min)\n"
    "Press <b>'r'</b>: Manual Forced Reset to Standard Simulation State\n"
)
scene.caption = hud_text

for _ in range(MAX_CAPACITY):
    new_ball = sphere(pos=vector(0, 0, 0), texture=textures.metal, radius=0.2, color=color.white)
    new_ball.visible = False
    balls.append(new_ball)

bounded_pos = np.zeros((MAX_CAPACITY, 3))
bounded_vel = np.zeros((MAX_CAPACITY, 3))

tracker = EnergyTracker()

def set_simulation_visibility(visible_state):
    for idx in range(n):
        balls[idx].visible = visible_state
    container_box_top.visible = visible_state
    container_box_bottom.visible = visible_state
    container_box_back.visible = visible_state
    container_box_left.visible = visible_state
    container_box_right.visible = visible_state

def initialize_simulation(target_n, testing_mode=False):
    global n, bounded_pos, bounded_vel, is_re_adjust_count, sim_time
    is_re_adjust_count = True
    n = target_n
    
    sim_time = 0.0
    tracker.reset_graph()
    timestamp_label.text = "Time: 0.00s"
    
    if not testing_mode:
        for i in range(n):
            while True:
                candidate_pos = (max_val - min_val) * rng.random(3) + min_val
                if i == 0:
                    bounded_pos[i] = candidate_pos
                    break
                else:
                    distances = np.sqrt(np.sum((bounded_pos[:i] - candidate_pos) ** 2, axis=1))
                    if np.all(distances >= 0.5):
                        bounded_pos[i] = candidate_pos
                        break
                        
        eps = np.finfo(float).eps
        nonzero_random = (1.0 - eps) * rng.uniform(eps, 1.0, size=(n, 3))
        bounded_vel[:n] = (vmax - vmin) * nonzero_random + vmin
    
    for idx in range(MAX_CAPACITY):
        if idx < n:
            balls[idx].visible = True
            balls[idx].color = color.white  
            # FIXED AXIS INDEXING: Unpacking specific X, Y, Z float matrix positions explicitly
            balls[idx].pos = vector(float(bounded_pos[idx][0]), float(bounded_pos[idx][1]), float(bounded_pos[idx][2]))
        else:
            balls[idx].visible = False
            
    count_label.text = f"Balls: {n}"
    is_re_adjust_count = False

def inject_test_profile(custom_pos, custom_vel, description_text):
    global n, bounded_pos, bounded_vel, is_re_adjust_count, sim_time, is_testing_mode, test_timer_countdown
    is_re_adjust_count = True
    sim_time = 0.0
    tracker.reset_graph()
    
    is_testing_mode = True
    test_timer_countdown = TEST_DURATION_LIMIT
    status_banner.text = f"TESTING: {description_text} (Time Left: {test_timer_countdown:.1f}s)"
    
    n = len(custom_pos)
    bounded_pos[:n] = custom_pos
    bounded_vel[:n] = custom_vel
    
    for idx in range(MAX_CAPACITY):
        if idx < n:
            balls[idx].visible = True
            balls[idx].color = color.white  
            # FIXED AXIS INDEXING: Unpacking specific X, Y, Z float matrix positions explicitly
            balls[idx].pos = vector(float(bounded_pos[idx][0]), float(bounded_pos[idx][1]), float(bounded_pos[idx][2]))
        else:
            balls[idx].visible = False
            
    count_label.text = f"Balls: {n}"
    is_re_adjust_count = False

scene.append_to_caption("\n<b>Dynamically Adjust Ball Count (Active Anytime):</b> ")
def handle_slider(s):
    if not is_testing_mode and not is_graph_view_active:
        initialize_simulation(int(s.value), testing_mode=is_testing_mode)

ball_slider = slider(min=2, max=MAX_CAPACITY, value=n, bind=handle_slider, step=1)

def handle_keypress(evt):
    global is_testing_mode, is_graph_view_active, graph_view_timer
    key = evt.key
    
    if is_graph_view_active and key != 'r':
        print("[INPUT BLOCKED]: You cannot switch profiles while viewing graphs! Press 'r' to return.")
        return
        
    if is_testing_mode and key != 'r' and key != 'e':
        return
    
    if key in TEST_PROFILES:
        profile = TEST_PROFILES[key]
        if key == 'd':
            print("\n" + "="*60)
            print("[DIAGNOSTIC EVENT]: Corner bounce profile activated.")
            print("="*60 + "\n")
            
        inject_test_profile(profile['pos'], profile['vel'], profile['desc'])
        ball_slider.value = profile['slider']
        
    elif key == 'e':
        print("\n[DISPLAY SWAP]: Freezing environment timeline to showcase energy profile plots...")
        is_graph_view_active = True
        graph_view_timer = GRAPH_VIEW_LIMIT
        status_banner.text = "ENERGY GRAPH VIEW INTERIM MODAL ACTIVE - PRESS 'r' TO EXIT"
        status_banner.color = color.red
        status_banner.background = color.white
        set_simulation_visibility(False)
        
    elif key == 'r':
        reset_to_standard_state()

def reset_to_standard_state():
    global is_testing_mode, test_timer_countdown, is_graph_view_active, graph_view_timer
    is_testing_mode = False
    test_timer_countdown = 0.0
    is_graph_view_active = False
    graph_view_timer = 0.0
    
    status_banner.text = "State: Standard Execution Mode"
    status_banner.color = color.blue
    status_banner.background = color.yellow
    
    set_simulation_visibility(True)
    initialize_simulation(int(ball_slider.value))

scene.bind('keydown', handle_keypress)

# --- Container Structural Objects ---
container_box_top    = box(pos=vector(0, 6, 0), texture=textures.wood, size=vector(12, 0.1, 12), opacity=1.0)
container_box_bottom = box(pos=vector(0, -6, 0), texture=textures.wood, size=vector(12, 0.1, 12), opacity=1.0)
container_box_back   = box(pos=vector(0, 0, -6), texture=textures.wood, size=vector(12, 12, 0.1), opacity=1.0)
container_box_left   = box(pos=vector(-6, 0, 0), texture=textures.wood, size=vector(0.1, 12, 12), opacity=1.0)
container_box_right  = box(pos=vector(6, 0, 0), texture=textures.wood, size=vector(0.1, 12, 12), opacity=1.0)

initialize_simulation(n)

while True:
    rate(100)
    if is_re_adjust_count:
        continue
        
    if is_graph_view_active:
        graph_view_timer -= dt
        if graph_view_timer <= 0:
            print("[TIMELOCK EXPIRED]: Automatically returning back to simulation viewport...")
            reset_to_standard_state()
        continue
        
    current_n = n
    local_pos = bounded_pos[:current_n].copy()
    local_vel = bounded_vel[:current_n].copy()
    
    sim_time += dt
    timestamp_label.text = f"Time: {sim_time:.2f}s"
    
    if is_testing_mode:
        test_timer_countdown -= dt
        if test_timer_countdown <= 0:
            reset_to_standard_state()
            continue
        else:
            status_banner.text = f"TEST ACTIVE (Resets in: {max(0.0, test_timer_countdown):.1f}s)"
            
    local_pos, local_vel = process_physics_frame(local_pos, local_vel, current_n, k=k_constant, mass=1.0, dt=dt)
    
    tracker.calculate_and_plot(local_pos, local_vel, current_n, k_constant, sim_time)
        
    for i in range(current_n):
        # FIXED DISPLAY RENDER WINDOW: Handled 3D components cleanly inside the loop
        balls[i].pos = vector(float(local_pos[i][0]), float(local_pos[i][1]), float(local_pos[i][2]))
        
    if not is_re_adjust_count and current_n == n:
        bounded_pos[:current_n] = local_pos
        bounded_vel[:current_n] = local_vel
