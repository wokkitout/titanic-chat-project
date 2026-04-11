import streamlit as st
import pandas as pd
import google.generativeai as genai

# 1. SETUP
st.set_page_config(page_title="Titanic", page_icon="🚢")
st.markdown("<style>.stApp { background-color: #f5f5dc; } * { color: #000000 !important; font-family: 'Georgia', serif; }</style>", unsafe_allow_html=True)

# 2. DATA
SHEET_URL = "https://docs.google.com/spreadsheets/d/1ELXfthW0Eni6MGMWDjyGAaSreKuf0lj_7LAundUj1yY/export?format=csv&gid=1264206782"
df = pd.read_csv(SHEET_URL)
name = st.query_params.get("passenger", "Lucille Carter")
p = df[df['Name'].str.contains(name, na=False)].iloc[0] if not df[df['Name'].str.contains(name, na=False)].empty else df.iloc[0]

# 3. UI
st.title(f"🚢 {p['Name']}")
user_input = st.text_input(f"Talk to {p['Name'].split()[0]}:")

# 4. THE BRAIN (The "List Everything" Version)
if user_input:
    try:
        K = st.secrets["GEMINI_KEY"].strip()
        genai.configure(api_key=K)
        
        # This will show us EXACTLY what your account is allowed to use
        models = [m.name for m in genai.list_models()]
        
        # Let's try to find ANY model that contains the word 'gemini'
        target = next((m for m in models if 'gemini' in m.lower()), None)
        
        if target:
            model = genai.GenerativeModel(target)
            response = model.generate_content(f"You are {p['Name']} in 1912. Reply: {user_input}")
            st.write(f"**{p['Name']}:** {response.text}")
        else:
            st.warning(f"Your account doesn't see Gemini. Available models: {models}")
            
    except Exception as e:
        st.error(f"⚠️ {e}")
