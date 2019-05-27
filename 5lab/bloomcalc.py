import numpy as np


n = 10**9#ceil(m / (-k / log(1 - exp(log(p) / k))))
p = 10**(-9)#pow(1 - exp(-k / (m / n)), k)
m = np.ceil((n * np.log(p)) / np.log(1 / pow(2, np.log(2)))) 
k = round((m / n) * np.log(2))

print("n: ",n)
print("p: ",p)
print("m: ",m)
print("k: ",k)