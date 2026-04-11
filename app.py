import streamlit as st
import pandas as pd
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
    query_name = st.query_params.get("passenger", "Lucille Carter")
except:
    query_name = "Lucille Carter"

p_row = df[df['Name'].str.contains(query_name, na=False)]
p = p_row.iloc[0] if not p_row.empty else df.iloc[0]

# --- 4. THE UI (IMAGE & TITLE) ---
st.markdown(f"<h1 class='main-title'>🚢 {p['Name']}</h1>", unsafe_allow_html=True)

# Checks for the image column (handles both 'ImageLink' and 'Image Link')
img_col = 'ImageLink' if 'ImageLink' in p else 'Image Link'
if img_col in p and pd.notna(p[img_col]):
    st.image(p[img_col], width=300)
else:
    st.write("📷 *[Portrait unavailable in manifest]*")

st.write("---")
user_input = st.text_input(f"Speak to {p['Name'].split()[0]}:")

# --- 5. THE BRAIN (1912 MODE) ---
if user_input:
    try:
        K = st.secrets["GEMINI_KEY"].strip()
        genai.configure(api_key=K)
        
        # SELF-HEALING SCANNER: Automatically finds the correct model name for your region
        available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        target = next((m for m in available_models if 'gemini-1.5-flash' in m), available_models[0])
        model = genai.GenerativeModel(target)
        
        # Pulls the 6-sentence bio from your Google Sheet
        persona = p.get('Bio & Roleplay (The Narrative)', "A passenger on the Titanic.")
        
        # The prompt that keeps them in 1912
        prompt = f"""
        STRICT ROLEPLAY RULE: The current date is April 10, 1912. 
        You are currently aboard the Titanic, which has just begun its maiden voyage.
        You have NO KNOWLEDGE of any sinking, iceberg, or disaster.
        If the user mentions a tragedy, act confused—to you, this ship is unsinkable.
        
        Your identity: {p['Name']}
        Background: {persona}
        User's message: {user_input}
        """
        
        response = model.generate_content(prompt)
        st.markdown(f"**{p['Name']}:** {response.text}")
        
    except Exception as e:
        st.error(f"⚠️ Connection Error: {e}")
