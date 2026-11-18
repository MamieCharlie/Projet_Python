# Faire plusieurs fonctions plutôt qu'une seule qui fait tout

import csv

def charger_donnees(nom_fichier):
# Ouverture et lecture du fichier
    list = []
    
    try:
        with open(nom_fichier, "r") as fichier:
        # Ouverture du fichier
            lignes = fichier.readlines()

            for ligne in lignes[1:]:
            # Parcourt chaque ligne
                donnees = ligne.strip().split(";")
                # Retire les espaces autour des données et split sur le ;

                if len(donnees) != 5:
                # Si il manque une info sur la ligne = ignore la ligne
                    print("Erreur : ligne mal formatée :", ligne)
                    continue

                try:
                   # Vérifie le format des données
                    heure = int(donnees[2].strip())
                    if heure < 0 or heure >= 24:
                        print("Erreur : l'heure doit être comprise entre 0 et 23.")
                        continue
                    consommation = float(donnees[3].strip())
                    temperature = float(donnees[4].strip())

                except ValueError:
                # Si la donnée n'est pas exploitable = ignore la ligne
                    print("Ligne ignorée :", ligne.strip())
                    continue

                mesure = {
                # Stock les données utilisable dans un dictionnaire
                    "Salle": donnees[0].strip(),
                    "Jour": donnees[1].strip(),
                    "Heure": donnees[2].strip(),
                    "Consommation": donnees[3].strip(),
                    "Temperature": donnees[4].strip()
                }

                list.append(mesure)
                # Rajoute le dictionnaire sur la liste
    except FileNotFoundError:
        print("Erreur : le fichier n'existe pas.")
        return None
    return list

     
def normaliser_salle(mesures):
    for mesure in mesures:
            mesure["Salle"] = mesure["Salle"].strip()
            mesure["Salle"] = mesure["Salle"][0].upper() + mesure["Salle"][1:]
    
    return mesures

def afficher_salle(mesures):
    nom_salle = input("Entrez le nom de la salle à rechercher : ")

    salle_trouvee = False

    # Parcourir toutes les mesures
    for mesure in mesures:

        if mesure["Salle"].casefold() == nom_salle.strip().casefold():

            if not salle_trouvee:
                print("\nSalle trouvée :", mesure["Salle"])
                print("--- MESURES ---")
                salle_trouvee = True

            print("Jour :", mesure["Jour"])
            print("Heure :", mesure["Heure"])
            print("Consommation :", mesure["Consommation"])
            print("Température :", mesure["Temperature"])
            print("-------------------")

    # Si aucune salle ne correspond
    if not salle_trouvee:
        print("Erreur : cette salle n'existe pas dans le fichier.")
    return

def calculer_statistiques(mesures):
    nom_salle = input("Entrez le nom de la salle : ")

    consommations = []
    temperatures = []

    # Parcourir les mesures de la salle sélectionnée
    for mesure in mesures:

        if mesure["Salle"].casefold() == nom_salle.strip().casefold():

            consommations.append(float(mesure["Consommation"]))
            temperatures.append(float(mesure["Temperature"]))

    # Vérifier que la salle existe
    if len(consommations) == 0:
        print("Erreur : cette salle n'existe pas ou ne possède aucune mesure.")
        return

    # Calcul des statistiques
    nombre_mesures = len(consommations)

    consommation_moyenne = sum(consommations) / nombre_mesures
    consommation_minimale = min(consommations)
    consommation_maximale = max(consommations)

    temperature_moyenne = sum(temperatures) / nombre_mesures

    # Affichage des résultats
    print("\n--- STATISTIQUES DE LA SALLE", nom_salle, "---")

    print("Nombre de mesures :", nombre_mesures)
    print("Consommation moyenne :", round(consommation_moyenne, 2))
    print("Consommation minimale :", consommation_minimale)
    print("Consommation maximale :", consommation_maximale)
    print("Température moyenne :", round(temperature_moyenne, 2))
    return

def detecter_anomalie(mesures):
    anomalies = []

    # Parcourir chaque mesure
    for mesure in mesures:

        salle = mesure["Salle"]
        consommation = float(mesure["Consommation"])

        consommations_reference = []

        # Récupérer les consommations des autres mesures de la même salle
        for autre_mesure in mesures:

            if autre_mesure is not mesure and autre_mesure["Salle"] == salle:

                consommations_reference.append(
                    float(autre_mesure["Consommation"])
                )

        # Vérifier qu'il existe d'autres mesures pour calculer la moyenne
        if len(consommations_reference) == 0:
            continue

        # Calculer la moyenne de référence
        moyenne_reference = sum(consommations_reference) / len(consommations_reference)

        # Calculer le seuil de 30 %
        seuil = moyenne_reference * 1.30

        # Vérifier si la consommation est anormalement élevée
        if consommation > seuil:

            anomalies.append
            ({
                "Salle": salle,
                "Jour": mesure["Jour"],
                "Heure": mesure["Heure"],
                "Consommation": consommation,
                "Moyenne_reference": moyenne_reference,
                "Seuil": seuil,
                "mesures": mesure
            })

    # Afficher les anomalies
    print("\n--- ANOMALIES DÉTECTÉES ---")

    if len(anomalies) == 0:
        print("Aucune anomalie détectée.")

    else:
        for anomalie in anomalies:

            print("\nSalle :", anomalie["Salle"])
            print("Jour :", anomalie["Jour"])
            print("Heure :", anomalie["Heure"])
            print("Consommation :", anomalie["Consommation"])
            print("Moyenne de référence :", round(anomalie["Moyenne_reference"], 2))
            print("Seuil calculé :", round(anomalie["Seuil"], 2))

    print("\nNombre total d'anomalies :", len(anomalies))

    return anomalies


def sauvegarder_donnees(mesures, anomalies):

    # Ouvrir ou créer le fichier
    with open("consommation_nettoyee.csv", "w", newline="", encoding="utf-8") as fichier:

        ecrivain = csv.writer(fichier, delimiter=";")

        # Écrire les en-têtes
        ecrivain.writerow([
            "Salle",
            "Jour",
            "Heure",
            "Consommation",
            "Temperature"
        ])

        nombre_sauvegarde = 0

        # Parcourir toutes les mesures
        for mesure in mesures:

            anomalie_trouvee = False

            # Vérifier si la mesure est une anomalie
            for anomalie in anomalies:

                if mesure is anomalie["mesure"]:
                    anomalie_trouvee = True
                    break

            # Sauvegarder uniquement les mesures sans anomalie
            if not anomalie_trouvee:

                ecrivain.writerow([
                    mesure["Salle"],
                    mesure["Jour"],
                    mesure["Heure"],
                    mesure["Consommation"],
                    mesure["Temperature"]
                ])

                nombre_sauvegarde += 1

    print("Fichier consommation_nettoyee.csv créé.")
    print("Nombre de mesures sauvegardées :", nombre_sauvegarde)
    
    return

print("je suis dans le fichier fonction")