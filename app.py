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

# --- FIND PASSENGER (Updated with .strip()) ---
# This ignores accidental spaces in the URL or the Spreadsheet
passenger_name_clean = passenger_name.strip()
passenger_data = df[df['Name'].str.strip() == passenger_name_clean]

# If we don't find them, default back to the Captain
if passenger_data.empty:
    passenger_data = df[df['Name'] == "Edward John Smith"]
    # We keep the Captain's data but we'll show the name we TRIED to find 
    # so we can debug it on your screen!
    display_name = f"NOT FOUND: {passenger_name_clean}"
else:
    display_name = passenger_name_clean
    p = passenger_data.iloc[0]

st.title(f"Titanic Passenger: {display_name}")

# If we don't find them, default back to the Captain
if passenger_data.empty:
    passenger_data = df[df['Name'] == "Edward John Smith"]
    passenger_name = "Edward John Smith"

p = passenger_data.iloc[0]

# --- 4. DISPLAY PAGE ---
st.title(f"Titanic Passenger: {passenger_name}")

# This is where your image and bio code goes...
# (Keep the rest of your display code here)
