from pybloom import BloomFilter
import numpy as np
from collections import defaultdict
import time

start = time.time()
exp = 7
size = 10**exp

random = np.random.randint(size//20,size=size//10)
seq = np.arange(size//10,size)
data = np.append(random,seq)

d = defaultdict(int)
f = BloomFilter(capacity=size,error_rate=10**(-exp))

for elem in data:
    if elem in f:
        d[elem] += 1
    else:
        f.add(elem)
s = 0
for key in d:
    if(d[key] > 2):
        s += d[key]

print(s)

end = time.time()
print("Time elapsed: ",end-start)
