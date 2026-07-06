import os
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
DB_PATH = os.getenv("DB_PATH","leasing.db")

print("Clé API chargée : ", "oui" if GROQ_API_KEY else  " API manquante")
print("Chemin de la base de données :", DB_PATH)