# coding=utf-8
import numpy as np
import os
from sys import stdout, argv

exe_path = "./SelfConsistent_MF/main.py"
result_path = "./result.csv"
out_path = "./out.csv"
procs = eval(argv[1])
N = 30
delta = 0.001  # 加入一个微扰，防止停留在0上

# tprime_list=np.linspace(0.1,0.4,N)
# U_list=np.linspace(0,5,N)
tprime_list = [0.3]
U_list = np.linspace(1, 4, 100)
dm0 = 0.1
recycle_path = "./recycle.txt"

fp = open(out_path, 'w')
print('U,tprime,dm,', file=fp)
fp.close()

fp = open(recycle_path, 'w')
print('these input (U,tprime) met error, you should calculate them by hand', file=fp)
print('corresponding values of dm are replaced by ###### in out.csv', file=fp)
fp.close()

for U in U_list:
    for tprime in tprime_list:
        print()
        print(f'>>>>>>>>>>>>>>>>  Start calculating for U = {
              U}, tprime = {tprime}  <<<<<<<<<<<<<<<<<')
        stdout.flush()
        # exit_code = os.system(f"mpirun -n {procs} --mca btl '^openib' python {exe_path} {tprime} {U} {dm0+delta}")
        exit_code = os.system(
            f"mpirun -n {procs} python {exe_path} {tprime} {U} {dm0+delta}")
        if exit_code == 0:
            fp = open(result_path, 'r')
            content = fp.read().split(',')
            dm0 = eval(content[1])
            fp.close()
            os.system(f'echo "{U},{tprime},{dm0}," >>{out_path}')
        else:
            os.system(f'echo "{U},{tprime}," >>{recycle_path}')
            os.system(f'echo "{U},{tprime},######," >>{out_path}')
