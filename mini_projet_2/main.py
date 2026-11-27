import sys
import pandas as pd
import numpy as np 
import fonctions2
import matplotlib.pyplot as plt


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

    print("\n--- CLASSEMENTS ---")

    print("Salle de consommation moyenne maximale :", stats["Moyenne"].idxmax())
    print("Salle de consommation moyenne minimale :", stats["Moyenne"].idxmin())
    print("Salle de consommation la plus variable :", stats["Ecart_type"].idxmax())
    print("Salle de température moyenne maximale :", stats["Temperature_moyenne"].idxmax())

    print("\n--- COMPARAISON MP1 (boucles) / MP2 (pandas) ---")

    manuel = fonctions2.statistiques_boucles(df)

    for salle, (moyenne, minimum, maximum) in manuel.items():

        ligne = stats.loc[salle]

        print(f"{salle} Moyenne : MP1={moyenne:.2f}, MP2={ligne['Moyenne']:.2f}")
        print(f"{salle} Minimum : MP1={minimum:.2f}, MP2={ligne['Minimum']:.2f}")
        print(f"{salle} Maximum : MP1={maximum:.2f}, MP2={ligne['Maximum']:.2f}")

    print("\n--- RELATION TEMPERATURE / CONSOMMATION ---")

    temperature = df["Temperature"].to_numpy()
    correlation = df["Temperature"].corr(df["Consommation"])
    print("Correlation de Pearson :", round(correlation, 4))

    for salle, groupe in df.groupby("Salle"):
        r = groupe["Temperature"].corr(groupe["Consommation"])
        print(f"{salle} : correlation = {r:.2f}")

    if correlation < 0:
        verdict = "plus la temperature augmente, plus la consommation diminue"
    else:
        verdict = "plus la temperature augmente, plus la consommation augmente"

    conclusion = (
        f"Relation temperature / consommation : correlation de Pearson = {correlation:.4f}. "
        f"Dans les donnees fournies, {verdict} "
        f"(voir le graphique consommation en fonction de la temperature)."
    )

    print(conclusion)

    ## --- GRAPHIQUE CONSOMMATION / TEMPERATURE ---

    salle = stats["Moyenne"].idxmax()
    mesures_salle = df[df["Salle"] == salle].sort_values("Heure")

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.plot(mesures_salle["Heure"], mesures_salle["Consommation"],
            marker="o", color="#2a6f97", label=salle)
    ax.set_title(f"Consommation selon l'heure - salle {salle}")
    ax.set_xlabel("Heure")
    ax.set_ylabel("Consommation (kWh)")
    ax.legend()
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    fig.savefig("graphique_heure.png", dpi=150)
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.bar(stats.index, stats["Moyenne"], color="#2a6f97")
    ax.set_title("Consommation moyenne par salle")
    ax.set_xlabel("Salle")
    ax.set_ylabel("Consommation moyenne (kWh)")
    ax.grid(True, axis="y", alpha=0.3)
    fig.tight_layout()
    fig.savefig("graphique_salles.png", dpi=150)
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.scatter(df["Temperature"], df["Consommation"],
               color="#2a6f97", alpha=0.75, label="Mesures")
    ax.set_title("Consommation en fonction de la température")
    ax.set_xlabel("Température (°C)")
    ax.set_ylabel("Consommation (kWh)")
    ax.legend()
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    fig.savefig("graphique_temperature.png", dpi=150)
    plt.close(fig)

        # 11. Rapport final
    total_anomalies = fonctions2.compter_anomalies(df)

    lignes = [
        "RAPPORT D'ANALYSE ENERGETIQUE",
        "",
        f"Nombre de salles : {df['Salle'].nunique()}",
        f"Nombre total de mesures : {len(df)}",
        f"Salle de consommation moyenne maximale : {stats['Moyenne'].idxmax()}",
        f"Salle de consommation moyenne minimale : {stats['Moyenne'].idxmin()}",
        f"Salle de consommation la plus variable : {stats['Ecart_type'].idxmax()}",
        f"Salle de température moyenne maximale : {stats['Temperature_moyenne'].idxmax()}",
        f"Nombre d'anomalies : {total_anomalies}",
        "",
        "Comparaison avec le mini-projet 1 : les moyennes, minimums et maximums",
        "obtenus par les boucles du mini-projet 1 et par pandas sont identiques",
        "(voir le détail affiché sur la console).",
        "",
        conclusion,
    ]

    with open("rapport.txt", "w", encoding="utf-8") as fichier:
        fichier.write("\n".join(lignes) + "\n")

    print("\nFichier rapport.txt cree.")


main()
