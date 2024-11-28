import streamlit as st
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

def load_data(db_path, table_name):
    conn = sqlite3.connect(db_path)
    df = pd.read_sql_query(f"SELECT * FROM {table_name};", conn)
    conn.close()
    return df

def display():
    # Charger les données
    db_path = 'donky.db'
    table_name = "climate"
    df = load_data(db_path, table_name)
    df["eventTime"] = pd.to_datetime(df["eventTime"])  # Convertir eventTime en datetime

    st.title("Analyse des événements climatiques")

    # Sélectionner les `kind`
    kinds = df["kind"].unique()
    selected_kinds = st.multiselect("Sélectionnez les types d'événements :", kinds, default=kinds)

    # Filtrer les données
    filtered_df = df[df["kind"].isin(selected_kinds)]
    filtered_df["day"] = filtered_df["eventTime"].dt.to_period("D")
    grouped = filtered_df.groupby(["day", "kind"]).size().reset_index(name="count")
    pivot_df = grouped.pivot(index="day", columns="kind", values="count").fillna(0)

    # Ajouter une colonne sur la droite pour les options
    st.sidebar.header("Options d'affichage")
    line_style = st.sidebar.selectbox("Style des lignes :", ["-", "--", "-.", ":"])
    show_grid = st.sidebar.checkbox("Afficher la grille", value=True)
    marker_style = st.sidebar.selectbox("Style des points :", ["o", "s", "D", "^", "x"])
    figsize = st.sidebar.slider("Taille du graphique :", 8, 16, 12)

    # Afficher le graphique
    st.write("**Tendance quotidienne : Nombre d'événements par jour pour chaque type sélectionné**")
    plt.figure(figsize=(figsize, 6))
    for kind in selected_kinds:
        if kind in pivot_df.columns:
            plt.plot(
                pivot_df.index.astype(str),
                pivot_df[kind],
                marker=marker_style,
                linestyle=line_style,
                label=kind
            )

    plt.xticks(rotation=45)
    plt.xlabel("Jour")
    plt.ylabel("Nombre d'événements")
    plt.title("Tendance quotidienne par type d'événement")
    if show_grid:
        plt.grid(True)
    plt.legend(title="Types d'événements")
    st.pyplot(plt)


