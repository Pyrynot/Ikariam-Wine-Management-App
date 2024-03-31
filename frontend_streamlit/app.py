import streamlit as st
from components import TownManager, highlight_low_wine, get_towns

st.header("Transfer Wine Between Towns")

town_manager = TownManager()

towns = get_towns()
unique_player_names = town_manager.get_unique_player_names()

# Select player name outside the form
player_name = st.selectbox("Player Name", options=unique_player_names, key='player_name')

# Filter towns for the selected player
player_towns = town_manager.get_towns_by_player(player_name)
town_names = [town['town_name'] for town in player_towns]

# Select source town outside the form
source_town = st.selectbox("Source Town", options=town_names, key='source_town')

# Dynamic update of destination towns based on source town selection
destination_towns = [town for town in town_names if town != source_town]

with st.form("transfer_wine"):
    # Form for transferring wine
    destination_town = st.selectbox("Destination Town", options=destination_towns, key='destination_town')
    wine_amount = st.number_input("Wine Amount", min_value=0.0, format="%f", key='wine_amount')
    submitted_transfer = st.form_submit_button("Transfer Wine")
    if submitted_transfer:
        transfer_status = town_manager.transfer_wine(player_name, source_town, destination_town, wine_amount)
        if transfer_status:
            st.success("Wine transferred successfully!")
        else:
            st.error("Failed to transfer wine.")

# Display existing towns
st.header('Existing Towns')
town_manager.display_towns()

# Form for adding a new town
with st.form("add_town"):
    st.header('Add a New Town')
    status_code = town_manager.add_town_form()
    if status_code == 200:
        st.success("Town added successfully!")
    elif status_code is not None:  # Avoid showing this message on first load
        st.error("Failed to add town. Please try again.")

if st.button('Force Update Wine Levels'):
    update_message = town_manager.force_update_wine_levels()
    st.success(update_message)
