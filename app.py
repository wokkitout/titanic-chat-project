import streamlit as st
import pandas as pd
import urllib.parse

# --- 1. CONFIG & VINTAGE AESTHETICS ---
st.set_page_config(page_title="Titanic Manifest", page_icon="🚢")

st.markdown("""
    <style>
    .stApp { background-color: #f5f5dc; }
    .main-title { color: #2c3e50; font-family: 'Georgia', serif; text-align: center; }
    .wiki-text { 
        color: #1a1a1a; 
        font-family: 'Helvetica', sans-serif; 
        font-size: 1rem; 
        line-height: 1.5;
        background-color: #ffffff;
        padding: 15px;
        border-left: 5px solid #2c3e50;
    }
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

# --- 6. HISTORICAL RECORD (The Wikipedia Box) ---
st.subheader("White Star Line Archive")

# Instead of pulling the "Secret Bio", we show a generic "Public Info" summary
# You can update this text to be the Wikipedia summary for each person
wiki_summary = f"{p['Name']} was a passenger on the RMS Titanic. Records indicate they boarded at {p.get('Role / Class', 'the designated port')}. No further public records are available regarding their final destination."

st.markdown(f"<div class='wiki-text'>{wiki_summary}</div>", unsafe_allow_html=True)

# --- 7. THE AI CHAT (Where the persona lives) ---
st.write("---")
st.subheader(f"Inquire with {p['Name'].split()[0]}")
st.write("*Speak to the passenger to learn of their experiences and eventual fate.*")

user_input = st.text_input("Type your message:", placeholder="Are you worried about the ice?")

if user_input:
    # Here, your Gemini AI will use the 'Bio & Roleplay' column 
    # to answer, but the user CAN'T see that column on the screen!
    st.info(f"*{p['Name']} is typing a reply...*")
