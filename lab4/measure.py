

import matplotlib.pyplot as plt
plt.plot([1,4,8,16,32],[1,4,8,16,32], 'b-')
ogtime = 90.332
speedup = []
speedup.append(1)
speedup.append(ogtime/51.208)
speedup.append(ogtime/32.285)
speedup.append(ogtime/22.050)
speedup.append(ogtime/18.340)
speedup.append(ogtime/16.727)
#[84.002,48.253,31.098,21.842,17.866, 16.374 ]
plt.plot([1,2,4,8,16,32],speedup, 'r-')
plt.axis([0, 33, 0, 33])
plt.ylabel("Speedup")
plt.xlabel("#Cores")
plt.show()
plt.savefig("problem1aplot.png")
