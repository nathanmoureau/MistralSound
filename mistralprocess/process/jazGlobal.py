import numpy as np


def normalisation(Intensite, n=True, afficherIm=False, seuil=0.1):
    if n:
        Imin, Imax = np.min(Intensite), np.max(Intensite)
        if Imax - Imin != 0:
            Intensite = (Intensite - Imin) / (Imax - Imin)
        else:
            Intensite = np.zeros_like(Intensite)

    # Im = np.mean(concatenated_intensite)
    Im = np.true_divide(Intensite.sum(), (Intensite >= seuil).sum())

    if afficherIm:
        print(f"Valeur moyenne Im : {Im:.4f}")

    return Im
