import fonctions

def main():

    # Demander le nom du fichier à charger
    nom_fichier = input("Entrez le nom du fichier : ")

    # Charger les données
    mesures = fonctions.charger_donnees(nom_fichier)

    # Vérifier que le fichier existe
    if mesures is None:
        return

    # Normaliser les noms des salles
    mesures = fonctions.normaliser_salle(mesures)

    # Initialiser la variable pour conserver les anomalies
    anomalies = []

    # Boucle du menu
    choix = 0

    while choix != 7:

        print("\n===== DONNEES ENERGETIQUES =====")
        print("1. Afficher les mesures")
        print("2. Afficher les salles")
        print("3. Rechercher une salle")
        print("4. Afficher les statistiques")
        print("5. Rechercher les anomalies")
        print("6. Sauvegarder les donnees nettoyees")
        print("7. Quitter")

        choix = input("\nVotre choix : ")

        # Vérifier le choix de l'utilisateur
        if choix == "1":

            # Afficher toutes les mesures
            for mesure in mesures:
                print(mesure)

        elif choix == "2":

            # Afficher les salles sans doublons
            salles = []

            for mesure in mesures:
                if mesure["Salle"] not in salles:
                    salles.append(mesure["Salle"])

            print("\n--- LISTE DES SALLES ---")

            for salle in salles:
                print(salle)

        elif choix == "3":

            # Rechercher une salle
            fonctions.afficher_salle(mesures)

        elif choix == "4":

            # Afficher les statistiques
            fonctions.calculer_statistiques(mesures)

        elif choix == "5":

            # Rechercher les anomalies
            anomalies = fonctions.detecter_anomalie(mesures)

        elif choix == "6":

            # Sauvegarder les donnees sans anomalies
            fonctions.sauvegarder_donnees(mesures, anomalies)

        elif choix == "7":

            print("Fermeture du programme. Au revoir !")

        else:

            print("Erreur : veuillez choisir un nombre entre 1 et 7.")

# Lancement du programme
main()