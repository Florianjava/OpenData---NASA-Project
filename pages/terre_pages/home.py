import streamlit as st
import requests
import datetime
import time
import random

# Date d'hier
yesterday = (datetime.datetime.now() - datetime.timedelta(days=1)).strftime('%Y-%m-%d')

# Fonction pour récupérer les images de la date d'hier
def get_images_for_date(date):
    url = f"https://api.nasa.gov/EPIC/api/natural/date/{date}?api_key=kmprgzbT3jYlUGYa2BeDfRWMjrEnUu4RcWrelMfJ"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    return []



def display() :
# Récupérer les images
    images = get_images_for_date(yesterday)
    st.title("Earth Homepage")
    st.write("")
    st.write("")
    st.write("")

    # Diviser en colonnes
    col1, col2 = st.columns([3, 4])

   
    with col1: 
        # Texte avec une taille différente pour les 2 premières phrases et liste HTML
        st.markdown("""
            <h2>Welcome to the Earth Home Page.</h2>  
            <h3>Here you can use the three following APIs from the NASA website:</h3>
            <ul>
                <li><strong>Earth Imagery</strong>: Request a satellite picture of a location using its coordinates and a date.</li>
                <li><strong>EONET API</strong>: Reports different natural events that happened in recent days all around the globe.</li>
                <li><strong>NEOs API</strong>: Tracks flying objects like asteroids.</li>
            </ul>
        """, unsafe_allow_html=True)

    # Colonne de droite : Affichage d'images
    with col2:
        st.subheader("NASA EPIC Images (Yesterday)")
        if images:
            if 'image_idx' not in st.session_state:
                st.session_state.image_idx = random.randint(0, len(images) - 1)
            # Sélectionner une image à partir de l'indice stocké
            image = images[st.session_state.image_idx]
            image_date = image["date"].split(" ")[0].replace("-", "/")
            image_name = image["image"]
            image_url = f"https://api.nasa.gov/EPIC/archive/natural/{image_date}/png/{image_name}.png?api_key=kmprgzbT3jYlUGYa2BeDfRWMjrEnUu4RcWrelMfJ"
                
                # Afficher l'image
            st.image(image_url, caption=image["caption"])
            
                
        else:
            st.write("No images available for yesterday.")
