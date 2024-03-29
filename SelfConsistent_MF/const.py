import numpy as np
import sys

L: int = 200
L2: int = L*L
eps = 1e-6
mu_range = 3.

a: int = 1
a1 = np.array([a, a])
a2 = np.array([a, -a])

flag: bool = True
iter_max: int = 500

T = 0
U = 3.5
t = 1.
tprime = 0.3
delta = 0.2
n = 1.
dm0 = 0.1
mu = None

magnetism = np.diag([1, -1, -1, 1])

# -----------从命令行读取输入参数----------
arglist = sys.argv
if len(arglist) == 4:
    tprime = eval(arglist[1])
    U = eval(arglist[2])
    dm0 = eval(arglist[3])
