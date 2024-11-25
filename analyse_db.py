import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

# Connexion à la base de données
conn = sqlite3.connect('neo.db')

# Création du curseur pour exécuter des requêtes
cursor = conn.cursor()

# Récupérer et afficher les tables disponibles
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()
print("Tables disponibles :", tables)

# Exploration d'une table (remplacez 'table_name' par une table réelle)
table_name = "neo"  # Changez selon votre base
cursor.execute(f"SELECT * FROM {table_name} LIMIT 10;")  # Récupère les 10 premières lignes
rows = cursor.fetchall()
print(f"Contenu de la table {table_name} :")
for row in rows:
    print(row)

df = pd.read_sql_query("SELECT * FROM neo;", conn)



print(len(df))
print(df.head())

if not pd.api.types.is_datetime64_any_dtype(df['close_approach_date']):
    df['close_approach_date'] = pd.to_datetime(df['close_approach_date'])

# Trier par temps
df = df.sort_values('close_approach_date')
df = df[df["absolute_magnitude"]>25]
df = df[df["relative_velocity"]>30]

# Scatter plot
plt.figure(figsize=(10, 6))
plt.scatter(df['close_approach_date'], df['miss_distance'], alpha=0.7, edgecolors='k')
plt.title("Miss Distance vs Time")
plt.xlabel("Time")
plt.ylabel("Miss Distance")
plt.grid(True)
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()



# Fermer la connexion
conn.close()
