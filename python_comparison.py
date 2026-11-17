import numpy as np
import time
import tracemalloc
rng = np.random.default_rng()
n = int(input("enter the number of atoms:"))
k =15
xc = 0.8
tracemalloc.start()
pos = (10.0)*rng.random(size=(n,2))
force =np.zeros((n,2))

start = time.perf_counter()
for i in range (n):
    for j in range(i+1,n):
        dx = pos[i][0] -pos[j][0]
        dy = pos[i][1] -pos[j][1]
        x = (dx**2 + dy**2)**(1/2)    #n*(n-1)/2
        force[i][0] +=k*dx*(x-xc)/x
        force[i][1] +=k*dy*(x-xc)/x

        force[j][0] += -k*dx*(x-xc)/x
        force[j][1] +=-k*dy*(x-xc)/x
end = time.perf_counter()   
current, peak = tracemalloc.get_traced_memory()
tracemalloc.stop()   
sumx =0
sumy =0
for i in range (n):
    sumx += force[i][0]
    sumy += force[i][1]

elasped = end - start
print("time elapsed :" ,elasped)
print("total force in x:" ,sumx)    
print("total force in y:",sumy)    
print("memory:",peak)
