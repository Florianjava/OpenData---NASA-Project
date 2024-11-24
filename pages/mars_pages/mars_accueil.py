import streamlit as st


def display():
    st.title("Page Accueil de Mars")
    st.write("Bienvenue sur la page d'accueil de Mars !")

    # Sous-menu pour Terre Accueil
    sub_menu = st.radio("Sous-pages de Terre", ["InSight", "Rover"])
    
    if sub_menu == "InSight":
        from .insight import display
        display()
        
    elif sub_menu == "Rover":
        from .rover import display
        display()