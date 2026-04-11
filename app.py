import streamlit as st
import pandas as pd
import google.generativeai as genai

# 1. STYLE & PAGE SETUP
st.set_page_config(page_title="Titanic", page_icon="🚢")
st.markdown("<style>.stApp { background-color: #f5f5dc; } * { color: #000000 !important; font-family: 'Georgia', serif; }</style>", unsafe_allow_html=True)

# 2. LOAD DATA
SHEET_URL = "https://docs.google.com/spreadsheets/d/1ELXfthW0Eni6MGMWDjyGAaSreKuf0lj_7LAundUj1yY/export?format=csv&gid=1264206782"
df = pd.read_csv(SHEET_URL)

# 3. GET PASSENGER (From URL or Default)
query_name = st.query_params.get("passenger", "Lucille Carter")
p = df[df['Name'].str.contains(query_name, na=False)].iloc[0] if not df[df['Name'].str.contains(query_name, na=False)].empty else df.iloc[0]

# 4. DISPLAY THE SCREEN
st.title(f"🚢 {p['Name']}")
if 'ImageLink' in p and pd.notna(p['ImageLink']):
    st.image(p['ImageLink'], width=300)

# THIS LINE MUST COME BEFORE THE "IF USER_INPUT" BLOCK
user_input = st.text_input(f"Talk to {p['Name'].split()[0]}:")

# 5. THE AI BRAIN
if user_input:
    try:
        # Get the Key from Secrets
        K = st.secrets["GEMINI_KEY"].strip()
        genai.configure(api_key=K)
        
        # Use the absolute path name to prevent 404s
        model = genai.GenerativeModel('models/gemini-1.5-flash')
        
        persona = p.get('Bio & Roleplay (The Narrative)', 'A passenger on the Titanic.')
        prompt = f"You are {p['Name']} in 1912. {persona}. No knowledge of the sinking. Reply to: {user_input}"
        
        response = model.generate_content(prompt)
        st.write(f"**{p['Name']}:** {response.text}")
    except Exception as e:
        st.error(f"⚠️ {e}")
