import numpy as np


def getIrel(Intensite, i1, i2):
    """
    Intensite : float array
    i1 : int
    i2 : int
    Renvoie le ratio Intensite[i1]/ Intensite[i2].
    Renvoie np.inf si Intensite[i2] = 0
    """
    I1 = Intensite[i1]
    I2 = Intensite[i2]
    if I2 == 0:
        Irel = np.inf
    else:
        Irel = I1 / I2
    return Irel


def norminf(x: float) -> float:
    """
    fonction de normalisation : [0; +inf] -> [0; 1]
    """
    v = 1 - np.exp(-x)
    return v * (v >= 0)
