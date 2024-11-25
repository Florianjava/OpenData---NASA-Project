import streamlit as st
import requests
from PIL import Image
from io import BytesIO

def display():
    st.title("NASA Earth Imagery API")
    
    # Inputs pour les coordonnées et la date
    lon = st.number_input("Longitude", value=100.75, format="%.6f")
    lat = st.number_input("Latitude", value=1.5, format="%.6f")
    date = st.text_input("Date (YYYY-MM-DD)", value="2014-02-01")
    zoom = st.number_input("niveau de zoom", value=0.1, min_value=0.0, max_value=1.0)
    
    if st.button("Get Image"):
        # URL de l'API
        url = f"https://api.nasa.gov/planetary/earth/imagery"
        params = {
            "lon": lon,
            "lat": lat,
            "date": date,
            "api_key": "DEMO_KEY",
            "dim":zoom
        }
        
        response = requests.get(url, params=params)
        if response.status_code == 200:
            img = Image.open(BytesIO(response.content))
            st.image(img, caption=f"Image for {lat}, {lon} on {date}", use_column_width=True)
        else:
            st.error(f"Error: {response.status_code} - {response.json().get('msg', 'Unknown error')}")