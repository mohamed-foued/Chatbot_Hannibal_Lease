from backend.documents.doc_loader import charger_catalogue_csv

TAUX_ANNUEL = 0.105
RATIO_SALAIRE_MAX = 0.35
RATIO_APPORT_MIN = 0.10


def calculer_mensualite(montant_finance, duree_mois, taux_annuel=TAUX_ANNUEL):
    if montant_finance <= 0:
        return 0
    taux_mensuel = taux_annuel / 12
    return montant_finance * taux_mensuel / (1 - (1 + taux_mensuel) ** (-duree_mois))


def evaluer_vehicule(voiture, apport, salaire, duree_mois):
    prix = int(voiture["Prix (Price TND)"])
    apport_minimum = prix * RATIO_APPORT_MIN
    apport_utilise = min(apport, prix)
    montant_finance = max(0, prix - apport_utilise)
    mensualite = calculer_mensualite(montant_finance, duree_mois)
    mensualite_max = salaire * RATIO_SALAIRE_MAX
    abordable = apport >= apport_minimum and mensualite <= mensualite_max

    return {
        **voiture,
        "apport_utilise": round(apport_utilise, 2),
        "montant_finance": round(montant_finance, 2),
        "mensualite": round(mensualite, 2),
        "mensualite_max": round(mensualite_max, 2),
        "abordable": abordable,
    }


def suggerer_vehicules(apport, salaire, duree_mois=48, nombre_resultats=3):
    catalogue = charger_catalogue_csv()
    evalues = []
    for voiture in catalogue:
        try:
            evalues.append(evaluer_vehicule(voiture, apport, salaire, duree_mois))
        except (ValueError, KeyError):
            continue

    abordables = [v for v in evalues if v["abordable"]]
    a_trier = abordables if abordables else evalues
    a_trier.sort(key=lambda v: v["mensualite"])
    return a_trier[:nombre_resultats]


def formater_suggestions(suggestions):
    if not suggestions:
        return "Aucun vehicule trouve pour ce profil."
    lignes = []
    for v in suggestions:
        statut = "Abordable" if v["abordable"] else "Au-dessus du budget recommande"
        lignes.append(
            f"- {v['Marque (Brand)']} {v['Modele (Model)']} ({v['Version / Finition']}) - "
            f"Prix : {int(v['Prix (Price TND)']):,} TND - "
            f"Mensualite estimee : {v['mensualite']:,.0f} TND/mois - {statut}"
        )
    return "\n".join(lignes)
