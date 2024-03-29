# coding=utf-8
from mpi4py import MPI
from time import time
from gc import collect
from scipy.optimize import root_scalar
from functools import partial
from const import *
from funcs import *

# ------------获取各个进程id---------------
comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

# ------------生成1BZ的k点-----------------
if rank == 0:
    start_time = time()
    KPOINTS = Generate_1BZ()
else:
    KPOINTS = None
part = int(L2/size)
KPOINTS = comm.bcast(KPOINTS, root=0)
# 划分任务
if part*size < L2 and part > size:
    part += 1
if rank == size-1:
    KPOINTS = KPOINTS[part*rank:]
else:
    KPOINTS = KPOINTS[part*rank:part*(rank+1)]
collect()

# 把mu的方程写成函数，方便求根时调用


def func_mu(x, dm):
    f = Density_Equation(x, dm, KPOINTS)
    return n-comm.allreduce(f, MPI.SUM)


# -------------开始迭代--------------------
it: int = 0
method = 'brentq'
while flag:
    it += 1
    # 在临界点附近会临界慢化，收敛速度很慢
    if it == iter_max:
        method = 'ridder'
    elif it >= 2*iter_max:
        if rank==0:
            raise Exception("Beyond maximum iteration times!")
        break
    # -------------------用scipy求mu--------------
    f = partial(func_mu, dm=dm0)
    mu = root_scalar(f, method=method, bracket=[-3., 3.], xtol=eps).root
    """scipy.optimize.root_scalar求根方法:
    bisect: 二分法, 可靠但速度慢
    secant: 割线法, 速度快精度低
    newton: 牛顿法, 这里有问题
    brentq/brenth: Brent法, 介于二分法和割线法之间
    ridder: 与割线法类似"""

    mu = comm.bcast(mu, root=0)
    # ------------------求新的dm----------------
    dm_part = Magnetism_Equation(dm0, mu, KPOINTS)
    dm1 = comm.reduce(dm_part, op=MPI.SUM, root=0)
    if rank == 0:
        dm1 = dm1*0.6+dm0*0.4
        # print(f'it = {it}, mu = {mu}, dm = {dm1}')
        # sys.stdout.flush()
        if abs(dm1-dm0) <= eps:
            flag = False
    dm0 = comm.bcast(dm1, root=0)
    flag = comm.bcast(flag, root=0)

# --------------输出结果---------------------
if rank == 0:
    fp = open('result.csv', 'w')
    print(f'{mu:.16f},{dm1:.16f},', file=fp)
    fp.close()

    end_time = time()
    print(f'converged after {it} times iteration and {end_time-start_time} seconds')
    print(f'mu = {mu}, dm = {dm1}')
    print('>>>>>>>>>>>>>>>>>>>>>>>  Iteration finished!  <<<<<<<<<<<<<<<<<<<<<<<<')
