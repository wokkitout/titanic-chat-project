import streamlit as st
import pandas as pd
import urllib.parse
import google.generativeai as genai

# --- 1. THE VIBE (Black Text, Beige Paper) ---
st.set_page_config(page_title="Titanic Manifest", page_icon="🚢")
st.markdown("""
    <style>
    .stApp { background-color: #f5f5dc; }
    * { color: #000000 !important; font-family: 'Georgia', serif; }
    .main-title { text-align: center; font-weight: bold; font-size: 2rem; }
    input { color: #000000 !important; background-color: #ffffff !important; }
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
p_row = df[df['Name_Clean'] == passenger_name]
p = p_row.iloc[0] if not p_row.empty else df.iloc[0]

# --- 4. THE SCREEN ---
st.markdown(f"<h1 class='main-title'>🚢 {p['Name']}</h1>", unsafe_allow_html=True)
if 'ImageLink' in p and pd.notna(p['ImageLink']):
    st.image(p['ImageLink'], use_container_width=True)

st.write("---")
user_input = st.text_input(f"Speak to {p['Name'].split()[0]}:", key="chat")

# --- 5. THE AI (LUCILE'S BRAIN) ---
if user_input:
    try:
        # 🔑 KEY CHECK: Ensure there are no spaces inside the quotes!
        genai.configure(api_key="PASTE_YOUR_AIZA_KEY_HERE")
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        # Pull the secret persona
        secret_persona = p.get('Bio & Roleplay (The Narrative)', "A passenger on the Titanic.")
        
        prompt = f"""
        You are {p['Name']} in April 1912. 
        Background: {secret_persona}
        - You are OBLIVIOUS to the sinking. You think the ship is unsinkable.
        - You have no knowledge of modern tech (phones/internet).
        - Use 1912 language. Keep it to 2 sentences.
        User says: {user_input}
        """
        
        response = model.generate_content(prompt)
        st.markdown(f"**{p['Name']}:** {response.text}")
        
    except Exception as e:
        st.error(f"Lucille is still quiet because: {e}")
