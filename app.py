import streamlit as st
import pandas as pd
import google.generativeai as genai

# 1. Page Styling
st.set_page_config(page_title="Titanic", page_icon="🚢")
st.markdown("<style>.stApp { background-color: #f5f5dc; } * { color: #000000 !important; font-family: 'Georgia', serif; }</style>", unsafe_allow_html=True)

# 2. Load the Manifest
SHEET_URL = "https://docs.google.com/spreadsheets/d/1ELXfthW0Eni6MGMWDjyGAaSreKuf0lj_7LAundUj1yY/export?format=csv&gid=1264206782"
df = pd.read_csv(SHEET_URL)

# 3. Find Passenger
query_name = st.query_params.get("passenger", "Lucille Carter")
p = df[df['Name'].str.contains(query_name, na=False)].iloc[0] if not df[df['Name'].str.contains(query_name, na=False)].empty else df.iloc[0]

# 4. The Screen
st.title(f"🚢 {p['Name']}")
if 'ImageLink' in p and pd.notna(p['ImageLink']):
    st.image(p['ImageLink'], width=300)

user_input = st.text_input(f"Speak to {p['Name'].split()[0]}:")

# 5. The Brain (Using the Secret Key)
if user_input:
    try:
        # We look for the key in Streamlit Secrets, NOT the code
        api_key = st.secrets["GEMINI_KEY"]
        genai.configure(api_key=api_key.strip())
        model = genai.GenerativeModel('gemini-pro')
        
        persona = p.get('Bio & Roleplay (The Narrative)', "A passenger on the Titanic.")
        prompt = f"You are {p['Name']} in 1912. {persona}. You think the ship is unsinkable. Reply to: {user_input}"
        
        response = model.generate_content(prompt)
        st.write(f"**{p['Name']}:** {response.text}")
    except Exception as e:
        st.error(f"⚠️ {e}")
