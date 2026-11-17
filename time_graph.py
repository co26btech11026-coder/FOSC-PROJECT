
import matplotlib.pyplot as plt
import numpy as np

# x = np.array([50, 100, 200, 500])

# y1 = np.array([0.00004400, 0.00011800, 0.000489000, 0.015054700])
# y2 = np.array([0.001628600, 0.002526199, 0.004676317, 0.015054709])
# y3 = np.array([0.059092400, 0.232335524, 0.822847664, 5.134180265])

x = np.array([50,100,200,500,100000])
y1 = np.array([0.00004400,0.00011800,0.000489000,0.015054700,86.220978000000002])
y2 = np.array([0.001628600, 0.002526199, 0.004676317, 0.015054709,135.1035797999939])
y3 = np.array([0.059092400, 0.232335524, 0.822847664, 5.134180265,200])

plt.figure(figsize=(9, 6))

plt.plot(x, y1, marker='o', linewidth=2, markersize=7, label='C')
plt.plot(x, y2, marker='s', linewidth=2, markersize=7, label='NumPy')
plt.plot(x, y3, marker='^', linewidth=2, markersize=7, label='Python')

plt.title('Execution Time vs Number of Particles', fontsize=15)
plt.xlabel('Number of Particles (N)', fontsize=12)
plt.ylabel('Execution Time (seconds)', fontsize=12)

plt.xticks(x)
plt.grid(True, linestyle='--', alpha=0.5)

plt.legend(title='Programming Language', fontsize=10)

plt.tight_layout()
plt.show()
