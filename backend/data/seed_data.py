from database import get_connection

connection = get_connection()
cursor = connection.cursor()

cursor.execute(
    "INSERT INTO clients (nom, prenom, cin, email) VALUES (?, ?, ?, ?)",
    ("Ben Ali", "Ahmed", "12345678", "ahmed@email.com")
)

client_id = cursor.lastrowid

cursor.execute(
    "INSERT INTO dossiers (numero_dossier, client_id, statut, remarque) VALUES (?, ?, ?, ?)",
    ("DOS-2026-001", client_id, "en_cours", "En attente de justificatifs")
)

connection.commit()
connection.close()
print("Données de test ajoutées")

