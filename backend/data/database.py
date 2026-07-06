import sqlite3
from backend.config import DB_PATH


def get_connection():
    connection = sqlite3.connect(DB_PATH)
    connection.execute("PRAGMA foreign_keys = ON")
    return connection


def create_tables():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS  clients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nom TEXT NOT NULL,
            prenom TEXT NOT NULL,
            cin TEXT NOT NULL UNIQUE,
            email TEXT
        )    
    """)



cursor.execute("""
        CREATE TABLE IF NOT EXISTS dossiers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
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
    create_tables