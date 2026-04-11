import streamlit as st
import pandas as pd
import urllib.parse
import google.generativeai as genai

# --- 1. THE LOOK (Black text, No Bios) ---
st.set_page_config(page_title="Titanic", page_icon="🚢")
st.markdown("<style>.stApp { background-color: #f5f5dc; } * { color: #000000 !important; font-family: 'Georgia', serif; } .main-title { text-align: center; font-weight: bold; }</style>", unsafe_allow_html=True)

# --- 2. DATA ---
SHEET_URL = "https://docs.google.com/spreadsheets/d/1ELXfthW0Eni6MGMWDjyGAaSreKuf0lj_7LAundUj1yY/export?format=csv&gid=1264206782"
df = pd.read_csv(SHEET_URL)

try:
    raw_name = st.query_params.get("passenger", "Edward John Smith")
except:
    raw_name = st.experimental_get_query_params().get("passenger", ["Edward John Smith"])[0]

passenger_name = urllib.parse.unquote(raw_name).strip()
p = df[df['Name'].str.strip() == passenger_name].iloc[0] if not df[df['Name'].str.strip() == passenger_name].empty else df.iloc[0]

# --- 3. THE UI ---
st.markdown(f"<h1 class='main-title'>🚢 {p['Name']}</h1>", unsafe_allow_html=True)
if 'ImageLink' in p and pd.notna(p['ImageLink']):
    st.image(p['ImageLink'], use_container_width=True)

st.write("---")
user_input = st.text_input(f"Speak to {p['Name'].split()[0]}:")

# --- 4. THE AI BRAIN ---
if user_input:
    try:
        # PASTE YOUR NEW AIza KEY BELOW
        genai.configure(api_key="PASTE_YOUR_AIza_KEY_HERE")
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        # Use the roleplay column from your sheet
        persona = p.get('Bio & Roleplay (The Narrative)', "A passenger on the Titanic.")
        
        prompt = f"""
        You are {p['Name']} in April 1912. 
        Background: {persona}
        RULES:
        - You don't know the ship will sink.
        - You don't know what modern technology is.
        - Keep it to 2 sentences max.
        User said: {user_input}
        """
        
        response = model.generate_content(prompt)
        st.markdown(f"**{p['Name']}:** {response.text}")
        
    except Exception as e:
        st.error(f"Lucille is still quiet because: {e}")
    
