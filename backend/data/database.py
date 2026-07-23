import time
import psycopg2
from backend.config import DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD


def get_connection(retries: int = 3, delay: int = 5):
    """
    Etablit une connexion PostgreSQL avec timeout et retry automatique.
    Utile quand Supabase sort de pause (cold start ~30s).
    """
    last_error = None
    for attempt in range(1, retries + 1):
        try:
            return psycopg2.connect(
                host=DB_HOST,
                port=DB_PORT,
                dbname=DB_NAME,
                user=DB_USER,
                password=DB_PASSWORD,
                sslmode="require",
                connect_timeout=10,
            )
        except psycopg2.OperationalError as e:
            last_error = e
            print(f"[DB] Tentative {attempt}/{retries} echouee : {e}")
            if attempt < retries:
                print(f"[DB] Nouvelle tentative dans {delay}s... (verifiez que le projet Supabase n'est pas en pause)")
                time.sleep(delay)
    raise ConnectionError(
        f"Impossible de se connecter a la base de donnees apres {retries} tentatives.\n"
        f"Verifiez que le projet Supabase est actif sur https://app.supabase.com\n"
        f"Derniere erreur : {last_error}"
    )


def create_tables():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS clients (
            id SERIAL PRIMARY KEY,
            login TEXT UNIQUE NOT NULL,
            mot_de_passe_hash TEXT NOT NULL,
            nom TEXT NOT NULL,
            prenom TEXT NOT NULL,
            cin TEXT NOT NULL UNIQUE,
            email TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS dossiers (
            id SERIAL PRIMARY KEY,
            numero_dossier TEXT NOT NULL UNIQUE,
            client_id INTEGER NOT NULL,
            statut TEXT NOT NULL DEFAULT 'en_cours',
            remarque TEXT,
            FOREIGN KEY (client_id) REFERENCES clients (id)
        )
    """)

    connection.commit()
    connection.close()
    print("Tables créées (ou déjà existantes).")

if __name__ == "__main__":
    create_tables()