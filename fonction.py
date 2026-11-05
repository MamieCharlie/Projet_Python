def charger_donnees(nom_fichier):

    list = []
    erreur_formatage = 0

    with open(nom_fichier, "r") as fichier:

        lignes = fichier.readlines()

        for ligne in lignes[1:]:

            donnees = ligne.strip().split(";")

            if len(donnees) != 5:
                print("Erreur : ligne mal formatée :", ligne)
                erreur_formatage += 1
                continue

            try:
                heure = int(donnees[2].strip())
                consommation = float(donnees[3].strip())
                temperature = float(donnees[4].strip())

            except ValueError:
                print("Ligne ignorée :", ligne.strip())
                erreur_formatage += 1
                continue

            mesure = {
                "Salle": donnees[0].strip(),
                "Jour": donnees[1].strip(),
                "Heure": donnees[2].strip(),
                "Consommation": donnees[3].strip(),
                "Temperature": donnees[4].strip()
            }

            list.append(mesure)
    return list

def normaliser_donnees(mesures):

    for mesure in mesures:
        mesure["Salle"] = mesure["Salle"].strip()
        mesure["Salle"] = mesure["Salle"][0].upper() + mesure["Salle"][1:]

    return mesures

afichier = input("fichier :")
resultat = charger_donnees(afichier)
resultat = normaliser_donnees(resultat)

print(resultat)