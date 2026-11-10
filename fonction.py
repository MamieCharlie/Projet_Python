def charger_donnees(nom_fichier):
# Chargement des données + Vérification 
    list = []
    erreur_formatage = 0
    
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
                    erreur_formatage += 1
                    continue

                try:
                   # Vérifie le format des données
                    heure = int(donnees[2].strip())
                    if heure < 0 or heure >= 24:
                        print("Erreur : l'heure doit être comprise entre 0 et 23.")
                        erreur_formatage += 1
                        continue
                    consommation = float(donnees[3].strip())
                    temperature = float(donnees[4].strip())

                except ValueError:
                # Si la donnée n'est pas exploitable = ignore la ligne
                    print("Ligne ignorée :", ligne.strip())
                    erreur_formatage += 1
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
        return None, erreur_formatage
    return list, erreur_formatage

def normaliser_donnees(mesures):
# Normaliser le nom des salles

    for mesure in mesures:
        mesure["Salle"] = mesure["Salle"].strip()
        mesure["Salle"] = mesure["Salle"][0].upper() + mesure["Salle"][1:]

    return mesures

def compter_salles(mesures):
# Compter les salles différentes
    salles = set()

    for mesure in mesures:
        salles.add(mesure["Salle"])

    return len(salles)



afichier = input("fichier :")
resultat, erreur = charger_donnees(afichier)
if resultat is not None:
    resultat = normaliser_donnees(resultat)
    nombre_salle = compter_salles(resultat)

print(resultat)
print("Il y a", nombre_salle, "salles différentes")