import pdfplumber
import csv
import os

DOCUMENTS_DIR = os.path.dirname(os.path.abspath(__file__))

def extraire_texte_pdf(nom_fichier):
    """Extracte tout le texte à partir d'un fichier
    pdf et retourne le en un seul string"""

    chemin = os.path.join(DOCUMENTS_DIR,nom_fichier)
    texte_complet = ""

    with pdfplumber.open(chemin) as pdf :
        for page in pdf.pages :
            texte_page = page.extract_text()
            if texte_page :
                texte_complet += texte_page + "\n"
    
    return texte_complet


def charger_catalogue_csv():
    """Charge le catalogue des véhicules depuis
     un fichier CSV et renvoie une liste de dictionnaires."""

    chemin = os.path.join(DOCUMENTS_DIR,"automobile_tn_master_catalog.csv")
    voitures = []

    with open(chemin,"r", encoding="utf-8") as fichier :
        lecteur = csv.DictReader(fichier)

        for ligne in lecteur :
            voitures.append(ligne)

    return voitures


def recherher_voiture(marque=None, budget_max=None):
    """Recherche la voiture selon la marque et/ou le budget
    maximal."""

    voitures = charger_catalogue_csv()
    resultats = []

    for voiture in voitures :
        prix = int(voiture["Prix (Price TND)"])

        if marque and marque.lower() not in voiture["Marque (Brand)"].lower() :
            continue
        if budget_max and prix > budget_max :
            continue
        resultats.append(voiture)
    
    return voitures


def formater_resultats_voitures(resultats):
    """Met en forme une liste de véhicules en une chaîne 
    de caractères lisible par l'IA."""

    if not resultats :
        return "Aucune voiture trouvée avec ces critères"

    lignes = []

    for v in resultats :
        ligne = (
            f"- {v['Marque (Brand)']} {v['Modèle (Model)']} "
            f"({v['Version / Finition']}) — "
            f"{v['Énergie (Fuel Type)']} — "
            f"{v['Puissance Fiscale']} — "
            f"{int(v['Prix (Price TND)']):,} TND"
        )  
        lignes.append(ligne)
    
    return "\n".join(lignes) 


if __name__=="__main__":
    print("=== Test PDF ===")
    texte = extraire_texte_pdf("Leasing en Tunisie _ Hannibal Lease.pdf")
    print(texte[:500])

    print("\n=== Test recherche voiture ===")
    resultats = recherher_voiture(marque="Toyota",budget_max=100000)
    print(formater_resultats_voitures(resultats))