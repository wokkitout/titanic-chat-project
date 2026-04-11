import streamlit as st
import pandas as pd
import urllib.parse

# --- 1. PAGE CONFIG ---
st.set_page_config(page_title="Titanic Manifest", page_icon="🚢")

# --- 2. URL DATA DECODER ---
# This section captures the name from the QR code and fixes symbols like %20
try:
    # Handles newest Streamlit version
    raw_name = st.query_params.get("passenger", "Edward John Smith")
except:
    # Fallback for older Streamlit versions
    raw_name = st.experimental_get_query_params().get("passenger", ["Edward John Smith"])[0]

# Convert "Lucille%20Carter" -> "Lucille Carter" and remove any extra spaces
passenger_name = urllib.parse.unquote(raw_name).strip()

# --- 3. DATA LOADING ---
# Replace this with your actual Google Sheet CSV Export link
SHEET_URL = "https://docs.google.com/spreadsheets/d/1ELXfthW0Eni6MGMWDjyGAaSreKuf0lj_7LAundUj1yY/export?format=csv&gid=1264206782"

@st.cache_data(ttl=60)
def load_data():
    return pd.read_csv(SHEET_URL)

df = load_data()

# --- 4. PASSENGER LOOKUP ---
# We strip spaces from the spreadsheet column too, just to be safe
passenger_data = df[df['Name'].str.strip() == passenger_name]

# If the name from the QR isn't found, show the Captain
if passenger_data.empty:
    p = df[df['Name'].str.strip() == "Edward John Smith"].iloc[0]
else:
    p = passenger_data.iloc[0]

# --- 5. DISPLAY PASSENGER PAGE ---
st.title(f"{p['Name']}")

# Display Image
if 'ImageLink' in p and pd.notna(p['ImageLink']):
    st.image(p['ImageLink'], use_container_width=True)
else:
    st.warning("No portrait available for this passenger.")

# Display Bio
st.subheader("Biography")
st.write(p['Biography'])

# --- 6. CHAT FEATURE (OPTIONAL) ---
# If you have your Gemini chat code, you would place it here, 
# using p['Biography'] as the context for the AI.
