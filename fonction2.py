# Faire plusieurs fonctions plutôt qu'une seule qui fait tout

def charger_donnees(nom_fichier):
# Ouverture et lecture du fichier
    try: 
        with open(nom_fichier, "r") as fichier:
                lignes = fichier.readlines()
    
    except FileNotFoundError:
            print("Erreur : le fichier n'existe pas.")
            return None
    return lignes
     
def normaliser_salle(mesures):
    for mesure in mesures:
            mesure["Salle"] = mesure["Salle"].strip()
            mesure["Salle"] = mesure["Salle"][0].upper() + mesure["Salle"][1:]
    
    return mesure


def afficher_salle():
    return

def rechercher_salle():
    return
print
def calculer_statistiques():
    return

def detecter_anomalie():
    return
def sauvegarder_donnee():
    return

nom_fichier = input("Fichier:")
charger_donnees(nom_fichier)