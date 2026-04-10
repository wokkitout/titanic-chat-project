import streamlit as st
from google import genai
import pandas as pd

# --- 1. CONNECT TO YOUR GOOGLE SHEET ---
# Replace this with your Google Sheet URL
SHEET_URL = "https://docs.google.com/spreadsheets/d/1ELXfthW0Eni6MGMWDjyGAaSreKuf0lj_7LAundUj1yY/export?format=csv"

@st.cache_data
def load_data():
    df = pd.read_csv(SHEET_URL)
    # Convert the sheet into a dictionary the app can use
    return df.set_index('Name').to_dict('index')

passengers_data = load_data()

# --- 2. IDENTIFY PASSENGER FROM URL ---
query_params = st.query_params
# Use the passenger name from the URL or default to Captain Smith
p_name = query_params.get("p", "Capt. E.J. Smith") 
person = passengers_data.get(p_name, passengers_data["Capt. E.J. Smith"])

st.title(f"🚢 {p_name}")

# --- 3. EXTRACT AND DISPLAY IMAGE ---
# This pulls whatever URL you put in the '@images (File Path)' column
image_url = person.get("@images (File Path)")
if image_url and image_url.startswith("http"):
    st.image(image_url, width=250)
