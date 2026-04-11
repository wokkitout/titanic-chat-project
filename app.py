import streamlit as st
import pandas as pd
import urllib.parse

# --- 1. CONFIG & VINTAGE AESTHETICS ---
st.set_page_config(page_title="Titanic Manifest", page_icon="🚢")

st.markdown("""
    <style>
    .stApp { background-color: #f5f5dc; } /* Vintage Paper Beige */
    .main-title { 
        color: #2c3e50; 
        font-family: 'Georgia', serif; 
        text-align: center; 
        margin-top: 20px;
    }
    .stTextInput label {
        font-family: 'Georgia', serif;
        color: #2c3e50;
        font-weight: bold;
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

# --- 6. THE CONVERSATION (No Bio, No Spoilers) ---
st.write("---")
st.subheader(f"Speak with {p['Name'].split()[0]}")

# Instructions for the user
st.write(f"*You are standing on the deck of the RMS Titanic. {p['Name'].split()[0]} is looking out at the horizon.*")

user_input = st.text_input("Address the passenger:", placeholder="Good evening, how are you enjoying the voyage?")

if user_input:
    # --- 7. THE AI PROMPT (The "Time Travel" Rules) ---
    # When you add your Gemini logic, make sure the system prompt is set like this:
    # "You are {p['Name']}. It is April 1912. You are on the Titanic.
    # You have NO knowledge of the future. You don't know what a 'cell phone', 
    # 'internet', 'Wi-Fi', or 'AI' is. If asked about these things, you should 
    # be confused or assume they are some strange new slang from America. 
    # Use the 'Bio & Roleplay' column from the sheet for your history, but 
    # NEVER reveal your fate (living or dying) unless it is happening in the moment."
    
    st.info(f"*{p['Name']} is looking at you, preparing a response...*")
