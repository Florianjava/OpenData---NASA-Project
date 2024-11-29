import streamlit as st


def display() :
    st.title("Mars Homepage")
    st.write("")
    st.write("")
    st.write("")

    col1, col2 = st.columns([1, 1])

    with col1: 
        # Texte avec une taille différente pour les 2 premières phrases et liste HTML
        st.markdown("""
            <h2>Welcome to the Mars Home Page.</h2>  
            <h3>Here you can use the three following APIs from the NASA website:</h3>
            <ul>
                <li><strong>InSight API</strong>: Provides climatic data on Mars.</li>
                <li><strong>Rover</strong>: Give access to Mars Rover's photos.</li>
                <li><strong>Donky</strong>: Describe some of the space climatic incident.</li>
            </ul>
        """, unsafe_allow_html=True)
    with col2 :
        st.image("pages/mars_pages/mars.jpg", use_column_width=True)
        st.markdown(
            """
            <p style="color: white; font-size: 14px;">
            Image taken from: <a href="https://th.bing.com/th/id/OIP.h0Sf1sMd2_uA2N4nYTMR1wHaEK?w=316&h=180&c=7&r=0&o=5&pid=1.7" style="color: white; text-decoration: none;">Link</a>
            </p>
            """,
            unsafe_allow_html=True
        )
