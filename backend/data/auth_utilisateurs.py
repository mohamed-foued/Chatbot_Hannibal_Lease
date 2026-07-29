import re
import bcrypt
from backend.data.database import get_connection


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _hash(password: str) -> str:
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


def _generer_numero_dossier(cursor) -> str:
    """Génère le prochain numéro DOS-YYYY-NNN automatiquement."""
    from datetime import date
    annee = date.today().year
    cursor.execute(
        "SELECT COUNT(*) FROM dossiers WHERE numero_dossier LIKE %s",
        (f"DOS-{annee}-%",)
    )
    n = cursor.fetchone()[0] + 1
    return f"DOS-{annee}-{n:03d}"


# ---------------------------------------------------------------------------
# Inscription (nouveau client)
# ---------------------------------------------------------------------------

def inscrire_client(login: str, mot_de_passe: str,
                    nom: str, prenom: str,
                    cin: str, email: str = "") -> dict:
    """
    Crée un nouveau client dans la table `clients` puis ouvre
    automatiquement un premier dossier dans la table `dossiers`.

    Retourne :
        {"succes": True,  "client_id": int, "numero_dossier": str, "message": str}
        {"succes": False, "message": str}   en cas d'erreur
    """
    # --- validation basique ---
    if not re.fullmatch(r"\d{8}", cin):
        return {"succes": False, "message": "Le CIN doit contenir exactement 8 chiffres."}
    if len(mot_de_passe) < 6:
        return {"succes": False, "message": "Le mot de passe doit comporter au moins 6 caractères."}
    if not login.strip():
        return {"succes": False, "message": "Le login ne peut pas être vide."}

    try:
        connection = get_connection()
        cursor = connection.cursor()

        # Insérer le client
        cursor.execute(
            """
            INSERT INTO clients (login, mot_de_passe_hash, nom, prenom, cin, email)
            VALUES (%s, %s, %s, %s, %s, %s)
            RETURNING id
            """,
            (login.strip(), _hash(mot_de_passe),
             nom.strip(), prenom.strip(),
             cin.strip(), email.strip()),
        )
        client_id = cursor.fetchone()[0]

        # Créer le premier dossier automatiquement
        numero_dossier = _generer_numero_dossier(cursor)
        cursor.execute(
            """
            INSERT INTO dossiers (numero_dossier, client_id, statut, remarque)
            VALUES (%s, %s, %s, %s)
            """,
            (numero_dossier, client_id,
             "en_attente_documents",
             "Nouveau client – dossier en attente de documents."),
        )

        connection.commit()
        connection.close()
        return {
            "succes": True,
            "client_id": client_id,
            "numero_dossier": numero_dossier,
            "message": (
                f"Compte créé avec succès ! "
                f"Votre numéro de dossier est {numero_dossier}."
            ),
        }

    except Exception as e:
        err = str(e)
        if "clients_login_key" in err or "unique" in err.lower():
            if "login" in err:
                return {"succes": False, "message": f"Le login '{login}' est déjà utilisé."}
            if "cin" in err:
                return {"succes": False, "message": f"Le CIN '{cin}' est déjà enregistré."}
        return {"succes": False, "message": f"Erreur lors de l'inscription : {e}"}


# ---------------------------------------------------------------------------
# Connexion (client existant)
# ---------------------------------------------------------------------------

def verifier_login(login: str, mot_de_passe: str) -> dict:
    """
    Vérifie les identifiants d'un client.

    Retourne :
        {"succes": True,  "client_id": int, "nom": str, "prenom": str}
        {"succes": False, "message": str}
    """
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute(
        "SELECT id, mot_de_passe_hash, nom, prenom FROM clients WHERE login = %s",
        (login,)
    )
    ligne = cursor.fetchone()
    connection.close()

    if ligne is None:
        return {"succes": False, "message": "Identifiant introuvable."}

    client_id, hash_stocke, nom, prenom = ligne
    if bcrypt.checkpw(mot_de_passe.encode("utf-8"), hash_stocke.encode("utf-8")):
        return {"succes": True, "client_id": client_id,
                "nom": nom, "prenom": prenom,
                "message": "Connexion réussie."}
    return {"succes": False, "message": "Mot de passe incorrect."}


# ---------------------------------------------------------------------------
# Test rapide
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    print(inscrire_client("test_user", "secret123", "Dupont", "Jean", "11223344", "jean@email.com"))
    print(verifier_login("test_user", "secret123"))
    print(verifier_login("test_user", "mauvais_mdp"))