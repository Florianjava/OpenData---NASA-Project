import streamlit as st


import sqlite3
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns

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
    
    # Filtre sur miss_distance (range slider)
    miss_distance_range = st.sidebar.slider(
        "Distance (min et max)",
        min_value=float(df['miss_distance'].min()),
        max_value=float(df['miss_distance'].max()),
        value=(float(df['miss_distance'].min()), float(df['miss_distance'].max()))
    )
    min_miss_distance, max_miss_distance = miss_distance_range
    df_filtered = df[(df['miss_distance'] >= min_miss_distance) & (df['miss_distance'] <= max_miss_distance)]
    
    # Filtre par checkbox pour is_hazardous
    is_hazardous_filter = st.sidebar.checkbox("Is Hazardous", value=False)
    if is_hazardous_filter:
        df_filtered = df_filtered[df_filtered['is_hazardous'] == True]
    
    # Filtre sur relative_velocity (range slider)
    velocity_range = st.sidebar.slider(
        "Relativ velocity (min  max)",
        min_value=float(df['relative_velocity'].min()),
        max_value=float(df['relative_velocity'].max()),
        value=(float(df['relative_velocity'].min()), float(df['relative_velocity'].max()))
    )
    min_velocity, max_velocity = velocity_range
    df_filtered = df_filtered[(df_filtered['relative_velocity'] >= min_velocity) & (df_filtered['relative_velocity'] <= max_velocity)]
    
    # Filtre sur magnitude (range slider)
    magnitude_range = st.sidebar.slider(
        "Magnitude (min  max)",
        min_value=float(df['absolute_magnitude'].min()),
        max_value=float(df['absolute_magnitude'].max()),
        value=(float(df['absolute_magnitude'].min()), float(df['absolute_magnitude'].max()))
    )
    min_magnitude, max_magnitude = magnitude_range
    df_filtered = df_filtered[(df_filtered['absolute_magnitude'] >= min_magnitude) & (df_filtered['absolute_magnitude'] <= max_magnitude)]
    
    # Filtre sur diamètre (range slider)
    diameter_range = st.sidebar.slider(
        "Diametre (min  max)",
        min_value=float(df['estimated_diameter_min'].min()),
        max_value=float(df['estimated_diameter_max'].max()),
        value=(float(df['estimated_diameter_min'].min()), float(df['estimated_diameter_max'].max()))
    )
    min_diameter, max_diameter = diameter_range
    df_filtered = df_filtered[(df_filtered['estimated_diameter_min'] >= min_diameter) & (df_filtered['estimated_diameter_max'] <= max_diameter)]
    
    return df_filtered

# Page Streamlit

def plot_scatter_and_density(df):
    df['estimated_diameter_avg'] = (df['estimated_diameter_min'] + df['estimated_diameter_max']) / 2

    # Mapping pour renommer les variables
    axis_labels = {
        "absolute_magnitude": "Absolute Magnitude",
        "relative_velocity": "Relative Velocity",
        "miss_distance": "Miss Distance",
        "estimated_diameter_avg": "Estimated Diameter (Avg)"
    }

    # Sélection de la variable pour le graphique de densité
    variable = st.selectbox(
        "Select a variable for the density plot :",
        ["absolute_magnitude", "relative_velocity", "miss_distance", "estimated_diameter_avg"]
    )

    # **1. Scatter plot avec estimation de la densité**
    fig, axes = plt.subplots(1, 2, figsize=(16, 6))
    if not pd.api.types.is_datetime64_any_dtype(df['close_approach_date']):
        df['close_approach_date'] = pd.to_datetime(df['close_approach_date'])
    df = df.sort_values('close_approach_date')

    # Calcul de la densité avec Gaussian KDE
    from scipy.stats import gaussian_kde
    x = df['close_approach_date'].map(lambda x: x.timestamp())  # Convertir en timestamps
    y = df['miss_distance']
    kde = gaussian_kde([x, y])
    density = kde([x, y])

    scatter = axes[0].scatter(
        df['close_approach_date'], df['miss_distance'], c=density, cmap='viridis', alpha=0.7, edgecolors='k'
    )
    axes[0].set_title("Miss Distance vs Time (avec densité)")
    axes[0].set_xlabel("Time")
    axes[0].set_ylabel(axis_labels["miss_distance"])
    axes[0].grid(True)
    axes[0].tick_params(axis='x', rotation=45)
    fig.colorbar(scatter, ax=axes[0], label="Densité")

    # **2. Graphique de densité**
    sns.kdeplot(df[variable], ax=axes[1], fill=True, color="skyblue")
    axes[1].set_title(f"Density of {axis_labels[variable]}")
    axes[1].set_xlabel(axis_labels[variable])
    axes[1].set_ylabel("Density")

    plt.tight_layout()
    st.pyplot(fig)

    # **3. Matrice de corrélation sur un plot séparé**
    st.write("### Correlation matrix between caracteristics")

    corr_fig, axes = plt.subplots(1, 3, figsize=(20, 4))  # Taille ajustée pour éviter l'écrasement
    corr_matrix = df[["absolute_magnitude", "relative_velocity", "miss_distance", "estimated_diameter_avg"]].corr()
    renamed_corr = corr_matrix.rename(columns=axis_labels, index=axis_labels)  # Modifier les noms
    sns.heatmap(renamed_corr, annot=True, cmap="coolwarm", ax=axes[1], cbar_kws={'shrink': 0.8}, fmt=".2f")
    axes[1].set_title("Correlation matrix")
    axes[0].axis("off")
    axes[2].axis("off")
    st.pyplot(corr_fig)





def display() : 

    # Charger les données depuis la base de données
    db_path = 'neo.db'  # Remplacer par le chemin vers ta base de données
    table_name = "neo"  # Remplacer par le nom de ta table
    
    # Charger les données
    df = load_data(db_path, table_name)
    
    # Afficher un titre
    st.title("Asteroids : Near Earth Objects (date, miss distance and caracteristics)")
    
    # Afficher les premières lignes de la table
    #st.write("**Premières lignes des données :**")
    #st.dataframe(df.head())

    # Appliquer les filtres
    df_filtered = filter_data(df)

    # Afficher le graphique
    st.write("**Graphique : Miss Distance vs Time**")
    plot_scatter_and_density(df_filtered)
    #plot_miss_distance(df_filtered)


