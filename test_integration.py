from groq import Groq
from backend.config import GROQ_API_KEY
from backend.data.sql_tools import dossiers_par_login

client = Groq(api_key=GROQ_API_KEY)

# Le client connecté est identifié par son login (clé primaire de la table clients)
login = "ahmed"
info_dossier = dossiers_par_login(login)

question = "Quel est le statut de mon dossier et que dois-je faire maintenant ?"

reponse = client.chat.completions.create(
    model="llama-3.3-70b-versatile",
    messages=[
        {"role": "system", "content": "Tu es un assistant leasing. Réponds uniquement à partir des informations fournies, en français, de façon concise."},
        {"role": "user", "content": f"Informations sur le dossier : {info_dossier}\n\nQuestion du client : {question}"}
    ]
)

print(reponse.choices[0].message.content)
