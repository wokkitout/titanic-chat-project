import streamlit as st
import pandas as pd
import urllib.parse

# --- 1. CONFIG & AESTHETICS ---
st.set_page_config(page_title="Titanic Manifest", page_icon="🚢")

st.markdown("""
    <style>
    .stApp { background-color: #f5f5dc; }
    .main-title { color: #2c3e50; font-family: 'Georgia', serif; text-align: center; }
    .bio-box { background-color: white; padding: 20px; border-radius: 10px; border: 1px solid #d3d3d3; color: black; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. URL DECODER ---
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
p = passenger_data.iloc[0] if not passenger_data.empty else df[df['Name'].str.strip() == "Edward John Smith"].iloc[0]

# --- 5. DISPLAY HEADER & IMAGE ---
st.markdown(f"<h1 class='main-title'>🚢 {p['Name']}</h1>", unsafe_allow_html=True)
st.write("---")

if 'ImageLink' in p and pd.notna(p['ImageLink']):
    st.image(p['ImageLink'], use_container_width=True)

# --- 6. BIOGRAPHY (The Specific Match) ---
st.subheader("Passenger Details")

# We use the exact name we found in your debug list
target_col = 'Bio & Roleplay (The Narrative)'

if target_col in p:
    st.markdown(f"<div class='bio-box'>{p[target_col]}</div>", unsafe_allow_html=True)
else:
    st.error(f"Column '{target_col}' not found. Check your sheet headers!")

# --- 7. CHAT BOX ---
st.write("---")
st.subheader(f"Speak with {p['Name'].split()[0]}")
user_input = st.text_input("Ask about my life or the ship:", placeholder="What class are you traveling in?")
if user_input:
    st.info(f"*{p['Name']} is considering your question...*")
