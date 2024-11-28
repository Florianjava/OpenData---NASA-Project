import streamlit as st
import sqlite3
import pandas as pd
import plotly.graph_objects as go
import numpy as np
import plotly.express as px


def load_data(db_path, table_name):
    conn = sqlite3.connect(db_path)
    df = pd.read_sql_query(f"SELECT * FROM {table_name};", conn)
    conn.close()
    return df

def convert_coordinates(coord):
    """Convertir une chaîne de coordonnées comme N12E17 en valeurs numériques"""
    direction_lat, direction_lon = coord[0], coord[3]
    lat_deg, lon_deg = int(coord[1:3]), int(coord[4:6])
    
    lat = lat_deg if direction_lat == 'N' else -lat_deg
    lon = lon_deg if direction_lon == 'E' else -lon_deg
    return lat, lon

def array_equal(arr1, arr2) :
    if len(arr1) != len(arr2) :
        return False
    else :
        for i in range(len(arr1)) :
            if arr1[i] != arr2[i] :
                return False
        return True

def display():
    # Charger les données
    db_path = 'donky.db'
    table_name = "climate"
    df = load_data(db_path, table_name)
    df["eventTime"] = pd.to_datetime(df["eventTime"])  # Convertir eventTime en datetime

    st.title("Analyse des événements climatiques")

    # Créer deux colonnes : une plus large pour le graphique, une plus petite pour les boutons
    col1, col2 = st.columns([3, 1])

    # Créer un espace vide pour le graphique principal
    if "current_visu" not in st.session_state:
        st.session_state["current_visu"] = '1'
    #st.session_state.current_visu = '1'
    plot_area = col1.empty()

    # Visualisation des événements climatiques
    def plot_events(selected_kinds):
        selected_kinds = st.multiselect(
            "Sélectionnez les types d'événements :", 
            kinds, 
            default=st.session_state.selected_kinds
        )
        
        # Mettre à jour st.session_state lorsque la sélection change
        if not array_equal(selected_kinds, st.session_state.selected_kinds):
            st.session_state.selected_kinds = selected_kinds
            #st.experimental_rerun()  # Rafraîchir la page

        plot_area.empty()  # Vider l'espace actuel
        st.write("**Tendance quotidienne : Nombre d'événements par jour pour chaque type sélectionné**")
        
        # Filtrer les données
        filtered_df = df[df["kind"].isin(selected_kinds)]
        filtered_df["day"] = filtered_df["eventTime"].dt.to_period("D")
        grouped = filtered_df.groupby(["day", "kind"]).size().reset_index(name="count")
        pivot_df = grouped.pivot(index="day", columns="kind", values="count").fillna(0)

        # Création du graphique interactif avec Plotly
        fig = go.Figure()

        for kind in selected_kinds:
            if kind in pivot_df.columns:
                fig.add_trace(go.Scatter(
                    x=pivot_df.index.astype(str), 
                    y=pivot_df[kind],
                    mode="lines+markers",
                    name=kind
                ))

        fig.update_layout(
            title="Tendance quotidienne par type d'événement",
            xaxis_title="Jour",
            yaxis_title="Nombre d'événements",
            xaxis_tickangle=45,
            legend_title="Types d'événements",
            template="plotly_dark",
            autosize=True, 
            width=600,
            height=600
        )
        
        plot_area.plotly_chart(fig, use_container_width=True, key="unique_id1")

    # Scatter plot des flares
    def plot_flares():
        plot_area.empty()  # Vider l'espace actuel
        table_name_flare = "flare"
        flare_df = load_data(db_path, table_name_flare)
        flare_df["sourceLocation"] = flare_df["sourceLocation"].astype(str)
        
        # Convertir les coordonnées en latitudes et longitudes
        flare_df[['latitude', 'longitude']] = flare_df["sourceLocation"].apply(
            lambda coord: pd.Series(convert_coordinates(coord))
        )
        
        # Ajouter la colonne 'main_class'
        flare_df['main_class'] = flare_df['classType'].apply(
            lambda x: 'M' if x.startswith('M') else ('X' if x.startswith('X') else 'Other')
        )
        
        # Création du scatter plot interactif avec Plotly
        fig = go.Figure()

        # Boucle sur chaque classe principale pour les colorier
        colors = px.colors.qualitative.Plotly
        for i, main_class in enumerate(flare_df['main_class'].unique()):
            class_data = flare_df[flare_df['main_class'] == main_class]
            fig.add_trace(go.Scatter(
                x=class_data['longitude'], 
                y=class_data['latitude'], 
                mode='markers',
                marker=dict(color=colors[i % len(colors)], size=6, opacity=0.7),
                name=main_class
            ))

        # Ajouter un cercle représentant le centre (0, 0)
        fig.add_shape(
            type="circle",
            xref="x", yref="y",
            x0=-10, y0=-10, x1=10, y1=10,
            line=dict(color="Blue", width=2, dash="dash")
        )

        # Forcer l'échelle égale entre les axes X et Y
        fig.update_layout(
            title="Scatter plot des flares",
            xaxis_title="Longitude",
            yaxis_title="Latitude",
            template="plotly_dark",
            autosize=True,
            legend=dict(title="Flare", font=dict(size=10)),
            showlegend=True,
            xaxis=dict(range=[-50, 50], scaleanchor="y"),  # Limites pour l'axe X
            yaxis=dict(range=[-100, 100]),  # Limites pour l'axe Y
            width=600,  # Fixer la largeur de la figure
            height=600
        )

        plot_area.plotly_chart(fig, use_container_width=True)


    def plot_geomagnetic():
        plot_area.empty()  # Vider l'espace actuel
        table_name_geomagnetic = "geomagnetic"
        geomagnetic_df = load_data(db_path, table_name_geomagnetic)
        geomagnetic_df["date"] = pd.to_datetime(geomagnetic_df["observedTime"])  # Convertir la date en datetime
        
        # Créer une colonne pour les symboles de points en fonction de kpId
        symbols = {0: "circle", 1: "triangle-up", 2: "square", 3: "diamond"}
        geomagnetic_df["marker_symbol"] = geomagnetic_df["kpId"].map(symbols).fillna("circle")

        # Création du scatter plot avec Plotly
        fig = go.Figure()

        for kpId, data in geomagnetic_df.groupby("kpId"):
            fig.add_trace(go.Scatter(
                x=data["date"],
                y=data["kpIndex"],
                mode="markers",
                marker=dict(
                    size=8,
                    symbol=data["marker_symbol"],
                    opacity=0.8
                ),
                name=f"KpId: {kpId}"
            ))

        fig.update_layout(
            title="Indice Kp en fonction du temps",
            xaxis_title="Date",
            yaxis_title="Kp Index",
            template="plotly_dark",
            autosize=True,
            legend=dict(title="KpId", font=dict(size=10)),
            showlegend=True,
            width=800,  # Largeur du graphique
            height=600  # Hauteur du graphique
        )

        plot_area.plotly_chart(fig, use_container_width=True)


    def plot_coronal_analysis():
        plot_area.empty()  # Vider l'espace actuel

        # Charger les données des tables coronal_impact et coronal_analyse
        table_impact = "coronal_impact"
        table_analyse = "coronal_analyse"
        impact_df = load_data(db_path, table_impact)
        analyse_df = load_data(db_path, table_analyse)

        # Faire la jointure entre les deux tables
        merged_df = pd.merge(impact_df, analyse_df, left_on="id", right_on="id", how="inner")

        # Convertir arrivalTime en datetime pour une gestion correcte
        merged_df["arrivalTime"] = pd.to_datetime(merged_df["arrivalTime"], errors="coerce")

        # Sélecteur pour la variable à colorier
        variable = st.selectbox(
            "Choisissez la variable pour colorier les points :", 
            ["halfAngle", "speed", "arrivalTime", "type"]
        )

        # Gestion de la coloration
        if variable == "arrivalTime":
            # Convertir arrivalTime en timestamp pour une coloration continue
            merged_df["arrivalTimestamp"] = merged_df["arrivalTime"].apply(lambda x: x.timestamp() if not pd.isnull(x) else None)
            color_var = "arrivalTimestamp"
            color_scale = "Viridis"
        elif variable in ["halfAngle", "speed"]:
            color_var = variable
            color_scale = "Viridis"
        else:  # Variable qualitative (type)
            color_var = variable
            color_scale = px.colors.qualitative.Set3

        # Création du scatter plot
        fig = px.scatter(
            merged_df,
            x="longitude",
            y="latitude",
            color=color_var,
            color_continuous_scale=color_scale if variable != "type" else None,
            color_discrete_sequence=color_scale if variable == "type" else None,
            title="Analyse coronal : Distribution par latitude/longitude",
            labels={"longitude": "Longitude", "latitude": "Latitude", variable: variable},
            hover_data=["halfAngle", "speed", "arrivalTime", "type"]
        )

        # Ajuster la palette de couleurs et les limites des axes
        fig.update_layout(
            template="plotly_dark",
            width=800,
            height=600,
            coloraxis_colorbar=dict(title=variable if variable != "type" else "Type")
        )

        plot_area.plotly_chart(fig, use_container_width=True)



    # Gestion des boutons et du multiselect
    kinds = df["kind"].unique()

    # Utiliser st.session_state pour garder la trace de la sélection
    if "selected_kinds" not in st.session_state:
        st.session_state.selected_kinds = kinds  # Valeur par défaut

    # Afficher le multiselect et stocker la sélection dans session_state
    
    # Initialiser la visualisation par défaut
    

    # Boutons pour changer de visualisation
    with col2:
        st.subheader("Autres visualisations")
        
        # Bouton pour réafficher la première visualisation
        if st.button("Daily report of event"):
            st.session_state['current_visu'] = '1'
            #plot_events(st.session_state.selected_kinds)

        # Bouton pour afficher le scatter plot des flares
        if st.button("Flare"):
            st.session_state['current_visu'] = '2'
            #plot_flares()
        if st.button("Geomagnetic Storm") :
            st.session_state["current_visu"]='3'

        if st.button("Coronal Impact") :
            st.session_state["current_visu"] = '4'

    if st.session_state["current_visu"] == '1' :
        plot_events(st.session_state.selected_kinds)

    if st.session_state["current_visu"] == '2' :
        plot_flares()
    if st.session_state["current_visu"] == "3" :
        plot_geomagnetic()
    if st.session_state["current_visu"] == '4' :
        plot_coronal_analysis()




