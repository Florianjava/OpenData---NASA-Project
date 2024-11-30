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
        <h2>Explore Mars and Space Weather Data!</h2>

        <p>In the <strong>Mars</strong> section, you can:</p>
        <ul>
            <li><strong>View Stunning Photos</strong>: Discover images captured by Mars rovers through NASA’s Mars Rover API.</li>
            <li><strong>Check Martian Weather</strong>: Access weather data from the InSight lander, providing insights into Mars’ atmospheric conditions.</li>
            <li><strong>Explore Space Weather</strong>: Stay updated with space weather events using the DONKI API, offering real-time information on solar activities and their potential impact.</li>
        </ul>

        <p>Dive in and explore the Red Planet and beyond! 🌌🔭</p>

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
