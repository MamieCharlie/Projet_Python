# Faire plusieurs fonctions plutôt qu'une seule qui fait tout

import csv

COLONNES = ("Salle", "Jour", "Heure", "Consommation", "Temperature")

def charger_donnees(nom_fichier):

    # Initialisation des variables
    mesures = []
    nombre_lignes_lues = 0
    nombre_lignes_valides = 0
    nombre_lignes_corrigees = 0
    nombre_lignes_ignorees = 0
    salles = []

    try:

        # Ouverture et lecture du fichier
        with open(nom_fichier, "r", encoding="utf-8") as fichier:

            lignes = fichier.readlines()

            # Parcourir chaque ligne sans prendre l'en-tête
            for ligne in lignes[1:]:

                nombre_lignes_lues += 1

                donnees = ligne.strip().split(";")

                # Vérifier le nombre de colonnes
                if len(donnees) != 5:

                    print("Erreur : ligne mal formatée :", ligne.strip())
                    nombre_lignes_ignorees += 1
                    continue

                try:

                    # Vérifier et convertir les données
                    heure = int(donnees[2].strip())

                    if heure < 0 or heure >= 24:
                        print("Erreur : heure incorrecte :", ligne.strip())
                        nombre_lignes_ignorees += 1
                        continue

                    consommation = float(donnees[3].strip())
                    if consommation < 0:
                        print("Erreur : consommation négative :", ligne.strip())
                        nombre_lignes_ignorees += 1
                        continue
                    temperature = float(donnees[4].strip())

                except ValueError:

                    print("Erreur : données non exploitables :", ligne.strip())
                    nombre_lignes_ignorees += 1
                    continue

                # Vérifier si la ligne nécessite une correction
                salle = donnees[0].strip()
                jour = donnees[1].strip()

                corrigee = False

                if salle != donnees[0] or jour != donnees[1]:
                    corrigee = True

                # Normaliser le nom de la salle
                if salle:
                    nouvelle_salle = salle[0].upper() + salle[1:]

                    if nouvelle_salle != salle:
                        corrigee = True

                    salle = nouvelle_salle

                # Construire le dictionnaire
                mesure = {
                    "Salle": salle,
                    "Jour": jour,
                    "Heure": heure,
                    "Consommation": consommation,
                    "Temperature": temperature
                }

                mesures.append(mesure)

                # Compter les lignes valides ou corrigées
                if corrigee:
                    nombre_lignes_corrigees += 1
                else:
                    nombre_lignes_valides += 1

                # Ajouter les salles sans doublons
                if salle and salle not in salles:
                    salles.append(salle)

    except FileNotFoundError:

        print("Erreur : le fichier est inexistant.")
        return None

    # Affichage du diagnostic
    print("\n===== CONTROLE DES DONNEES =====")

    print("Nombre de lignes lues :", nombre_lignes_lues)
    print("Nombre de lignes valides :", nombre_lignes_valides)
    print("Nombre de lignes corrigées :", nombre_lignes_corrigees)
    print("Nombre de lignes ignorées :", nombre_lignes_ignorees)
    print("Nombre de salles détectées :", len(salles))

    print("\n===== FIN DU CONTROLE =====")

    return mesures

     
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
        print("Erreur : cette salle est inexistante pas dans le fichier.")
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

            anomalies.append({
                "Salle": salle,
                "Jour": mesure["Jour"],
                "Heure": mesure["Heure"],
                "Consommation": consommation,
                "Moyenne_reference": moyenne_reference,
                "Seuil": seuil,
                "mesure": mesure
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
        ecrivain.writerow(COLONNES)

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

    print("Fichier consommation_nettoyee.csv cree.")
    print("Nombre de mesures sauvegardées :", nombre_sauvegarde)
    
    return