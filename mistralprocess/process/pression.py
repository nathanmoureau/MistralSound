def Vtomb(V):
    """
    V : float
    computes pressure in mbar for a given tension.
    See documentation :
    """
    pression = (V - 1) * 0.125 * 0.1
    if pression >= 0:
        return pression
    return 0
