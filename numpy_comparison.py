import numpy as np
import time

n = int(input("Enter number of particles: "))

k = 15
x0 = 0.8

pos = np.random.rand(n,2)*10.0

force = np.zeros((n,2))
start = time.perf_counter()
for i in range(n):

    dx = pos[i,0] - pos[i+1:,0]
    dy = pos[i,1] - pos[i+1:,1]
    x = np.sqrt(dx**2 + dy**2)
    fx = k*dx*(x-x0)/x
    fy = k*dy*(x-x0)/x


    force[i,0] += np.sum(fx)
    force[i,1] += np.sum(fy)

    force[i+1:,0] -= fx
    force[i+1:,1] -= fy

end = time.perf_counter()   
elapsed = end - start

sumx = np.sum(force[:,0])
sumy = np.sum(force[:,1])

memory = pos.nbytes + force.nbytes

print("time Elapsed:",elapsed)
print("total force in x direction :",sumx)
print("total force in y direction :",sumy) 
print("Memory :",memory)
