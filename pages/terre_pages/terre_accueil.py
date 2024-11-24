import streamlit as st

def display() :
    st.title("Page Accueil de Terre")
    st.write("Bienvenue sur la page d'accueil de Terre !")

    # Sous-menu pour Terre Accueil
    sub_menu = st.radio("Sous-pages de Terre", ["Earth", "EONET"])
    
    if sub_menu == "Earth":
        from pages.terre_pages.earth import display
        display()
        
    elif sub_menu == "EONET":
        from pages.terre_pages.eonet import display
        display()