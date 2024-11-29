import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

# Connexion à la base de données
conn = sqlite3.connect('donky.db')

# Création du curseur pour exécuter des requêtes
cursor = conn.cursor()

# Récupérer et afficher les tables disponibles
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()
print("Tables disponibles :", tables)



# Exploration d'une table (remplacez 'table_name' par une table réelle)
table_name = "climate"  # Changez selon votre base    # ID KIND eventTme   --> CME / etc (= les evenements)
#table_name = "linked_climate"    # ID event1 ID event 2 ==> pour lier évènements
#table_name = "flare"    # evt FLR --> heure de debut / peak / fin       class type      sourceLocation     activeRegionNum
#table_name  = "geomagnetic"   # evt GST    --> kpId    observedTime    kpIndex     source
#table_name = "coronal_analyse"   # evt CME     --> id    isMostAccurate     latitude    longitude     halfAngle    speed    type
#table_name = "coronal_impact"   # evt CME    -->  id  isGlancingBlow     location   arrivalTime
cursor.execute(f"SELECT * FROM {table_name} LIMIT 10;")  # Récupère les 10 premières lignes
rows = cursor.fetchall()
print(f"Contenu de la table {table_name} :")
for row in rows:
    print(row)

df = pd.read_sql_query("""SELECT * FROM geomagnetic 
""", conn)


print(df.head(100))
#toto()

df = pd.read_sql_query("""SELECT * FROM coronal_analyse 
""", conn)


print(df.head(100))

toto()



df = pd.read_sql_query("""SELECT id, COUNT(*) AS cnt 
FROM coronal_impact AS t1 
GROUP BY id;
""", conn)
print(len(df))

print(df.head(100))

df = pd.read_sql_query("""SELECT id, COUNT(*) AS cnt 
FROM coronal_analyse AS t1 
GROUP BY id;
""", conn)

print(len(df))
print(df.head(100))








# Fermer la connexion
conn.close()
