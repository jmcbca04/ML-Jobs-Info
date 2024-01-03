import streamlit as st
import pandas as pd
import pydeck as pdk

# Streamlit page title
st.title('Where companies are hiring candidates with Machine Learning skills in the US')

# Load data
df = pd.read_csv('job_listings_with_coordinates.csv')

# Define the tooltip for hover functionality
tooltip = {
    "html": "<b>Title:</b> {title} <br><b>Location:</b> {location}",
    "style": {
        "backgroundColor": "steelblue",
        "color": "white"
    }
}

# Define the layer
layer = pdk.Layer(
    "ScatterplotLayer",
    df,
    get_position=["longitude", "latitude"],
    get_color=[255, 0, 0, 160],  # Red color, adjust as needed
    get_radius=10000,  # Radius of the dots, adjust for visibility
    pickable=True
)

# Define the view state
view_state = pdk.ViewState(
    latitude=df["latitude"].mean(),
    longitude=df["longitude"].mean(),
    zoom=4
)

# Render the deck.gl map
st.pydeck_chart(pdk.Deck(layers=[layer], initial_view_state=view_state, tooltip=tooltip))
