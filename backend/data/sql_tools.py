from database import get_connection


def verifier_cin(cin):
    cin=cin.strip()
    if len(cin)!=8 or not cin.isdigit() :
        return {"valide": False, "message": "CIN invalide : doit contenir exactement 8 chiffres."}

    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT nom, prenom FROM clients WHERE cin = ?", (cin,))
    row = cursor.fetchone()
    connection.close()

    if row is None :
        return {"valide": False, "message": f"Aucun client trouvé avec le CIN {cin}."}

    return {"valide": True, "message": f"Client trouvé : {row[1]} {row[0]}."}


def consulter_dossier(numero_dossier):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute(
        "SELECT numero_dossier, statut, remarque FROM dossiers WHERE numero_dossier = ?",
        (numero_dossier,)
    )
    row = cursor.fetchone()
    connection.close()

    if row is None :
        return f"Aucun dossier trouvé avec le numéro {numero_dossier}."
    return f"Dossier {row[0]} — Statut : {row[1]} — Remarque : {row[2] or 'Aucune'}"


if __name__ == "__main__":
    print(verifier_cin("12345678"))
    print(verifier_cin("00000000"))
    print(verifier_cin("abc"))
    print(consulter_dossier("DOS-2026-001"))