from collections import defaultdict
import numpy as np
import time

start = time.time()
exp = 7
size = 10**exp

random = np.random.randint(size//20,size=size//10)
seq = np.arange(size//10,size)
data = np.append(random,seq)

d = defaultdict(int)

for elem in data:
    d[elem] += 1

s = 0
for key in d:
    if d[key] > 3:
        s += d[key]

print(s)
end = time.time()
print("time elapsed: ",end-start)