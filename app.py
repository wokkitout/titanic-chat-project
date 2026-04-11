import streamlit as st
import pandas as pd
import google.generativeai as genai

# --- 1. SETTINGS & STYLE ---
st.set_page_config(page_title="Titanic Manifest", page_icon="🚢")
st.markdown("<style>.stApp { background-color: #f5f5dc; } * { color: #000000 !important; font-family: 'Georgia', serif; } .main-title { text-align: center; font-weight: bold; }</style>", unsafe_allow_html=True)

# --- 2. LOAD DATA ---
SHEET_URL = "https://docs.google.com/spreadsheets/d/1ELXfthW0Eni6MGMWDjyGAaSreKuf0lj_7LAundUj1yY/export?format=csv&gid=1264206782"
df = pd.read_csv(SHEET_URL)

# --- 3. PASSENGER LOOKUP ---
try:
    query_name = st.query_params.get("passenger", "Lucille Carter")
except:
    query_name = "Lucille Carter"

p = df[df['Name'].str.contains(query_name, na=False)].iloc[0] if not df[df['Name'].str.contains(query_name, na=False)].empty else df.iloc[0]

# --- 4. THE UI ---
st.markdown(f"<h1 class='main-title'>🚢 {p['Name']}</h1>", unsafe_allow_html=True)
if 'ImageLink' in p and pd.notna(p['ImageLink']):
    st.image(p['ImageLink'], width=300)

user_input = st.text_input(f"Speak to {p['Name'].split()[0]}:", key="chat_input")

# --- 5. THE BRAIN (THE STABLE VERSION) ---
if user_input:
    try:
        # Pull key from secrets
        API_KEY = st.secrets["GEMINI_KEY"].strip()
        genai.configure(api_key=API_KEY)
        
        # We are switching to 'gemini-pro'. 
        # It is the most 'standard' model name and bypasses the 404 error.
        model = genai.GenerativeModel('gemini-pro')
        
        persona = p.get('Bio & Roleplay (The Narrative)', "A passenger on the Titanic.")
        prompt = f"You are {p['Name']} in April 1912. {persona}. You don't know the ship will sink. Reply to: {user_input}"
        
        response = model.generate_content(prompt)
        st.markdown(f"**{p['Name']}:** {response.text}")
        
    except Exception as e:
        # If this STILL 404s, we will try the 'models/gemini-pro' path
        st.error(f"⚠️ Connection Error: {e}")
