import streamlit as st
import requests 

st.set_page_config(page_title="Planetary Exploration", layout="wide")

if 'menu' not in st.session_state:
    st.session_state.menu = "Home"  # Valeur par défaut




st.sidebar.title("Menu Principal")
menu_1 = st.sidebar.button("Home")
menu_2 = st.sidebar.button("Earth")
menu_3 = st.sidebar.button("Mars")

if menu_1:
    st.session_state.menu = "Home"
elif menu_2:
    st.session_state.menu = "Earth"
    st.session_state.sub_menu = "Earth Homepage"
elif menu_3:
    st.session_state.menu = "Mars"
    st.session_state.sub_menu = "Mars Homepage"




if st.session_state.menu == "Home":
    st.title("Nasa's data dashboard")

    # NASA APOD API request
    api_key = "HGekEmLtCDZMt3lz64DHrHfS526Mx5vPGfQaUnOv"  
    apod_url = f"https://api.nasa.gov/planetary/apod?api_key={api_key}"

    left_column, right_column = st.columns([0.6, 0.4], gap="large", vertical_alignment = "top")

    with left_column:
        st.markdown(f"""
        <div style='font-size: 15px; color: white;'>
            <strong><u>NASA API Overview</u></strong><br>
            NASA offers a range of APIs that provide access to exciting astronomical data. Key APIs include:<br>
            <ul>
                <li><strong>Astronomy Picture of the Day (APOD)</strong>: Get daily stunning images of space, complete with descriptions by professional astronomers.</li>
                <li><strong>Near Earth Object Web Service (NEOWS)</strong>: Track near-Earth objects, including asteroids and comets, with data on their size, orbit, and impact risks.</li>
                <li><strong>Mars Rover Photos</strong>: Access images captured by Mars rovers like Curiosity and Perseverance, filtered by date and location.</li>
                <li><strong>InSight</strong>: Explore data from NASA's InSight lander, studying Mars' seismic activity and atmospheric conditions.</li>
                <li><strong>Exoplanet Archive</strong>: Discover confirmed exoplanets and their characteristics, enhancing our understanding of planetary systems beyond our own.</li>
            </ul>
            These APIs empower users to explore and engage with the wonders of space and planetary science.<br>
            For more details, visit the <a href="https://api.nasa.gov/" style="color: white;">NASA APIs Documentation</a>.
        </div>
        """, unsafe_allow_html=True)

    with right_column:
        response = requests.get(apod_url)
        if response.status_code == 200:
            apod_data = response.json()
            apod_title = apod_data.get("title")
            apod_img_url = apod_data.get("url")
            apod_explanation = apod_data.get("explanation")
            apod_date = apod_data.get("date")

            st.markdown(f"""
            <div style='font-size: 15px; color: white;'>
                <strong><u>Pic of the day</u></strong><br>
            </div>
            """, unsafe_allow_html=True)
            st.markdown(f"<div style='text-align: center;font-size: 25px;font-weight: bold; color: white;'>{apod_title} ({apod_date})</div>", unsafe_allow_html=True)
            st.markdown(f"<div style='text-align: center;'><img src='{apod_img_url}' style='max-width: 100%; width: 500px;'></div>", unsafe_allow_html=True)
            # st.markdown(f"<div style='font-size: 12px; color: white;'>{apod_explanation}</div>", unsafe_allow_html=True)

            # st.write(apod_explanation)
        else:
            st.write("Error retrieving the daily image.")




elif st.session_state.menu == "Earth":
   
    col1, col2, col3, col4 = st.columns([1, 1, 1, 1]) 
    with col1:
        sub_menu_1 = st.button("Earth Homepage")
    with col2:
        sub_menu_2 = st.button("Earth photo")
    with col3:
        sub_menu_3 = st.button("EONET")
    with col4 :
        sub_menu_4 = st.button("NEOS")



    if sub_menu_1 :
        st.session_state.sub_menu = "Earth Homepage"
    elif sub_menu_2 :
        st.session_state.sub_menu = "Earth photo"
    elif sub_menu_3 :
        st.session_state.sub_menu = "EONET"
    elif sub_menu_4 :
        st.session_state.sub_menu = "NEOS"



    if st.session_state.sub_menu == "Earth Homepage" :
    
        st.title("Earth homepage")
        st.write("Bienvenue sur la page d'accueil de Terre !")
    
    elif st.session_state.sub_menu == "Earth photo" :
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
        sub_menu_1 = st.button("Mars Homepage")
    with col2:
        sub_menu_2 = st.button("InSight")
    with col3:
        sub_menu_3 = st.button("Rover")



    if sub_menu_1 :
        st.session_state.sub_menu = "Mars Homepage"
    elif sub_menu_2 :
        st.session_state.sub_menu = "InSight"
    elif sub_menu_3 :
        st.session_state.sub_menu = "Rover"



    if st.session_state.sub_menu == "Mars Homepage" :
        st.title("Mars homepage")
        st.write("Bienvenue sur la page d'accueil de Mars !")
    
    elif st.session_state.sub_menu == "InSight" :
        st.title("Sous-page InSight")
        from pages.mars_pages.insight import display
        display()  
        
    elif st.session_state.sub_menu == "Rover":  
        st.title("Sous-page Rover")
        from pages.mars_pages.rover import display
        display()  
