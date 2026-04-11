import streamlit as st
import pandas as pd
import urllib.parse

# --- 1. CONFIG & URL SETUP ---
# This is the "Engine" that finds your passengers
try:
    # Attempt to get the name from the URL (?passenger=Name)
    raw_name = st.query_params.get("passenger", "Edward John Smith")
except:
    # Fallback for older versions of Streamlit
    raw_name = st.experimental_get_query_params().get("passenger", ["Edward John Smith"])[0]

# IMPORTANT: This turns "Lucille%20Carter" back into "Lucille Carter"
passenger_name = urllib.parse.unquote(raw_name)

# --- 2. LOAD DATA ---
SHEET_URL = "https://docs.google.com/spreadsheets/d/1ELXfthW0Eni6MGMWDjyGAaSreKuf0lj_7LAundUj1yY/export?format=csv&gid=1264206782"

@st.cache_data(ttl=60)
def load_data():
    return pd.read_csv(SHEET_URL)

df = load_data()

# --- 3. FIND PASSENGER ---
passenger_data = df[df['Name'] == passenger_name]

# If we don't find them, default back to the Captain
if passenger_data.empty:
    passenger_data = df[df['Name'] == "Edward John Smith"]
    passenger_name = "Edward John Smith"

p = passenger_data.iloc[0]

# --- 4. DISPLAY PAGE ---
st.title(f"Titanic Passenger: {passenger_name}")

# This is where your image and bio code goes...
# (Keep the rest of your display code here)
