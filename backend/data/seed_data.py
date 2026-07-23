import bcrypt
from backend.data.database import create_tables, get_connection

clients = [
    ("Ben Ali", "Ahmed", "12345678", "ahmed@email.com", "ahmed", "motdepasse123"),
    ("Trabelsi", "Sarra", "23456789", "sarra@email.com", "sarra", "motdepasse123"),
    ("Gharbi", "Karim", "34567890", "karim@email.com", "karim", "motdepasse123"),
]

# (numero_dossier, index du client dans la liste ci-dessus, statut, remarque)
dossiers = [
    ("DOS-2026-001", 0, "en_cours", "En attente de justificatifs"),
    ("DOS-2026-002", 0, "accepte", "Financement validé"),
    ("DOS-2026-003", 1, "en_attente_documents", "Manque relevé bancaire"),
    ("DOS-2026-004", 2, "refuse", "Revenus insuffisants"),
]


def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


create_tables()
connection = get_connection()
cursor = connection.cursor()

client_ids = []
for nom, prenom, cin, email, login, password in clients:
    cursor.execute(
        "INSERT INTO clients (login, mot_de_passe_hash, nom, prenom, cin, email) VALUES (%s, %s, %s, %s, %s, %s) RETURNING id",
        (login, hash_password(password), nom, prenom, cin, email)
    )
    client_ids.append(cursor.fetchone()[0])

for numero, index_client, statut, remarque in dossiers:
    cursor.execute(
        "INSERT INTO dossiers (numero_dossier, client_id, statut, remarque) VALUES (%s, %s, %s, %s)",
        (numero, client_ids[index_client], statut, remarque)
    )

connection.commit()
connection.close()
print(f"{len(clients)} clients et {len(dossiers)} dossiers ajoutés.")