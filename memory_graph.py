
import matplotlib.pyplot as plt
import numpy as np

x = np.array([50, 100, 200, 500])

y1 = np.array([816, 1616, 3216, 16000])
y2 = np.array([1600, 3200, 6400, 16000])
y3 = np.array([2944, 4544, 7744, 17344])
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
