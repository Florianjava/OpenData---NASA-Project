import streamlit as st
import requests
import pandas as pd
import folium
from folium.plugins import MarkerCluster
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# Fonction pour récupérer les événements depuis l'API EONET
def fetch_eonet_data(limit):
    url = "https://eonet.gsfc.nasa.gov/api/v2.1/events"
    params = {
        'status': 'all',  # Obtenir tous les événements
        'limit': limit,  # Limite des événements (tu peux ajuster selon tes besoins)
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()['events']
    else:
        st.error("Erreur lors de la récupération des données EONET")
        return []

# Fonction pour afficher la carte avec les événements
def display_eonet_map(events):
    # Initialiser la carte (centrée sur une zone générique pour commencer)
    m = folium.Map(location=[20, 0], zoom_start=2)

    # Utiliser un MarkerCluster pour regrouper les événements proches
    marker_cluster = MarkerCluster().add_to(m)

    # Définir les icônes pour chaque type d'événement
    """
    event_icons = {
        "Wildfires": "pages/terre_pages/weather_icons/flame.svg",  # Icône de flamme pour les incendies
        "Earthquakes":  "pages/terre_pages/weather_icons/earthquake.svg",  # Icône de séisme
        "Severe Storms":  "pages/terre_pages/weather_icons/tornado.svg",  # Icône de tempête
        "Drought": "",  # Sécheresse
        "Dust and Haze": "",  # Poussière et brume
        "Floods": "",  # Inondations
        "Landslides": "",  # Glissement de terrain
        "Manmade": "",  # Événements d'origine humaine
        "Sea and Lake Ice": "",  # Glace de mer et de lac
        "Snow": "pages/terre_pages/weather_icons/snow.svg",  # Neige
        "Temperature Extremes": "",  # Températures extrêmes
        "Volcanoes": "pages/terre_pages/weather_icons/volcano.svg",  # Volcans
        "Water Color": "pages/terre_pages/weather_icons/water.svg",  # Couleur de l'eau
    }
    """
    event_colors = {
        "Wildfires": "red",  # Icône de flamme pour les incendies
        "Earthquakes":  "brown",  # Icône de séisme
        "Severe Storms":  "blue",  # Icône de tempête
        "Drought": "yellow",  # Sécheresse
        "Dust and Haze": "white",  # Poussière et brume
        "Floods": "lightblue",  # Inondations
        "Landslides": "lightbrown",  # Glissement de terrain
        "Manmade": "gray",  # Événements d'origine humaine
        "Sea and Lake Ice": "white",  # Glace de mer et de lac
        "Snow": "white",  # Neige
        "Temperature Extremes": "orange",  # Températures extrêmes
        "Volcanoes": "black",  # Volcans
        "Water Color": "green",  # Couleur de l'eau
    }
    # Ajouter chaque événement sur la carte avec une icône spécifique
    for event in events:
        if 'geometries' in event and event['geometries']:
            # Prendre les coordonnées du premier point géographique de l'événement
            coordinates = event['geometries'][0]['coordinates']
            latitude = coordinates[1]
            longitude = coordinates[0]
            title = event['title']
            description = event.get('description', 'Aucune description disponible')

            # Identifier le type d'événement et choisir l'icône
            event_type = None
            for category in event.get('categories', []):
                category_title = category['title']
                if category_title in event_colors:
                    event_type = category_title
                    break

            # Choisir l'icône basée sur le type d'événement
            if event_type:
                #icon_url = event_icons.get(event_type)
                color = event_colors.get(event_type)
                icon = folium.Icon(color=color, icon="info-sign")
                #icon = folium.CustomIcon(icon_url, icon_size=(40, 40))
            else:
                icon = folium.Icon(color="blue")  # Icône par défaut si pas de correspondance

            # Ajouter un marqueur pour chaque événement
            folium.Marker(
                location=[latitude, longitude],
                popup=f"<b>{title}</b><br>{description}",
                icon=icon
            ).add_to(marker_cluster)

    # Afficher la carte dans Streamlit
    map_html = f"""
    <div style="width: 100%; height: 400px;">
        {m._repr_html_()}
    </div>
    """
    
    # Afficher la carte dans Streamlit
    st.components.v1.html(map_html, height=600, scrolling=False)
    #st.components.v1.html(m._repr_html_(), width=900, height=600)

# Fonction pour analyser les événements et générer des séries temporelles
def generate_time_series(events):
    event_data = []
    

    # Itérer sur les événements pour extraire les informations nécessaires
    for event in events:
        # Extraire la date de l'événement
        if 'geometries' in event and event['geometries']:
            geometry = event['geometries'][0]
            event_date = pd.to_datetime(geometry['date'])
            event_categories = [category['title'] for category in event.get('categories', [])]
            
            for category in event_categories:
                event_data.append({
                    'date': event_date,
                    'category': category
                })
    
    # Créer un DataFrame pour mieux manipuler les données
    df = pd.DataFrame(event_data)
    
    if not df.empty:
        # Compter les événements par type et par date
        df_count = df.groupby([pd.Grouper(key='date', freq='D'), 'category']).size().unstack(fill_value=0)

        return df_count
    else:
        st.write("No event to analyze.")
        return None

# Fonction pour afficher les séries temporelles
def display_time_series(df_count):
    if df_count is not None:
        event_colors = {
            "Wildfires": "red",  # Icône de flamme pour les incendies
            "Earthquakes":  "brown",  # Icône de séisme
            "Severe Storms":  "blue",  # Icône de tempête
            "Drought": "yellow",  # Sécheresse
            "Dust and Haze": "white",  # Poussière et brume
            "Floods": "lightblue",  # Inondations
            "Landslides": "lightbrown",  # Glissement de terrain
            "Manmade": "gray",  # Événements d'origine humaine
            "Sea and Lake Ice": "white",  # Glace de mer et de lac
            "Snow": "white",  # Neige
            "Temperature Extremes": "orange",  # Températures extrêmes
            "Volcanoes": "black",  # Volcans
            "Water Color": "green",  # Couleur de l'eau
        }
        # Afficher la série temporelle par catégorie
        st.subheader("Number of event per category")

        # Créer une figure plus petite
        fig, ax = plt.subplots(figsize=(18, 10))
        colors = [event_colors[col] for col in df_count.columns if col in event_colors]

        df_count.plot(ax=ax, color=colors)
        
        ax.set_title("Number of event in function of the time")
        ax.set_xlabel("Date")
        ax.set_ylabel("Number of event")
        ax.xaxis.set_major_locator(mdates.MonthLocator())
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
        plt.xticks(rotation=45)
        plt.tight_layout()

        return fig

# Fonction qui sera appelée dans la page EONET
def display():
    st.title("Earth Observatory Natural Events Tracker : EONET")
    
    limit = st.slider('Select a limit of event to fetch', min_value=10, max_value=1000, value=100, step=10)

    # Récupérer les événements EONET
    events = fetch_eonet_data(limit=limit)

    if events:
        st.write(f"Number of element found : {len(events)}")

        # Créer deux colonnes pour afficher la carte et le graphique côte à côte
        col1, col2 = st.columns([4, 2])  # Colonne 1 pour la carte (plus large), Colonne 2 pour le graphique

        with col1:
            # Afficher la carte avec les événements
            display_eonet_map(events)

        with col2:
            # Générer et afficher les séries temporelles
            df_count = generate_time_series(events)
            if df_count is not None:
                # Afficher le graphique dans la colonne 2
                fig = display_time_series(df_count)
                st.pyplot(fig)
    else:
        st.write("No event available.")


   
