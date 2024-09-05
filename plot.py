import numpy as np
import matplotlib.pyplot as plt

N = 30
tprime_list = np.linspace(0.1, 0.4, N)
U_list = np.linspace(0, 5, N)
dm = []

with open('out.csv', 'r') as f:
    f.readline()
    for i in range(N*N):
        line = f.readline().split(',')
        dm.append(eval(line[2]))


dm = np.array(dm).reshape(N, N).transpose()

X, Y = np.meshgrid(U_list, tprime_list)

fig = plt.figure(figsize=(6, 4.5))
ax = fig.add_subplot(111)
c = ax.pcolormesh(X, Y, dm, cmap='Blues')
fig.colorbar(c, ax=ax)
ax.set_xlabel('U/t')
ax.set_ylabel('$t\'/t$')
ax.text(0.02, 0.95, 'T=0', transform=ax.transAxes,
        fontsize=10, verticalalignment='top')
ax.text(0.02, 0.88, r'$\delta$=0.2', transform=ax.transAxes,
        fontsize=10, verticalalignment='top')
fig.savefig('dm.png')
plt.show()
