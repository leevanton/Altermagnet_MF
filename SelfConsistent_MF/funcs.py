from math import pi, sqrt
from Hamiltonian import *
from const import *


def Generate_1BZ():
    K1 = np.array([0, -pi/a])
    K2 = np.array([-pi/a, 0])
    Kvec = np.array([pi/a, pi/a])
    edge = np.linspace(K1, K2, L)
    BZ = np.array([np.linspace(edge[i], edge[i]+Kvec, L) for i in range(L)])

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
