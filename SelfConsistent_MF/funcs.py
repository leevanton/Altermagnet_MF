from math import pi, sqrt
from Hamiltonian import *
from const import *


def Generate_1BZ():
    BZ = np.zeros([L, L, 2], dtype='double')
    k0x = 0
    k0y = -pi/a
    dk = sqrt(2)*pi/L
    for i in range(L):
        for j in range(L):
            BZ[i, j, 0] = k0x+i*dk
            BZ[i, j, 1] = k0y+j*dk

    return BZ.reshape(L2, 2)


def Density_Equation(mu, dm, klist):
    """数密度的自洽方程"""
    temp = 0
    H = Altermagnet_Hubbard(tprime, U, dm)
    if abs(T) <= eps:
        dis = Zero_Distribution
    else:
        dis = Fermi_Distribution

    for k in klist:
        eigvals = H.Eigw(k)
        for eigval in eigvals:
            temp += dis(eigval, mu)
    return temp/(2*L2)


def Magnetism_Equation(dm, mu, klist):
    """磁化的自洽方程"""
    temp = 0
    H = Altermagnet_Hubbard(tprime, U, dm)
    if abs(T) <= eps:
        dis = Zero_Distribution
    else:
        dis = Fermi_Distribution

    for k in klist:
        eigvals, eigvecs = H.Eigwv(k)
        for i in range(4):
            temp += eigvecs[:, i].transpose()@magnetism@eigvecs[:,
                                                                i]*dis(eigvals[i], mu)

    return temp/(4*L2)
