import streamlit as st
import pandas as pd
import os
import plotly.express as px


# Function to filter and plot data
def plot_filtered_data():
    df = pd.read_csv("mars_weather.csv")
    df["pressure"] = pd.to_numeric(df["pressure"], errors="coerce")
    df = df.dropna(subset=["pressure"])
    df = df.drop("wind_speed", axis = 1)
    st.sidebar.header("Plotting Options")

    # Sidebar: Select variable to plot
    variable_to_plot = st.sidebar.selectbox(
        "Select a variable to plot:",
        options=["pressure", "min_temp", "max_temp"],
        format_func=lambda x: x.replace("_", " ").title()
    )

    # Sidebar: Select sol range
    min_sol = int(df["sol"].min())
    max_sol = int(df["sol"].max())
    sol_range = st.sidebar.slider(
        "Select Sol Range",
        min_value=min_sol,
        max_value=max_sol,
        value=(min_sol, max_sol)
    )


    # Filter data based on pressure range
    filtered_df = df[df["sol"].between(*sol_range)]

    # Plot the selected variable
    st.subheader(f"{variable_to_plot.replace('_', ' ').title()} Trends on Mars")
    fig = px.line(
        filtered_df,
        x="sol",
        y=variable_to_plot,
        title=f"{variable_to_plot.replace('_', ' ').title()} on Mars over Time (Sol)",
        labels={"sol": "Martian Sol", variable_to_plot: variable_to_plot.replace('_', ' ').title()},
        markers=True
    )
    st.plotly_chart(fig)

    # Display filtered results
    st.write(f"Filtered Data (Sol between {sol_range[0]} and {sol_range[1]} ):")
    st.dataframe(filtered_df)

    # Display summary statistics
    st.write("Summary Statistics:")
    st.write(filtered_df.describe())
