import bcrypt
from backend.data.database import get_connection

# Nouveaux clients à insérer
# (login, mot_de_passe, nom, prenom, cin, email)  — login est la clé primaire
nouveaux_clients = [
    ("leila",   "motdepasse123", "Mansouri",  "Leila",   "45678901", "leila.mansouri@email.com"),
    ("yassine", "motdepasse123", "Chaabane",  "Yassine", "56789012", "yassine.chaabane@email.com"),
    ("rim",     "motdepasse123", "Jlassi",    "Rim",     "67890123", "rim.jlassi@email.com"),
    ("sofiene", "motdepasse123", "Hamdi",     "Sofiene", "78901234", "sofiene.hamdi@email.com"),
    ("nadia",   "motdepasse123", "Belhaj",    "Nadia",   "89012345", "nadia.belhaj@email.com"),
]

# Nouveaux dossiers à insérer
# (numero_dossier, login du client, statut, remarque)
nouveaux_dossiers = [
    ("DOS-2026-005", "leila",   "en_cours",              "En attente de vérification CIN"),
    ("DOS-2026-006", "leila",   "accepte",               "Dossier complet – véhicule Peugeot 208"),
    ("DOS-2026-007", "yassine", "en_attente_documents",  "Manque attestation de travail"),
    ("DOS-2026-008", "yassine", "en_cours",              "Dossier en cours d'étude"),
    ("DOS-2026-009", "rim",     "accepte",               "Financement accordé – Toyota Yaris"),
    ("DOS-2026-010", "rim",     "refuse",                "Taux d'endettement trop élevé"),
    ("DOS-2026-011", "sofiene", "en_cours",              "Documents reçus – analyse en cours"),
    ("DOS-2026-012", "nadia",   "en_attente_documents",  "Manque les 3 derniers bulletins de salaire"),
]


def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


def insert_nouveaux_clients_et_dossiers():
    connection = get_connection()
    cursor = connection.cursor()

    clients_inseres = 0
    for login, password, nom, prenom, cin, email in nouveaux_clients:
        try:
            cursor.execute(
                """
                INSERT INTO clients (login, mot_de_passe_hash, nom, prenom, cin, email)
                VALUES (%s, %s, %s, %s, %s, %s)
                """,
                (login, hash_password(password), nom, prenom, cin, email),
            )
            clients_inseres += 1
            print(f"  [OK] Client insere : {prenom} {nom} (login: {login})")

        except Exception as e:
            print(f"  [IGNORE] Client ignore ({login}) - probablement deja existant : {e}")
            connection.rollback()

    dossiers_inseres = 0
    for numero, login, statut, remarque in nouveaux_dossiers:
        try:
            cursor.execute(
                "SELECT login FROM clients WHERE login = %s",
                (login,),
            )
            if cursor.fetchone() is None:
                print(f"  [IGNORE] Dossier {numero} ignore - login client introuvable ({login})")
                continue
            cursor.execute(
                """
                INSERT INTO dossiers (numero_dossier, client_login, statut, remarque)
                VALUES (%s, %s, %s, %s)
                """,
                (numero, login, statut, remarque),
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
