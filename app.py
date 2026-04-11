import streamlit as st
import pandas as pd
import urllib.parse

# --- 1. CONFIG & VINTAGE AESTHETICS ---
st.set_page_config(page_title="Titanic Manifest", page_icon="🚢")

st.markdown("""
    <style>
    /* Background */
    .stApp { 
        background-color: #f5f5dc; 
    }
    
    /* Global Text Force-Black */
    html, body, [data-testid="stWidgetLabel"], [data-testid="stMarkdownContainer"] p, h1, h2, h3, span, li {
        color: #000000 !important;
        font-family: 'Georgia', serif;
    }

    .main-title { 
        color: #000000 !important;
        text-align: center; 
        margin-top: 20px;
        font-weight: bold;
        font-size: 2.2rem;
    }

    /* Input Box Styling - Black text on White background */
    .stTextInput input {
        color: #000000 !important;
        background-color: #ffffff !important;
        border: 2px solid #000000 !important;
    }

    /* Remove default Streamlit padding at the top */
    .block-container {
        padding-top: 1rem;
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

# --- 5. DISPLAY PORTRAIT ---
st.markdown(f"<h1 class='main-title'>🚢 {p['Name']}</h1>", unsafe_allow_html=True)

if 'ImageLink' in p and pd.notna(p['ImageLink']):
    st.image(p['ImageLink'], use_container_width=True)

# --- 6. THE IMMERSIVE SETTING ---
st.write("---")
st.markdown(f"**Location:** R.M.S. Titanic — At Sea")
st.markdown(f"**Date:** April 14, 1912")
st.write(f"You approach {p['Name'].split()[0]} on the deck. The ship is steady, and the evening air is crisp. They seem quite content with the voyage.")

# --- 7. CHAT INPUT ---
user_input = st.text_input(f"Address {p['Name'].split()[0]}:", placeholder="Say something...")

if user_input:
    # When you add Gemini logic, ensure your System Prompt says:
    # 'You are {p["Name"]}. You are currently on the Titanic. You believe 
    # the ship is unsinkable. You are excited about your arrival in New York.
    # You have NO idea what an iceberg or a shipwreck is.'
    st.markdown(f"**{p['Name']} looks up to answer you...**")
