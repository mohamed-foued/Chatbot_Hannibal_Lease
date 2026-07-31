from backend.data.database import get_connection


def verifier_cin(cin):
    cin = cin.strip()
    if len(cin) != 8 or not cin.isdigit():
        return {"valide": False, "message": "CIN invalide : doit contenir exactement 8 chiffres."}

    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT nom, prenom FROM clients WHERE cin = %s", (cin,))
    row = cursor.fetchone()
    connection.close()

    if row is None:
        return {"valide": False, "message": f"Aucun client trouvé avec le CIN {cin}."}

    return {"valide": True, "message": f"Client trouvé : {row[1]} {row[0]}."}


def consulter_dossier(numero_dossier):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute(
        "SELECT numero_dossier, statut, remarque FROM dossiers WHERE numero_dossier = %s",
        (numero_dossier,)
    )
    row = cursor.fetchone()
    connection.close()

    if row is None:
        return f"Aucun dossier trouvé avec le numéro {numero_dossier}."
    return f"Dossier {row[0]} — Statut : {row[1]} — Remarque : {row[2] or 'Aucune'}"


def dossiers_par_cin(cin):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute(
        "SELECT d.numero_dossier, d.statut, d.remarque "
        "FROM dossiers d "
        "JOIN clients c ON d.client_login = c.login "
        "WHERE c.cin = %s",
        (cin,),
    )
    lignes = cursor.fetchall()
    connection.close()

    if not lignes:
        return "Aucun dossier trouvé pour ce client."

    resultat = "Dossiers trouvés :\n"
    for ligne in lignes:
        resultat += f"- {ligne[0]} — Statut : {ligne[1]} — Remarque : {ligne[2] or 'Aucune'}\n"
    return resultat


def dossiers_par_login(login):
    """Récupère tous les dossiers d'un client connecté (identifié par login)."""
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute(
        "SELECT d.numero_dossier, d.statut, d.remarque "
        "FROM dossiers d "
        "JOIN clients c ON d.client_login = c.login "
        "WHERE c.login = %s",
        (login.strip(),),
    )
    lignes = cursor.fetchall()
    connection.close()

    if not lignes:
        return "Aucun dossier trouvé pour ce client."

    resultat = "Dossiers du client connecté :\n"
    for ligne in lignes:
        resultat += f"- {ligne[0]} — Statut : {ligne[1]} — Remarque : {ligne[2] or 'Aucune'}\n"
    return resultat


def dossier_appartient_a(login, numero_dossier):
    """Vérifie si un dossier appartient au client connecté (par login)."""
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute(
        "SELECT numero_dossier FROM dossiers "
        "WHERE numero_dossier = %s AND client_login = %s",
        (numero_dossier, login.strip()),
    )
    row = cursor.fetchone()
    connection.close()
    return row is not None


def infos_client_par_login(login):
    """Récupère les informations personnelles du client connecté (par login)."""
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute(
        "SELECT login, nom, prenom, cin, email FROM clients WHERE login = %s",
        (login.strip(),)
    )
    row = cursor.fetchone()
    connection.close()

    if row is None:
        return None

    return {
        "login": row[0],
        "nom": row[1],
        "prenom": row[2],
        "cin": row[3],
        "email": row[4],
    }


if __name__ == "__main__":
    print(verifier_cin("12345678"))
    print(verifier_cin("00000000"))
    print(verifier_cin("abc"))
    print(consulter_dossier("DOS-2026-001"))
    print(dossiers_par_login("ahmed"))
