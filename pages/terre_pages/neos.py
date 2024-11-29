import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Fonction pour charger la base de données
def load_data(db_path, table_name):
    conn = sqlite3.connect(db_path)
    df = pd.read_sql_query(f"SELECT * FROM {table_name};", conn)
    conn.close()
    return df

# Fonction pour appliquer des filtres
def filter_data(df):
    st.sidebar.title("Filter data")

    # Filtre sur miss_distance
    miss_distance_range = st.sidebar.slider(
        "Distance (min and max)",
        min_value=float(df['miss_distance'].min()),
        max_value=float(df['miss_distance'].max()),
        value=(float(df['miss_distance'].min()), float(df['miss_distance'].max()))
    )
    df = df[(df['miss_distance'] >= miss_distance_range[0]) & 
            (df['miss_distance'] <= miss_distance_range[1])]

    # Filtre sur relative_velocity
    velocity_range = st.sidebar.slider(
        "Relative Velocity (min and max)",
        min_value=float(df['relative_velocity'].min()),
        max_value=float(df['relative_velocity'].max()),
        value=(float(df['relative_velocity'].min()), float(df['relative_velocity'].max()))
    )
    df = df[(df['relative_velocity'] >= velocity_range[0]) & 
            (df['relative_velocity'] <= velocity_range[1])]

    # Filtre sur absolute_magnitude
    magnitude_range = st.sidebar.slider(
        "Absolute Magnitude (min and max)",
        min_value=float(df['absolute_magnitude'].min()),
        max_value=float(df['absolute_magnitude'].max()),
        value=(float(df['absolute_magnitude'].min()), float(df['absolute_magnitude'].max()))
    )
    df = df[(df['absolute_magnitude'] >= magnitude_range[0]) & 
            (df['absolute_magnitude'] <= magnitude_range[1])]
    
    return df

# Scatter plot avec Plotly
def plot_scatter(df):
    if not pd.api.types.is_datetime64_any_dtype(df['close_approach_date']):
        df['close_approach_date'] = pd.to_datetime(df['close_approach_date'])
    df = df.sort_values('close_approach_date')

    fig = px.scatter(
        df,
        x='close_approach_date',
        y='miss_distance',
        title="Miss Distance vs Time",
        labels={'close_approach_date': 'Date', 'miss_distance': 'Miss Distance'},
        color='relative_velocity',
        color_continuous_scale='Viridis'
    )
    fig.update_traces(marker=dict(size=6, opacity=0.8))
    return fig

def plot_relation(df, x_var, y_var, color_var=None):
    if color_var:
        fig = px.scatter(
            df,
            x=x_var,
            y=y_var,
            title=f"Relationship between {x_var.replace('_', ' ').title()} and {y_var.replace('_', ' ').title()}",
            labels={x_var: x_var.replace('_', ' ').title(), y_var: y_var.replace('_', ' ').title()},
            color=color_var,
            color_continuous_scale='Viridis'
        )
    else:
        fig = px.scatter(
            df,
            x=x_var,
            y=y_var,
            title=f"Relationship between {x_var.replace('_', ' ').title()} and {y_var.replace('_', ' ').title()}",
            labels={x_var: x_var.replace('_', ' ').title(), y_var: y_var.replace('_', ' ').title()},
        )
    fig.update_traces(marker=dict(size=6, opacity=0.8))
    return fig

# Graphique de densité avec Plotly
def plot_density(df, variable):
    fig = go.Figure()

    fig.add_trace(
        go.Histogram(
            x=df[variable],
            histnorm='probability density',
            name='Density',
            marker=dict(color='skyblue'),
            opacity=0.75
        )
    )

    fig.update_layout(
        title=f"Density Plot of {variable.replace('_', ' ').title()}",
        xaxis_title=variable.replace('_', ' ').title(),
        yaxis_title='Density',
        bargap=0.2
    )
    return fig

# Page principale
def display():
    db_path = 'neo.db'
    table_name = 'neo'

    # Charger les données
    df = load_data(db_path, table_name)

    # Afficher le titre
    st.title("Asteroids : Near Earth Objects Analysis")
    st.write("Here is a small dashboard for listing objects flying near earth and analyzing their caracteristics.")
    st.write("")
    st.write("")

    # Appliquer les filtres
    df_filtered = filter_data(df)

    col1a, col2a = st.columns([1, 1])
    with col1a :
        st.metric("Current number of objects selected : ", len(df_filtered))
    with col2a :
        variable = st.selectbox(
            "Select a variable for the density plot",
            ["miss_distance", "relative_velocity", "absolute_magnitude"]
        )

    # Scatter plot
    scatter_fig = plot_scatter(df_filtered)

    # Densité
    
    density_fig = plot_density(df_filtered, variable)

    # Afficher les deux graphiques côte à côte
    st.subheader("Visualizations")
    st.write("")

    col1b, col2b = st.columns(2)
    with col1b:
        st.plotly_chart(scatter_fig, use_container_width=True)
    with col2b:
        st.plotly_chart(density_fig, use_container_width=True)


    st.subheader("Analysis of correlation between two variables")
    col1c, col2c = st.columns([1, 3]) 

    
    with col1c :

        x_var = st.selectbox(
            "Select the variable for the X axis",
            df_filtered.columns.tolist()
        )
        y_var = st.selectbox(
            "Select the variable for the Y axis",
            df_filtered.columns.tolist()
        )

        # Sélectionner la variable pour colorier les points
        color_var = st.selectbox(
            "Select a variable to color the points",
            ["relative_velocity", "miss_distance", "absolute_magnitude"] + df_filtered.columns.tolist()
        )
    with col2c :
        # Générer et afficher le graphique de la relation
        relation_fig = plot_relation(df_filtered, x_var, y_var, color_var)
        st.plotly_chart(relation_fig, use_container_width=True)
