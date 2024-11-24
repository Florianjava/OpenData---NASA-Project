import sqlite3

import pandas as pd

# Ouvrir la connexion
conn = sqlite3.connect("donky.db")
cursor = conn.cursor()

#cursor.execute("ALTER TABLE data RENAME TO neo")
#conn.commit()
# Afficher toutes les lignes de la table
query = "SELECT * FROM coronal_impact"
df = pd.read_sql_query(query, conn)
print(df)

# Fermer la connexion
conn.close()

