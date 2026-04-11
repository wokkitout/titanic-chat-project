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
try:
    raw_name = st.query_params.get("passenger", "Lucille Carter")
except:
    raw_name = st.experimental_get_query_params().get("passenger", ["Lucille Carter"])[0]

passenger_name = urllib.parse.unquote(raw_name).strip()
p_row = df[df['Name'].str.strip() == passenger_name]
p = p_row.iloc[0] if not p_row.empty else df.iloc[0]

# --- 4. DISPLAY ---
st.markdown(f"<h1 class='main-title'>🚢 {p['Name']}</h1>", unsafe_allow_html=True)
if 'ImageLink' in p and pd.notna(p['ImageLink']):
    st.image(p['ImageLink'], use_container_width=True)

st.write("---")
user_input = st.text_input(f"Speak to {p['Name'].split()[0]}:", key="user_msg")

# --- 5. THE BRAIN ---
if user_input:
    try:
        # We fetch the key from the SECRETS menu, not the code
        api_key = st.secrets["GEMINI_KEY"]
        genai.configure(api_key=api_key.strip())
        
        # Standard model name to avoid 404 errors
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        persona = p.get('Bio & Roleplay (The Narrative)', "A passenger on the Titanic.")
        prompt = f"You are {p['Name']} in April 1912. {persona}. You don't know the ship sinks. Reply to: {user_input}"
        
        response = model.generate_content(prompt)
        st.markdown(f"**{p['Name']}:** {response.text}")
    except Exception as e:
        st.error(f"⚠️ Connection Error: {e}")
