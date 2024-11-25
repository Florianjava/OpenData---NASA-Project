import streamlit as st


import sqlite3
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

# Fonction pour charger la base de données
def load_data(db_path, table_name):
    # Connexion à la base de données
    conn = sqlite3.connect(db_path)
    
    # Charger la table dans un DataFrame
    df = pd.read_sql_query(f"SELECT * FROM {table_name};", conn)
    
    # Fermer la connexion
    conn.close()
    
    return df

# Fonction pour afficher le graphique
def plot_miss_distance(df):
    # Convertir la colonne de temps si nécessaire
    if not pd.api.types.is_datetime64_any_dtype(df['close_approach_date']):
        df['close_approach_date'] = pd.to_datetime(df['close_approach_date'])
    
    # Trier par temps
    df = df.sort_values('close_approach_date')

    # Scatter plot
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.scatter(df['close_approach_date'], df['miss_distance'], alpha=0.7, edgecolors='k')
    ax.set_title("Miss Distance vs Time")
    ax.set_xlabel("Time")
    ax.set_ylabel("Miss Distance")
    ax.grid(True)
    plt.xticks(rotation=45)
    st.pyplot(fig)

# Fonction pour ajouter des filtres interactifs
def filter_data(df):
    st.sidebar.title("Filtres de données")
    
    # Filtres sur la variable "miss_distance"
    min_miss_distance = st.sidebar.number_input("Miss Distance min", min_value=float(df['miss_distance'].min()), max_value=float(df['miss_distance'].max()), value=float(df['miss_distance'].min()))
    max_miss_distance = st.sidebar.number_input("Miss Distance max", min_value=float(df['miss_distance'].min()), max_value=float(df['miss_distance'].max()), value=float(df['miss_distance'].max()))
    
    # Appliquer le filtre
    df_filtered = df[(df['miss_distance'] >= min_miss_distance) & (df['miss_distance'] <= max_miss_distance)]
    
    # Filtres supplémentaires (exemples : champ autre que "miss_distance" et "time")
    # Par exemple, si tu as une colonne "category" dans ta table, tu pourrais ajouter un filtre pour cela :
    if 'category' in df.columns:
        categories = df['category'].unique()
        selected_category = st.sidebar.selectbox("Choisir une catégorie", categories)
        df_filtered = df_filtered[df_filtered['category'] == selected_category]
    
    return df_filtered

# Page Streamlit


def display() : 

    # Charger les données depuis la base de données
    db_path = 'neo.db'  # Remplacer par le chemin vers ta base de données
    table_name = "neo"  # Remplacer par le nom de ta table
    
    # Charger les données
    df = load_data(db_path, table_name)
    
    # Afficher un titre
    st.title("Analyse descriptive des données de la base de données")
    
    # Afficher les premières lignes de la table
    st.write("**Premières lignes des données :**")
    st.dataframe(df.head())

    # Appliquer les filtres
    df_filtered = filter_data(df)

    # Afficher le graphique
    st.write("**Graphique : Miss Distance vs Time**")
    plot_miss_distance(df_filtered)


