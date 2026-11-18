import fonctions

def main():

    nom_fichier = input("Fichier:")
    print("Pouet1")
    mesures = fonctions.charger_donnees(nom_fichier)
    print("pouet2")
    fonctions.afficher_salle(mesures)
    print("pouet3")
    fonctions.calculer_statistiques(mesures)
    print("pouet4")
    anomalie = fonctions.detecter_anomalie(mesures)
    print("pouet5")
    fonctions.sauvegarder_donnees(mesures, anomalie)
    print("pouet6")

    return

main(  )