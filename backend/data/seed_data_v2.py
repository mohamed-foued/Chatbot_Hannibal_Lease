import bcrypt
from backend.data.database import get_connection

# Nouveaux clients à insérer
nouveaux_clients = [
    # (nom, prenom, cin, email, login, password)
    ("Mansouri",  "Leila",   "45678901", "leila.mansouri@email.com",  "leila",   "motdepasse123"),
    ("Chaabane",  "Yassine", "56789012", "yassine.chaabane@email.com","yassine", "motdepasse123"),
    ("Jlassi",    "Rim",     "67890123", "rim.jlassi@email.com",      "rim",     "motdepasse123"),
    ("Hamdi",     "Sofiene", "78901234", "sofiene.hamdi@email.com",   "sofiene", "motdepasse123"),
    ("Belhaj",    "Nadia",   "89012345", "nadia.belhaj@email.com",    "nadia",   "motdepasse123"),
]

# Nouveaux dossiers à insérer
# (numero_dossier, index_client_dans_la_liste, statut, remarque)
nouveaux_dossiers = [
    ("DOS-2026-005", 0, "en_cours",              "En attente de vérification CIN"),
    ("DOS-2026-006", 0, "accepte",               "Dossier complet – véhicule Peugeot 208"),
    ("DOS-2026-007", 1, "en_attente_documents",  "Manque attestation de travail"),
    ("DOS-2026-008", 1, "en_cours",              "Dossier en cours d'étude"),
    ("DOS-2026-009", 2, "accepte",               "Financement accordé – Toyota Yaris"),
    ("DOS-2026-010", 2, "refuse",                "Taux d'endettement trop élevé"),
    ("DOS-2026-011", 3, "en_cours",              "Documents reçus – analyse en cours"),
    ("DOS-2026-012", 4, "en_attente_documents",  "Manque les 3 derniers bulletins de salaire"),
]


def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


def insert_nouveaux_clients_et_dossiers():
    connection = get_connection()
    cursor = connection.cursor()

    client_ids = []
    clients_inseres = 0
    for nom, prenom, cin, email, login, password in nouveaux_clients:
        try:
            cursor.execute(
                """
                INSERT INTO clients (login, mot_de_passe_hash, nom, prenom, cin, email)
                VALUES (%s, %s, %s, %s, %s, %s)
                RETURNING id
                """,
                (login, hash_password(password), nom, prenom, cin, email),
            )
            client_ids.append(cursor.fetchone()[0])
            clients_inseres += 1
            print(f"  [OK] Client insere : {prenom} {nom} (login: {login})")

        except Exception as e:
            print(f"  [IGNORE] Client ignore ({login}) - probablement deja existant : {e}")
            # Recuperer l'id existant pour lier les dossiers quand meme
            connection.rollback()
            cursor.execute("SELECT id FROM clients WHERE login = %s", (login,))
            row = cursor.fetchone()
            client_ids.append(row[0] if row else None)

    dossiers_inseres = 0
    for numero, index_client, statut, remarque in nouveaux_dossiers:
        client_id = client_ids[index_client] if index_client < len(client_ids) else None
        if client_id is None:
            print(f"  [IGNORE] Dossier {numero} ignore - client_id introuvable")
            continue
        try:
            cursor.execute(
                """
                INSERT INTO dossiers (numero_dossier, client_id, statut, remarque)
                VALUES (%s, %s, %s, %s)
                """,
                (numero, client_id, statut, remarque),
            )
            dossiers_inseres += 1
            print(f"  [OK] Dossier insere : {numero} (statut: {statut})")
        except Exception as e:
            print(f"  [IGNORE] Dossier {numero} ignore - probablement deja existant : {e}")
            connection.rollback()

    connection.commit()
    connection.close()
    print(f"\n[TERMINE] {clients_inseres} client(s) et {dossiers_inseres} dossier(s) ajoutes.")


if __name__ == "__main__":
    print("[DEBUT] Insertion des nouvelles donnees de test...\n")
    insert_nouveaux_clients_et_dossiers()
