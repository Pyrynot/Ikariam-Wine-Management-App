import requests
import pandas as pd
import streamlit as st
from datetime import datetime
import pytz

BACKEND_URL = "http://localhost:8000"



#@st.cache_data()  # Updated to use Streamlit's recommended caching
def get_towns():
    """Fetch towns data from the backend."""
    response = requests.get(f"{BACKEND_URL}/towns/")
    return response.json()


class TownManager:
    def __init__(self):
        self.session = requests.Session()



    def get_unique_player_names(self):
        """Retrieve a unique list of player names from the cached towns data."""
        towns = get_towns()
        return sorted(set(town['player_name'] for town in towns))

    def get_towns_by_player(self, player_name):
        """Filter and return towns for a given player name from the cached towns data."""
        return [town for town in get_towns() if town['player_name'] == player_name]

    def transfer_wine(self, player_name, source_town_name, destination_town_name, wine_amount):
        response = self.session.post(f"{BACKEND_URL}/towns/transfer/", json={
            "player_name": player_name,
            "source_town_name": source_town_name,
            "destination_town_name": destination_town_name,
            "wine_amount": wine_amount
        })
        if response.status_code == 200:
            st.cache_data.clear()
            return response.status_code
            

    def add_town_form(self):
        player_name = st.text_input("Player Name")
        town_name = st.text_input("Town Name")
        wine_storage = st.number_input("Wine Storage", min_value=0.0, format="%f")
        wine_hourly_consumption = st.number_input("Wine Hourly Consumption", min_value=0.0, format="%f")
        wine_production = st.number_input("Wine Production", min_value=0.0, format="%f")
        submitted = st.form_submit_button("Submit")
        if submitted:
            st.cache_data.clear()
            return self.add_town(player_name, town_name, wine_storage, wine_hourly_consumption, wine_production)
            
        return None

    def add_town(self, player_name, town_name, wine_storage, wine_hourly_consumption, wine_production):
        response = self.session.post(f"{BACKEND_URL}/towns/", json={
            "player_name": player_name,
            "town_name": town_name,
            "wine_storage": wine_storage,
            "wine_hourly_consumption": wine_hourly_consumption,
            "wine_production": wine_production
        })
        if response.status_code == 200:
            
            return response.status_code
        
        

    def force_update_wine_levels(self):
        response = self.session.get(f"{BACKEND_URL}/force-update/")
        if response:
            st.cache_data.clear()
        return response.json().get("message", "Update triggered")

    def display_towns(self):
        towns = get_towns()
        if towns:
            for player_name in self.get_unique_player_names():
                player_towns = self.get_towns_by_player(player_name)  # Filter towns by player
                self.display_towns_for_player(player_name, player_towns)  # Pass the filtered list

    @staticmethod
    def display_towns_for_player(player_name, player_towns):
        towns_df = pd.DataFrame(player_towns)
        towns_df['last_update'] = pd.to_datetime(towns_df['last_update'], utc=True, format='mixed').dt.tz_convert('Etc/GMT-3')
        towns_df['time_until_empty'] = towns_df.apply(calculate_time_until_empty, axis=1)
        towns_df = TownManager.rename_and_format_df(towns_df)
        st.write(f"Towns for {player_name}:")
        st.dataframe(towns_df.style.apply(highlight_low_wine, subset=['time_until_empty']), height=600)

    @staticmethod
    def rename_and_format_df(df):
        df.rename(columns={
            'player_name': 'Name',
            'wine_storage': 'Amount',
            'wine_hourly_consumption': 'Consumption',
            'wine_production': 'Production',
            'town_name': 'Town',
            'last_update': 'Last Update'
        }, inplace=True)
        df['Amount'] = df['Amount'].astype(int)
        df['Consumption'] = df['Consumption'].astype(int)
        df['Production'] = df['Production'].astype(int)
        return df

def highlight_low_wine(row):
    return ['background-color: yellow' if val < 7 else '' for val in row]

def calculate_time_until_empty(row):
    net_consumption_rate = row['wine_hourly_consumption'] - row['wine_production']
    return float('inf') if net_consumption_rate <= 0 else round(row['wine_storage'] / net_consumption_rate, 2)
