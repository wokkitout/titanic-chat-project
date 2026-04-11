import streamlit as st
import pandas as pd
import urllib.parse
import google.generativeai as genai

# --- 1. CONFIG & AESTHETICS ---
st.set_page_config(page_title="Titanic Manifest", page_icon="🚢")

st.markdown("""
    <style>
    .stApp { background-color: #f5f5dc; }
    html, body, [data-testid="stWidgetLabel"], p, h1, h2, h3, span {
        color: #000000 !important;
        font-family: 'Georgia', serif;
    }
    .main-title { text-align: center; margin-top: 20px; font-weight: bold; }
    .stTextInput input { color: #000000 !important; border: 2px solid #000000 !important; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. DATA LOADING ---
SHEET_URL = "https://docs.google.com/spreadsheets/d/1ELXfthW0Eni6MGMWDjyGAaSreKuf0lj_7LAundUj1yY/export?format=csv&gid=1264206782"

@st.cache_data(ttl=60)
def load_data():
    return pd.read_csv(SHEET_URL)

df = load_data()

# --- 3. PASSENGER LOOKUP ---
try:
    raw_name = st.query_params.get("passenger", "Edward John Smith")
except:
    raw_name = st.experimental_get_query_params().get("passenger", ["Edward John Smith"])[0]

passenger_name = urllib.parse.unquote(raw_name).strip()
df['Name_Clean'] = df['Name'].astype(str).str.strip()
passenger_data = df[df['Name_Clean'] == passenger_name]
p = passenger_data.iloc[0] if not passenger_data.empty else df.iloc[0]

# --- 4. DISPLAY HEADER & IMAGE ---
st.markdown(f"<h1 class='main-title'>🚢 {p['Name']}</h1>", unsafe_allow_html=True)
if 'ImageLink' in p and pd.notna(p['ImageLink']):
    st.image(p['ImageLink'], use_container_width=True)

st.write("---")

# --- 5. THE CHAT LOGIC ---
user_input = st.text_input(f"Speak to {p['Name'].split()[0]}:", key="input")

if user_input:
    # We define the model RIGHT HERE so it can't be 'undefined'
    try:
        # PASTE YOUR KEY INSIDE THE QUOTES BELOW
        genai.configure(api_key="AIzaSy...") 
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        persona = p.get('Bio & Roleplay (The Narrative)', "A passenger on the Titanic.")
        
        prompt = f"""
        You are {p['Name']} in April 1912. 
        Background: {persona}
        
        RULES:
        - You are OBLIVIOUS to the sinking. The ship is unsinkable.
        - You have no knowledge of modern technology.
        - Stay in character. Keep it to 2 sentences.
        
        User says: {user_input}
        """
        
        response = model.generate_content(prompt)
        st.markdown(f"**{p['Name']}:** {response.text}")
        
    except Exception as e:
        st.error(f"Lucille is still quiet because: {e}")
