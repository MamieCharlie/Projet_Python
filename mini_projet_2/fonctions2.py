import csv


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