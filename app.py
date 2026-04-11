import streamlit as st
import pandas as pd
import urllib.parse
import google.generativeai as genai

# --- 1. AESTHETICS ---
st.set_page_config(page_title="Titanic Manifest", page_icon="🚢")
st.markdown("""
    <style>
    .stApp { background-color: #f5f5dc; }
    html, body, [data-testid="stWidgetLabel"], p, h1, h2, h3, span { color: #000000 !important; font-family: 'Georgia', serif; }
    .main-title { text-align: center; margin-top: 20px; font-weight: bold; }
    .stTextInput input { color: #000000 !important; border: 2px solid #000000 !important; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. THE BRAIN (Using Secure Secrets) ---
try:
    # This pulls the key from the Streamlit Settings so it's not in the code
    API_KEY = st.secrets["GEMINI_KEY"]
    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    st.error("I can't find my brain! Make sure GEMINI_KEY is added to Streamlit Secrets.")

# --- 3. DATA LOADING ---
SHEET_URL = "https://docs.google.com/spreadsheets/d/1ELXfthW0Eni6MGMWDjyGAaSreKuf0lj_7LAundUj1yY/export?format=csv&gid=1264206782"

@st.cache_data(ttl=60)
def load_data():
    return pd.read_csv(SHEET_URL)

df = load_data()

# --- 4. PASSENGER LOOKUP ---
try:
    raw_name = st.query_params.get("passenger", "Edward John Smith")
except:
    raw_name = st.experimental_get_query_params().get("passenger", ["Edward John Smith"])[0]

passenger_name = urllib.parse.unquote(raw_name).strip()
df['Name_Clean'] = df['Name'].astype(str).str.strip()
passenger_data = df[df['Name_Clean'] == passenger_name]
p = passenger_data.iloc[0] if not passenger_data.empty else df.iloc[0]

# --- 5. DISPLAY ---
st.markdown(f"<h1 class='main-title'>🚢 {p['Name']}</h1>", unsafe_allow_html=True)
if 'ImageLink' in p and pd.notna(p['ImageLink']):
    st.image(p['ImageLink'], use_container_width=True)

st.write("---")

# --- 6. THE CHAT (REWRITTEN FOR STABILITY) ---
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

user_input = st.text_input(f"Speak to {p['Name'].split()[0]}:", key="input")

if user_input:
    # Build the prompt
    persona = p.get('Bio & Roleplay (The Narrative)', "A passenger on the Titanic.")
    prompt = f"You are {p['Name']} on the Titanic, April 1912. {persona}. You don't know the ship sinks. Reply to: {user_input}"
    
    try:
        # Get response from Gemini
        response = model.generate_content(prompt)
        answer = response.text
        # Show the answer
        st.markdown(f"**{p['Name']}:** {answer}")
    except Exception as e:
        # THIS WILL TELL US THE EXACT PROBLEM
        st.error(f"Bitch is quiet because: {e}")

# Display chat history so it doesn't disappear
for chat in st.session_state.chat_history:
    st.write(chat)
