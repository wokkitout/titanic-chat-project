import streamlit as st
import pandas as pd
import urllib.parse
import google.generativeai as genai

# --- 1. SETTINGS & STYLE ---
st.set_page_config(page_title="Titanic Manifest", page_icon="🚢")
st.markdown("""
    <style>
    .stApp { background-color: #f5f5dc; }
    * { color: #000000 !important; font-family: 'Georgia', serif; }
    .main-title { text-align: center; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. LOAD DATA ---
SHEET_URL = "https://docs.google.com/spreadsheets/d/1ELXfthW0Eni6MGMWDjyGAaSreKuf0lj_7LAundUj1yY/export?format=csv&gid=1264206782"

@st.cache_data
def load_data():
    return pd.read_csv(SHEET_URL)

df = load_data()

# --- 3. FIND PASSENGER ---
# st.query_params is a dict-like object in modern Streamlit (1.30+)
raw_name = st.query_params.get("passenger", "Lucille Carter")
passenger_name = urllib.parse.unquote(raw_name).strip()

p_row = df[df['Name'].str.strip() == passenger_name]
p = p_row.iloc[0] if not p_row.empty else df.iloc[0]

# --- 4. DISPLAY ---
st.markdown(f"<h1 class='main-title'>🚢 {p['Name']}</h1>", unsafe_allow_html=True)

if 'ImageLink' in df.columns and pd.notna(p['ImageLink']):
    st.image(p['ImageLink'], use_container_width=True)

st.write("---")

user_input = st.text_input(f"Speak to {p['Name'].split()[0]}:", key="user_msg")

# --- 5. THE BRAIN ---
if user_input:
    try:
        api_key = st.secrets["GEMINI_KEY"]
        genai.configure(api_key=api_key.strip())

        model = genai.GenerativeModel('gemini-1.5-flash')

        bio_col = 'Bio & Roleplay (The Narrative)'
        persona = p[bio_col] if bio_col in df.columns and pd.notna(p[bio_col]) else "
