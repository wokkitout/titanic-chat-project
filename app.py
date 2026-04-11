import streamlit as st
import pandas as pd
import google.generativeai as genai

# 1. SETUP
st.set_page_config(page_title="Titanic", page_icon="🚢")
st.markdown("<style>.stApp { background-color: #f5f5dc; } * { color: #000000 !important; font-family: 'Georgia', serif; }</style>", unsafe_allow_html=True)

# 2. DATA
SHEET_URL = "https://docs.google.com/spreadsheets/d/1ELXfthW0Eni6MGMWDjyGAaSreKuf0lj_7LAundUj1yY/export?format=csv&gid=1264206782"

@st.cache_data
def get_data():
    return pd.read_csv(SHEET_URL)

df = get_data()
name = st.query_params.get("passenger", "Lucille Carter")
p = df[df['Name'].str.contains(name, na=False)].iloc[0] if not df[df['Name'].str.contains(name, na=False)].empty else df.iloc[0]

# 3. UI
st.title(f"🚢 {p['Name']}")
if 'ImageLink' in p and pd.notna(p['ImageLink']):
    st.image(p['ImageLink'], width=300)

user_input = st.text_input(f"Talk to {p['Name'].split()[0]}:")

# 4. THE BRAIN (Self-Healing Version)
if user_input:
    try:
        K = st.secrets["GEMINI_KEY"].strip()
        genai.configure(api_key=K)
        
        # This checks which models YOUR key can actually see
        available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        
        # Priority: 1.5 Flash -> 1.5 Flash-8b -> Pro
        target_model = None
        for m in ['models/gemini-1.5-flash', 'models/gemini-1.5-flash-8b', 'models/gemini-pro']:
            if m in available_models:
                target_model = m
                break
        
        if target_model:
            model = genai.GenerativeModel(target_model)
            response = model.generate_content(f"You are {p['Name']} in 1912. Reply: {user_input}")
            st.write(f"**{p['Name']}:** {response.text}")
        else:
            st.error("No compatible models found on your account.")
            
    except Exception as e:
        st.error(f"⚠️ {e}")
