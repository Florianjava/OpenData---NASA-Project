import streamlit as st
import requests
from PIL import Image
from io import BytesIO

def display():
    st.title("NASA Earth Imagery API")

    st.markdown("""
    Get an image from wherever you want with its coordinate at any day, images from Landsat8.
    """)

    # Créer les colonnes pour les champs d'entrée
    col1, col2 = st.columns(2)
    
    with col1:
        # Inputs pour la longitude et latitude
        lon = st.number_input("Longitude", value=100.75, format="%.6f")
        
        date = st.text_input("Date (YYYY-MM-DD)", value="2024-11-28")
    
    with col2:
        # Inputs pour la date et niveau de zoom
        lat = st.number_input("Latitude", value=1.5, format="%.6f")
        zoom = st.number_input("Niveau de zoom", value=0.1, min_value=0.0, max_value=1.0)

    # Bouton Get Image sur la troisième ligne
    if st.button("Get Image"):
        # URL de l'API
        url = f"https://api.nasa.gov/planetary/earth/imagery"
        params = {
            "lon": lon,
            "lat": lat,
            "date": date,
            "api_key": "DEMO_KEY",
            "dim": zoom
        }
        
        response = requests.get(url, params=params)
        if response.status_code == 200:
            img = Image.open(BytesIO(response.content))
            st.image(img, caption=f"Image for {lat}, {lon} on {date}", use_column_width=True)
        else:
            st.error(f"Error: {response.status_code} - {response.json().get('msg', 'Unknown error')}")


