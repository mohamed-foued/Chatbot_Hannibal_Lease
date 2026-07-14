import bcrypt
from backend.data.database import get_connection


def creer_utilisateur(login,mot_de_passe):
    mot_de_passe_bytes=mot_de_passe.encode("utf-8")
    hash_genere=bcrypt.hashpw(mot_de_passe_bytes,bcrypt.gensalt())
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute(
        "INSERT INTO clients (login, mot_de_passe_hash) VALUES (%s, %s)",
        (login, hash_genere.decode("utf-8"))
        )
    connection.commit()
    connection.close()
    return {"succes": True, "message": f"Utilisateur {login} créé."}

def verifier_login(login, mot_de_passe):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute(
        "SELECT mot_de_passe_hash FROM clients WHERE login = %s",
        (login,)
    )
    ligne = cursor.fetchone()
    connection.close()
    if ligne is None:
        return {"succes": False, "message": "Utilisateur non trouvé."}
    hash_stocke = ligne[0].encode("utf-8")
    mot_de_passe_bytes = mot_de_passe.encode("utf-8")
    if bcrypt.checkpw(mot_de_passe_bytes, hash_stocke):
        return {"succes": True, "message": "Login réussi."}
    else:
        return {"succes": False, "message": "Mot de passe incorrect."}
    

if __name__ == "__main__":
    print(creer_utilisateur("admin", "motdepasse123"))
    print(verifier_login("admin", "motdepasse123"))
    print(verifier_login("admin", "mauvais_mdp"))