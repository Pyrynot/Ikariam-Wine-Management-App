import streamlit as st
import requests

BACKEND_URL = "http://localhost:8000"

def get_towns():
    response = requests.get(f"{BACKEND_URL}/towns/")
    if response.status_code == 200:
        return response.json()
    else:
        return []

def add_town(player_name, town_name, wine_storage, wine_hourly_consumption):
    response = requests.post(f"{BACKEND_URL}/towns/", json={
        "player_name": player_name,
        "town_name": town_name,
        "wine_storage": wine_storage,
        "wine_hourly_consumption": wine_hourly_consumption
    })
    return response.status_code

st.title('Wine Management System for Game Towns')

st.header('Add a New Town')
with st.form("add_town"):
    player_name = st.text_input("Player Name")
    town_name = st.text_input("Town Name")
    wine_storage = st.number_input("Wine Storage", min_value=0.0, format="%f")
    wine_hourly_consumption = st.number_input("Wine Hourly Consumption", min_value=0.0, format="%f")
    submitted = st.form_submit_button("Submit")
    if submitted:
        status_code = add_town(player_name, town_name, wine_storage, wine_hourly_consumption)
        if status_code == 200:
            st.success("Town added successfully!")
        else:
            st.error("Failed to add town. Please try again.")

st.header('Existing Towns')
towns = get_towns()
if towns:
    for town in towns:
        st.subheader(town["town_name"])
        st.write(f"Player Name: {town['player_name']}")
        st.write(f"Wine Storage: {town['wine_storage']}")
        st.write(f"Wine Hourly Consumption: {town['wine_hourly_consumption']}")
else:
    st.write("No towns found.")
