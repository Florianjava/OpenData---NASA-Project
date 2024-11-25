import streamlit as st

st.set_page_config(page_title="Exploration Planétaire", layout="wide")

if 'menu' not in st.session_state:
    st.session_state.menu = "Accueil"  # Valeur par défaut




st.sidebar.title("Menu Principal")
menu_1 = st.sidebar.button("Accueil")
menu_2 = st.sidebar.button("Terre")
menu_3 = st.sidebar.button("Mars")

if menu_1:
    st.session_state.menu = "Accueil"
elif menu_2:
    st.session_state.menu = "Terre"
    st.session_state.sub_menu = "Accueil"
elif menu_3:
    st.session_state.menu = "Mars"
    st.session_state.sub_menu = "Accueil"







if st.session_state.menu == "Accueil":
    st.title("Bienvenue sur notre site recensant les API de la NASA !")
    st.write("Sur ce site, vous pouvez explorer différentes pages d'informations sur les planètes.")







elif st.session_state.menu == "Terre":
   
    col1, col2, col3, col4 = st.columns([1, 1, 1, 1]) 
    with col1:
        sub_menu_1 = st.button("Terre - Accueil")
    with col2:
        sub_menu_2 = st.button("Earth")
    with col3:
        sub_menu_3 = st.button("EONET")
    with col4 :
        sub_menu_4 = st.button("NEOS")



    if sub_menu_1 :
        st.session_state.sub_menu = "Accueil"
    elif sub_menu_2 :
        st.session_state.sub_menu = "Earth"
    elif sub_menu_3 :
        st.session_state.sub_menu = "EONET"
    elif sub_menu_4 :
        st.session_state.sub_menu = "NEOS"



    if st.session_state.sub_menu == "Accueil" :
    
        st.title("Page Accueil de Terre")
        st.write("Bienvenue sur la page d'accueil de Terre !")
    
    elif st.session_state.sub_menu == "Earth" :
        from pages.terre_pages.earth import display
        display()  
        
    elif st.session_state.sub_menu == "EONET":  
        from pages.terre_pages.eonet import display
        display()  
    elif st.session_state.sub_menu == 'NEOS' :
        from pages.terre_pages.neos import display
        display()













elif st.session_state.menu == "Mars":

    col1, col2, col3 = st.columns([1, 1, 1]) 
    with col1:
        sub_menu_1 = st.button("Terre - Accueil")
    with col2:
        sub_menu_2 = st.button("InSight")
    with col3:
        sub_menu_3 = st.button("Rover")



    if sub_menu_1 :
        st.session_state.sub_menu = "Accueil"
    elif sub_menu_2 :
        st.session_state.sub_menu = "InSight"
    elif sub_menu_3 :
        st.session_state.sub_menu = "Rover"



    if st.session_state.sub_menu == "Accueil" :
    
        st.title("Page Accueil de Mars")
        st.write("Bienvenue sur la page d'accueil de Mars !")
    
    elif st.session_state.sub_menu == "InSight" :
        st.title("Sous-page InSight")
        from pages.mars_pages.insight import display
        display()  
        
    elif st.session_state.sub_menu == "Rover":  
        st.title("Sous-page Rover")
        from pages.mars_pages.rover import display
        display()  
