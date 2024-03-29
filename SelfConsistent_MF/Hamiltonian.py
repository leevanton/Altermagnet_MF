from math import cos, exp
from const import *


def Fermi_Distribution(E, mu):
    """费米分布函数"""
    return 1/(exp((E-mu)/T)+1)


def Zero_Distribution(E, mu):
    """零温分布函数"""
    if E <= mu:
        return 1
    else:
        return 0


class Altermagnet_Hubbard():
    """定义哈密顿量"""

    def __init__(self, tprime, U, dm):
        self.tp = tprime*(1+delta)
        self.tm = tprime*(1-delta)
        self.U = U
        self.dm = dm

    def Hk(self, k):
        h = np.zeros([4, 4], dtype='double')
        h[0, 0] = -(2*self.tm*cos(k.dot(a1))+2*self.tp *
                    cos(k.dot(a2))+self.U*self.dm)
        h[1, 1] = -(2*self.tp*cos(k.dot(a1))+2*self.tm *
                    cos(k.dot(a2))-self.U*self.dm)
        h[0, 1] = -2*t*(cos(k[0]*a)+cos(k[1]*a))
        h[1, 0] = h[0, 1]
        h[2, 2] = h[0, 0]+2*self.U*self.dm
        h[3, 3] = h[1, 1]-2*self.U*self.dm
        h[2, 3] = h[0, 1]
        h[3, 2] = h[1, 0]
        return h

    def Eigwv(self, k):
        """求k点的本征值和本征矢量"""
        return np.linalg.eigh(self.Hk(k))

    def Eigw(self, k):
        """求k点的本征值"""
        return np.linalg.eigvalsh(self.Hk(k))
