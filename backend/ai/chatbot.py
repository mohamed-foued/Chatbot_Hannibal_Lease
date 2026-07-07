from groq import Groq
from backend.config import GROQ_API_KEY
from backend.data.sql_tools import verifier_cin,consulter_dossier
from backend.documents.doc_loader import(extraire_texte_pdf,recherher_voiture,formater_resultats_voitures)


client = Groq(api_key=GROQ_API_KEY)

SYSTEM_PROMPT = """Tu es l'assistant virtuel de Hannibal Lease,    
une société de leasing en Tunisie.
Règles :
- Réponds toujours en français, de façon professionnelle et concise.
- Si des informations contextuelles sont fournies, base ta réponse UNIQUEMENT sur elles.
- Si tu ne connais pas la réponse, dis-le honnêtement.
- Pour les prix, utilise le format "XX,XXX TND".
- Sois chaleureux et accueillant avec les clients.
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


def construire_contexte(intention,message):
    """Construit les données de contexte en fonction 
    de l'intention détectée."""

    contexte = ""

    if intention == "verification_cin" :
        mots = message.split()
        cin = None 
        for mot in mots :
            if mot.isdigit() and len(mot)==8:
                cin = mot
                break
        if cin :
            resultats = verifier_cin(cin)
            contexte = f"Résultat de la vérification CIN : {resultat['message']}"
        else :
            contexte = "Le client n'a pas fourni de numéro CIN valide (8 chiffres)."

    
    elif intention == "consultation_dossier" :  
        mots = message.upper().split()
        numero = None
        for mot in mots :
            if mot.startswith("DOS-"):
                numero = mot
                break
        if numero :
            contexte = consulter_dossier(numero)
        else :
            contexte = "Le client n'a pas fourni de numéro de dossier (format: DOS-XXXX-XXX)."

    elif intention == "recherche_voiture":  
        resultats = recherher_voiture()
        contexte = "Voici les voitures disponibles\n"+formater_resultats_voitures(resultats)

    elif intention == "documents_requis":
        contexte = extraire_texte_pdf("dossier_de_credit_-_liste_des_documents_a_fournir.pdf")

    elif intention == "info_leasing":
        contexte = extraire_texte_pdf("Leasing en Tunisie _ Hannibal Lease.pdf")

    return contexte  



def repondre(message,historique=None):
    """Prend un message de l'utilisateur et renvoie la 
    réponse de l'IA."""

    if historique is None :
        historique = []

    intention = detecteur_intention(message)
    contexte = construire_contexte(intention,message)
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
            
