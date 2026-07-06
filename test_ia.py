from groq import Groq
from backend.config import GROQ_API_KEY

client = Groq(api_key=GROQ_API_KEY)
reponse = client.chat.completions.create(
    model = "llama-3.3-70b-versatile",
    messages= [
        {"role": "system", "content": "Tu es un assistant pour une société de leasing en Tunisie."},
        {"role": "user", "content": "Bonjour, quels documents faut-il pour financer une voiture ?"}
    ]
)

print(reponse.choices[0].message.content)