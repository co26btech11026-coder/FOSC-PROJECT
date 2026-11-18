# test_profiles.py
import numpy as np

# Dictionary containing overhauled, high-speed test profiles
TEST_PROFILES = {
    'a': {
        'pos': np.array([[5.6, 0.0, 0.0]]),
        'vel': np.array([[12.0, 0.0, 0.0]]), # High speed to cleanly hit and clamp against the wall
        'desc': "Wall Boundary Clamping",
        'slider': 1
    },
    'b': {
        # Positioned right at the 0.8 attraction threshold to watch them snap and collide elastically
        'pos': np.array([[-0.8, 0.0, 0.0], [0.8, 0.0, 0.0]]),
        'vel': np.array([[8.0, 0.0, 0.0], [-8.0, 0.0, 0.0]]), 
        'desc': "Mid-Air Elastic Collision",
        'slider': 2
    },
    'c': {
        'pos': np.array([
            [0.0, 0.0, 0.0],
            [0.0, 0.0, 0.0],
            [0.0, 0.0, 0.0]
        ]),
        'vel': np.array([
            [0.0, 0.0, 0.0],
            [0.0, 0.0, 0.0],
            [0.0, 0.0, 0.0]
        ]),
        'desc': "Zero-Distance Singularity Overlap Explosion",
        'slider': 3
    },
    'd': {
        # Replaces old test case g, triggered when 'd' is pressed
        'pos': np.array([[5.5, 5.5, 0.0]]),
        'vel': np.array([[10.0, 10.0, 0.00]]),
        'desc': "Corner Simultaneous Multi-Wall Bounce",
        'slider': 1
    }
}
