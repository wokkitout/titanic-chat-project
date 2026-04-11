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
if 'ImageLink' in p and pd.notna(p['ImageLink']):
    st.image(p['ImageLink'], width=300)

# Define user_input FIRST
user_input = st.text_input(f"Talk to {p['Name'].split()[0]}:")

# 4. THE BRAIN
if user_input:
    try:
        K = st.secrets["GEMINI_KEY"].strip()
        genai.configure(api_key=K)
        
        # We use the FULL path. This is the only way to kill a 404 error.
        model = genai.GenerativeModel('models/gemini-1.5-flash')
        
        response = model.generate_content(f"You are {p['Name']} in 1912. Reply: {user_input}")
        st.write(f"**{p['Name']}:** {response.text}")
    except Exception as e:
        st.error(f"⚠️ {e}")
