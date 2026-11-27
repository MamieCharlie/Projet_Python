import sys
import pandas as pd


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

    print("--- APERCU DES 5 PREMIERES LIGNES ---")
    print(df.head())

    print("\nNombre de lignes :", len(df))
    print("Nombre de colonnes :", df.shape[1])
    print("Colonnes :", list(df.columns))
    print("\nTypes des variables :")
    print(df.dtypes)


main()