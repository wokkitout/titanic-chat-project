import streamlit as st
import pandas as pd
import urllib.parse

# --- 1. PAGE CONFIG & AESTHETICS ---
st.set_page_config(page_title="Titanic Manifest", page_icon="🚢")

# This brings back your beige background and custom styling
st.markdown("""
    <style>
    .stApp {
        background-color: #f5f5dc; /* Classic Beige */
    }
    .main-title {
        color: #2c3e50;
        font-family: 'Georgia', serif;
        text-align: center;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. URL DECODER (The Lucille Fix) ---
try:
    raw_name = st.query_params.get("passenger", "Edward John Smith")
except:
    raw_name = st.experimental_get_query_params().get("passenger", ["Edward John Smith"])[0]

passenger_name = urllib.parse.unquote(raw_name).strip()

# --- 3. DATA LOADING ---
SHEET_URL = "https://docs.google.com/spreadsheets/d/1ELXfthW0Eni6MGMWDjyGAaSreKuf0lj_7LAundUj1yY/export?format=csv&gid=1264206782"

@st.cache_data(ttl=60)
def load_data():
    return pd.read_csv(SHEET_URL)

df = load_data()

# --- 4. PASSENGER LOOKUP ---
passenger_data = df[df['Name'].str.strip() == passenger_name]

if passenger_data.empty:
    p = df[df['Name'].str.strip() == "Edward John Smith"].iloc[0]
else:
    p = passenger_data.iloc[0]

# --- 5. DISPLAY HEADER ---
st.markdown(f"<h1 class='main-title'>🚢 {p['Name']}</h1>", unsafe_allow_html=True)
st.write("---")

# --- 6. PASSENGER IMAGE ---
if 'ImageLink' in p and pd.notna(p['ImageLink']):
    st.image(p['ImageLink'], use_container_width=True)
else:
    st.warning("Portrait not found in archives.")

# --- 7. BIOGRAPHY ---
st.subheader("Passenger Details")
st.info(p['Biography'])

# --- 8. THE CHAT BOX (Restored) ---
st.write("---")
st.subheader(f"Speak with {p['Name'].split()[0]}")

# Placeholder for your chat input
user_input = st.text_input("Ask a question about my journey:", placeholder="What is your cabin like?")

if user_input:
    # This is where your Gemini API logic would trigger
    st.write(f"*{p['Name']} is thinking...*")
    # (Insert your specific Gemini chat code here)
