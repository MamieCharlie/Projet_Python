import csv
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np 


def statistiques_boucles(df):
    """Recalcule moyenne, minimum et maximum par salle à la manière du projet 1."""

    par_salle = {}

    for salle, consommation in zip(df["Salle"], df["Consommation"]):
        par_salle.setdefault(salle, []).append(float(consommation))

    resultat = {}

    for salle, valeurs in par_salle.items():
        resultat[salle] = (
            sum(valeurs) / len(valeurs),
            min(valeurs),
            max(valeurs),
        )

    return resultat

def compter_anomalies(df):
    """Compte les mesures dépassant strictement 1,3 fois la moyenne des autres mesures de la même salle."""

    total = 0

    for _, groupe in df.groupby("Salle"):

        valeurs = groupe["Consommation"].to_numpy(dtype=float)

        if len(valeurs) < 2:
            continue

        for i in range(len(valeurs)):
            autres = np.delete(valeurs, i)
            if valeurs[i] > 1.3 * np.mean(autres):
                total += 1

    return total