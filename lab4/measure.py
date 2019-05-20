

import matplotlib.pyplot as plt
plt.plot([1,4,8,16,32],[1,4,8,16,32], 'b-')
ogtime = 84.002
speedup = []
speedup.append(1)
speedup.append(ogtime/48.253)
speedup.append(ogtime/31.098)
speedup.append(ogtime/21.842)
speedup.append(ogtime/17.866)
speedup.append(ogtime/16.374)
#[84.002,48.253,31.098,21.842,17.866, 16.374 ]
plt.plot([1,2,4,8,16,32],speedup, 'r-')
plt.axis([0, 33, 0, 33])
plt.show()
plt.savefig("nplot.png")
