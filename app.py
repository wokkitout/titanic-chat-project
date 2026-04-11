import streamlit as st
import pandas as pd
import urllib.parse
import google.generativeai as genai

# --- 1. THE LOOK ---
st.set_page_config(page_title="Titanic", page_icon="🚢")
st.markdown("<style>.stApp { background-color: #f5f5dc; } * { color: #000000 !important; font-family: 'Georgia', serif; } .main-title { text-align: center; font-weight: bold; }</style>", unsafe_allow_html=True)

# --- 2. THE DATA ---
SHEET_URL = "https://docs.google.com/spreadsheets/d/1ELXfthW0Eni6MGMWDjyGAaSreKuf0lj_7LAundUj1yY/export?format=csv&gid=1264206782"

@st.cache_data(ttl=60)
def load_data():
    return pd.read_csv(SHEET_URL)

df = load_data()

# --- 3. PASSENGER LOOKUP ---
try:
    raw_name = st.query_params.get("passenger", "Lucille Carter")
except:
    raw_name = st.experimental_get_query_params().get("passenger", ["Lucille Carter"])[0]

passenger_name = urllib.parse.unquote(raw_name).strip()
p = df[df['Name'].str.strip() == passenger_name].iloc[0] if not df[df['Name'].str.strip() == passenger_name].empty else df.iloc[0]

# --- 4. THE UI ---
st.markdown(f"<h1 class='main-title'>🚢 {p['Name']}</h1>", unsafe_allow_html=True)
if 'ImageLink' in p and pd.notna(p['ImageLink']):
    st.image(p['ImageLink'], use_container_width=True)

st.write("---")
user_input = st.text_input(f"Speak to {p['Name'].split()[0]}:", placeholder="Enter your message...")

# --- 5. THE AI (REWRITTEN CONNECTION) ---
if user_input:
    # 🔑 PASTE YOUR CLEAN KEY HERE
    API_KEY = "PASTE_YOUR_AIza_KEY_HERE"
    
    try:
        # We configure it right here to ensure it's fresh
        genai.configure(api_key=API_KEY.strip())
        
        # We'll try 'gemini-1.5-flash-latest'—it's very reliable for new keys
        model = genai.GenerativeModel('gemini-1.5-flash-latest')
        
        persona = p.get('Bio & Roleplay (The Narrative)', "A passenger on the Titanic.")
        prompt = f"You are {p['Name']} on the Titanic in 1912. {persona}. No future knowledge. Stay in character. User says: {user_input}"
        
        # Adding a timeout/retry feel
        response = model.generate_content(prompt)
        
        if response:
            st.markdown(f"**{p['Name']}:** {response.text}")
            
    except Exception as e:
        # If this still says '400', the API isn't enabled in Google Cloud
        st.error(f"⚠️ Connection Error: {e}")
        st.info("If it says 'API key not valid', go to AI Studio, click 'Get API Key', and make sure you create a 'New Key in a NEW Project'.")
