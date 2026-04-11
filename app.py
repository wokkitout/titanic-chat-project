import streamlit as st
import pandas as pd
import urllib.parse
import google.generativeai as genai

# --- 1. THE LOOK ---
st.set_page_config(page_title="Titanic", page_icon="🚢")
st.markdown("<style>.stApp { background-color: #f5f5dc; } * { color: #000000 !important; font-family: 'Georgia', serif; } .main-title { text-align: center; font-weight: bold; }</style>", unsafe_allow_html=True)

# --- 2. THE DATA ---
SHEET_URL = "https://docs.google.com/spreadsheets/d/1ELXfthW0Eni6MGMWDjyGAaSreKuf0lj_7LAundUj1yY/export?format=csv&gid=1264206782"
df = pd.read_csv(SHEET_URL)

try:
    raw_name = st.query_params.get("passenger", "Lucille Carter")
except:
    raw_name = st.experimental_get_query_params().get("passenger", ["Lucille Carter"])[0]

passenger_name = urllib.parse.unquote(raw_name).strip()
p = df[df['Name'].str.strip() == passenger_name].iloc[0] if not df[df['Name'].str.strip() == passenger_name].empty else df.iloc[0]

# --- 3. THE UI ---
st.markdown(f"<h1 class='main-title'>🚢 {p['Name']}</h1>", unsafe_allow_html=True)
if 'ImageLink' in p and pd.notna(p['ImageLink']):
    st.image(p['ImageLink'], use_container_width=True)

st.write("---")
user_input = st.text_input(f"Speak to {p['Name'].split()[0]}:")

# --- 4. THE AI (LUCILE'S BRAIN) ---
if user_input:
    try:
        # Pulling the key from the SECRETS you just set up
        API_KEY = st.secrets["GEMINI_KEY"]
        genai.configure(api_key=API_KEY)
        
        # Using the absolute most stable model name
        model = genai.GenerativeModel('gemini-1.5-flash-latest')
        
        persona = p.get('Bio & Roleplay (The Narrative)', "A passenger on the Titanic.")
        prompt = f"You are {p['Name']} on the Titanic in 1912. {persona}. You are oblivious to the sinking. Keep it to 2 sentences. User says: {user_input}"
        
        response = model.generate_content(prompt)
        st.markdown(f"**{p['Name']}:** {response.text}")
        
    except Exception as e:
        # If this still fails, it's a settings issue in Google AI Studio
        st.error(f"⚠️ Connection Error: {e}")

# --- 5. THE AI (STRICT CONNECTION) ---
if user_input:
    try:
        # Get the key from Secrets
        raw_key = st.secrets["GEMINI_KEY"]
        # .strip() cleans up any accidental spaces from copying/pasting
        genai.configure(api_key=raw_key.strip())
        
        # We use 'gemini-1.5-flash' because 'flash-latest' was causing that 404 error
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        persona = p.get('Bio & Roleplay (The Narrative)', "A passenger on the Titanic.")
        
        prompt = f"""
        You are {p['Name']} in April 1912. 
        Background: {persona}
        Stay in character. You think the ship is unsinkable. 
        No modern talk. Keep it to 2 sentences.
        User says: {user_input}
        """
        
        response = model.generate_content(prompt)
        
        # This displays the actual answer in bold black text
        st.markdown(f"**{p['Name']}:** {response.text}")
        
    except Exception as e:
        # This will now only show ONE error box if something goes wrong
        st.error(f"⚠️ Connection Error: {e}")
