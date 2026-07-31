import bcrypt
from backend.data.database import create_tables, get_connection

# (login, mot_de_passe, nom, prenom, cin, email)  — login est la clé primaire
clients = [
    ("ahmed", "motdepasse123", "Ben Ali", "Ahmed", "12345678", "ahmed@email.com"),
    ("sarra", "motdepasse123", "Trabelsi", "Sarra", "23456789", "sarra@email.com"),
    ("karim", "motdepasse123", "Gharbi", "Karim", "34567890", "karim@email.com"),
]

# (numero_dossier, login du client, statut, remarque)
dossiers = [
    ("DOS-2026-001", "ahmed", "en_cours", "En attente de justificatifs"),
    ("DOS-2026-002", "ahmed", "accepte", "Financement validé"),
    ("DOS-2026-003", "sarra", "en_attente_documents", "Manque relevé bancaire"),
    ("DOS-2026-004", "karim", "refuse", "Revenus insuffisants"),
]


def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


create_tables()
connection = get_connection()
cursor = connection.cursor()

for login, password, nom, prenom, cin, email in clients:
    cursor.execute(
        """
        INSERT INTO clients (login, mot_de_passe_hash, nom, prenom, cin, email)
        VALUES (%s, %s, %s, %s, %s, %s)
        ON CONFLICT (login) DO NOTHING
        """,
        (login, hash_password(password), nom, prenom, cin, email)
    )

for numero, login, statut, remarque in dossiers:
    cursor.execute(
        """
        INSERT INTO dossiers (numero_dossier, client_login, statut, remarque)
        VALUES (%s, %s, %s, %s)
        ON CONFLICT (numero_dossier) DO NOTHING
        """,
        (numero, login, statut, remarque)
    )

connection.commit()
connection.close()
print(f"{len(clients)} clients et {len(dossiers)} dossiers ajoutés (login = clé).")
