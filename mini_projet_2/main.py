import sys
import pandas as pd
import numpy as np 


def main():
    """Charge le CSV nettoyé et affiche un aperçu des données."""

    if len(sys.argv) < 2:
        print("Usage : python main.py <fichier.csv>")
        return

    try:
        df = pd.read_csv(sys.argv[1], sep=";")
    except FileNotFoundError:
        print("Erreur : fichier introuvable :", sys.argv[1])
        return
    except pd.errors.EmptyDataError:
        print("Erreur : le fichier est vide :", sys.argv[1])
        return
    if df.empty:
        print("Aucune mesure dans le fichier :", sys.argv[1])
        return

    print("--- APERCU DES 5 PREMIERES LIGNES ---")
    print(df.head())

    print("\nNombre de lignes :", len(df))
    print("Nombre de colonnes :", df.shape[1])
    print("Colonnes :", list(df.columns))
    print("\nTypes des variables :")
    print(df.dtypes)


    print("\n--- STATISTIQUES GLOBALES ---")

    conso = df["Consommation"].to_numpy()

    moyenne = np.mean(conso)
    ecarts = conso - moyenne

    print("Moyenne :", round(moyenne, 2))
    print("Minimum :", np.min(conso))
    print("Maximum :", np.max(conso))
    print("Ecart-type (ddof=0) :", round(np.std(conso), 2))
    print("Ecart a la moyenne des 5 premieres mesures :", np.round(ecarts[:5], 2))


    print("\n--- STATISTIQUES PAR SALLE ---")

    stats = df.groupby("Salle").agg(
        Nombre=("Consommation", "count"),
        Moyenne=("Consommation", "mean"),
        Minimum=("Consommation", "min"),
        Maximum=("Consommation", "max"),
        Ecart_type=("Consommation", "std"),
        Temperature_moyenne=("Temperature", "mean"),
    )

    print(stats.round(2))

    stats.reset_index().to_csv("statistiques_salles.csv", sep=";", index=False)
    print("\nFichier statistiques_salles.csv cree.")

main()