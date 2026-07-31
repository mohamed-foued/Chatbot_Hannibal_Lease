import re

from groq import Groq
from backend.config import GROQ_API_KEY
from backend.data.sql_tools import (
    verifier_cin,
    consulter_dossier,
    dossiers_par_cin,
    dossiers_par_login,
    dossier_appartient_a,
    infos_client_par_login,
)
from backend.documents.doc_loader import(
    extraire_texte_pdf,
    recherher_voiture,
    formater_resultats_voitures,
)
from backend.suggestions import suggerer_vehicules


client = Groq(api_key=GROQ_API_KEY)

SYSTEM_PROMPT = """Tu es l'assistant virtuel de Hannibal Lease, une société de leasing en Tunisie.

Règles générales :
- Réponds toujours en français, de façon professionnelle, chaleureuse et concise.
- Base ta réponse UNIQUEMENT sur les informations contextuelles fournies. N'invente jamais un prix, un statut ou une mensualité qui n'est pas dans le contexte.
- Si le contexte indique un refus d'accès, explique-le clairement sans essayer de deviner l'information à sa place.
- Si tu ne sais pas, dis-le honnêtement plutôt que de deviner.
- Ne divulgue jamais d'informations privées (dossier, statut, coordonnées) si le client n'est pas authentifié par login et mot de passe.

Identification du client :
- Le login unique et le mot de passe du client identifient sa fiche dans la base clients.
- Si le contexte contient « Client connecté : » avec un login, l'identité du client est confirmée : tu peux lui donner directement ses informations personnelles (dossier, statut, coordonnées) qui figurent dans le contexte.
- Si le contexte précise que le client n'est PAS connecté, refuse poliment de donner le statut d'un dossier, son contenu ou toute information personnelle, et invite-le à se connecter.
- N'indique jamais les informations d'un autre client : un dossier ou un CIN qui n'appartient pas au login connecté ne doit jamais être divulgué.

Format :
- Pour les prix et montants, utilise le format "XX,XXX TND".
- Pour une liste (véhicules, dossiers, documents), utilise des tirets "- ", un élément par ligne.
- Reste concis : quelques phrases, plus une liste si besoin.
- Ne mentionne jamais explicitement que tu reçois des "informations contextuelles" — parle naturellement.
"""


def detecteur_intention(message):
    """Détecte ce que l'utilisateur demande."""

    msg = message.lower()

    if any(mot in msg for mot in ["cin", "identité", "carte"]) :
        return "verification_cin"
    
    if any(mot in msg for mot in ["dossier", "statut", "dos-"]) :
        return "consultation_dossier"

    if any(mot in msg for mot in ["voiture", "prix", "modèle","marque", "budget", "acheter", "financer", "véhicule"]):
        return "recherche_voiture"

    if any(mot in msg for mot in ["document", "pièce", "fournir","justificatif", "dossier de crédit"]):
        return "documents_requis"                                   
    
    if any(mot in msg for mot in ["leasing", "crédit", "financement","taux", "mensualité", "durée"]):
        return "info_leasing"                                       
    
    return "general"   


def construire_contexte(intention, message, client_login=None):
    """Construit les données de contexte en fonction 
    de l'intention détectée et du client connecté (login)."""

    contexte = ""

    def extraire_cin(texte):
        mots = texte.replace("-", " ").split()
        for mot in mots:
            mot_nettoye = re.sub(r"[^0-9]", "", mot)
            if len(mot_nettoye) == 8 and mot_nettoye.isdigit():
                return mot_nettoye
        return None

    def entete_client(login):
        """Présente le client connecté pour que l'IA sache à qui elle parle."""
        infos = infos_client_par_login(login)
        if infos is None:
            return ""
        return (
            f"Client connecté : login {infos['login']}, "
            f"{infos['prenom']} {infos['nom']}, "
            f"CIN {infos['cin']}, email {infos['email']}.\n\n"
        )

    if intention == "verification_cin" :
        cin = extraire_cin(message)
        if client_login:
            # Le client connecté est identifié : on confirme sa propre identité
            infos = infos_client_par_login(client_login)
            contexte = (
                f"Le client connecté (login {client_login}) est vérifié : "
                f"{infos['prenom']} {infos['nom']}, CIN {infos['cin']}."
                if infos else "Client connecté introuvable en base."
            )
        elif cin :
            resultats = verifier_cin(cin)
            contexte = f"Résultat de la vérification CIN : {resultats['message']}"
        else :
            contexte = "Le client n'a pas fourni de numéro CIN valide (8 chiffres)."

    
    elif intention == "consultation_dossier" :  
        if client_login:
            # Client connecté : ses dossiers sont identifiés par son login
            numero = None
            for mot in message.upper().split():
                if mot.startswith("DOS-"):
                    numero = mot
                    break
            if numero:
                if dossier_appartient_a(client_login, numero):
                    contexte = consulter_dossier(numero)
                else:
                    contexte = (
                        f"Refus d'accès : le dossier {numero} n'appartient pas "
                        f"au client connecté (login {client_login})."
                    )
            else:
                contexte = dossiers_par_login(client_login)
        else :
            contexte = (
                "Le client n'est PAS connecté. Ne divulgue aucun statut de dossier "
                "ni information personnelle tant qu'il ne s'est pas authentifié "
                "par login et mot de passe."
            )

    elif intention == "recherche_voiture":
        nombres = [int(n) for n in re.findall(r'\d+', message.replace(" ", ""))]
        if len(nombres) >= 2:
            contexte = "Suggestions personnalisées :\n" + formater_suggestions(
                suggerer_vehicules(apport=nombres[0], salaire=nombres[1])
            )
        else:
            resultats = recherher_voiture(budget_max=nombres[0] if nombres else None)
            contexte = "Voici les voitures disponibles\n" + formater_resultats_voitures(resultats)

    elif intention == "documents_requis":
        contexte = extraire_texte_pdf("dossier_de_credit_-_liste_des_documents_a_fournir.pdf")

    elif intention == "info_leasing":
        contexte = extraire_texte_pdf("Leasing en Tunisie _ Hannibal Lease.pdf")

    if client_login and contexte:
        contexte = entete_client(client_login) + contexte

    return contexte  



def repondre(message, historique=None, client_login=None):
    """Prend un message de l'utilisateur et renvoie la 
    réponse de l'IA. Le client connecté est identifié par
    son login unique (clé de la table clients)."""

    if historique is None :
        historique = []

    intention = detecteur_intention(message)
    contexte = construire_contexte(intention, message, client_login)
    messages_api = [{"role": "system", "content": SYSTEM_PROMPT}] 


    for msg in historique :
        messages_api.append(msg)
    if contexte :
        contenu_utilisateur = (                               
        f"Contexte fourni par le système :\n{contexte}\n\n"     
        f"Question du client : {message}"
        ) 
    else :
        contenu_utilisateur = message
    messages_api.append({"role": "user", "content": contenu_utilisateur})
    reponse = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=messages_api,
        temperature=0.3,
        max_tokens=1024
        ) 
        
    return reponse.choices[0].message.content
