import os
from pathlib import Path
from dotenv import dotenv_values

PROJECT_ROOT = Path(__file__).resolve().parent.parent
BACKEND_ENV = Path(__file__).resolve().parent / ".env"
ROOT_ENV = PROJECT_ROOT / ".env"


def load_env_file(path: Path) -> bool:
    if not path.exists():
        return False

    try:
        values = dotenv_values(path)
    except UnicodeDecodeError:
        values = dotenv_values(path, encoding="utf-16")
    if not values:
        return False

    for key, value in values.items():
        if value is None or value == "":
            if key == "GROQ_API_KEY":
                print(f"⚠️ {path} contient GROQ_API_KEY mais la valeur est vide")
            continue

        current_value = os.environ.get(key, "")
        if current_value == "":
            os.environ[key] = value

    return True


loaded = False
for dotenv_path in [ROOT_ENV, BACKEND_ENV]:
    if load_env_file(dotenv_path):
        print(f"Chargement des variables d'environnement depuis : {dotenv_path}")
        loaded = True

if not loaded:
    print("Aucun fichier .env chargé. Vérifiez backend/.env ou .env à la racine du projet.")

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
DB_PATH = os.getenv("DB_PATH","leasing.db")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "postgres")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")


print("Clé API chargée : ", "oui" if GROQ_API_KEY else  " API manquante")
print("Chemin de la base de données :", DB_PATH)