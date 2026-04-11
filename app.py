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

# --- 2. BRAIN SETUP ---
# Get your key from https://aistudio.google.com/
genai.configure(api_key="PASTE_YOUR_KEY_HERE")
model = genai.GenerativeModel('gemini-1.5-flash')

# --- 3. DATA LOADING ---
SHEET_URL = "https://docs.google.com/spreadsheets/d/1ELXfthW0Eni6MGMWDjyGAaSreKuf0lj_7LAundUj1yY/export?format=csv&gid=1264206782"

@st.cache_data(ttl=60)
def load_data():
    return pd.read_csv(SHEET_URL)

df = load_data()

# --- 4. THE "NO-CRASH" PASSENGER LOOKUP ---
try:
    raw_name = st.query_params.get("passenger", "Edward John Smith")
except:
    raw_name = st.experimental_get_query_params().get("passenger", ["Edward John Smith"])[0]

passenger_name = urllib.parse.unquote(raw_name).strip()

# Fuzzy search to prevent that red IndexError
df['Name_Clean'] = df['Name'].astype(str).str.strip()
passenger_data = df[df['Name_Clean'] == passenger_name]

if not passenger_data.empty:
    p = passenger_data.iloc[0]
else:
    # If it can't find the name, just grab the first row so it doesn't crash
    p = df.iloc[0]

# --- 5. DISPLAY ---
st.markdown(f"<h1 class='main-title'>🚢 {p['Name']}</h1>", unsafe_allow_html=True)
if 'ImageLink' in p and pd.notna(p['ImageLink']):
    st.image(p['ImageLink'], use_container_width=True)

st.write("---")
st.write(f"*It is April 14, 1912. {p['Name'].split()[0]} is standing nearby.*")

# --- 6. THE CONVERSATION ---
user_input = st.text_input(f"Speak to {p['Name'].split()[0]}:", key="chat_input")

if user_input:
    # Use the long bio column name we found earlier
    persona = p.get('Bio & Roleplay (The Narrative)', "A passenger on the Titanic.")
    
    prompt = f"""
    You are {p['Name']}, a passenger on the Titanic in April 1912.
    Your history: {persona}
    
    RULES:
    1. You are OBLIVIOUS to the sinking. You think the ship is unsinkable.
    2. No modern tech talk.
    3. Stay in 1912 character.
    4. Keep it to 2 sentences.
    
    User says: {user_input}
    """
    
    try:
        response = model.generate_content(prompt)
        st.markdown(f"**{p['Name']}:** {response.text}")
    except Exception as e:
        st.error("The passenger is silent. Check if your Gemini API Key is valid!")
