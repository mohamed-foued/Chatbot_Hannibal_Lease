from database import get_connection

connexion = get_connection()
cursor = connexion.cursor()

cursor.execute("""
    SELECT table_name FROM information_schema.tables
    WHERE table_schema = 'public'
""")
tables = cursor.fetchall()
print("Tables trouvées :", [t[0] for t in tables])

for table in tables:
    nom_table = table[0]
    print(f"\n--- {nom_table} ---")
    cursor.execute(f"SELECT * FROM {nom_table} LIMIT 5")
    for ligne in cursor.fetchall():
        print(ligne)

connexion.close()