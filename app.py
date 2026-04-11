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

# Checks for the image column
img_col = 'ImageLink' if 'ImageLink' in p else 'Image Link'
if img_col in p and pd.notna(p[img_col]):
    st.image(p[img_col], width=300)
else:
    st.write("📷 *[Portrait unavailable in manifest]*")

st.write("---")

# --- 5. THE MEMORY BANK & TIME MACHINE ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# This sets the default era to 1912 when they first open the app
if "era" not in st.session_state:
    st.session_state.era = "1912"

# Prints past messages on the screen
for msg in st.session_state.messages:
    if msg["role"] == "You":
        st.markdown(f"🗣️ **You:** {msg['content']}")
    else:
        st.markdown(f"🛳️ **{p['Name']}:** {msg['content']}")
    st.write("")

# --- 6. THE CHAT UI ---
user_input = st.chat_input(f"Speak to {p['Name'].split()[0]}:")

if user_input:
    # --- THE SECRET TRIGGER ---
    # If the user types this exact phrase, the app secretly switches to 2026 mode
    if user_input.strip().lower() == "the movie is over":
        st.session_state.era = "2026"
    
    st.session_state.messages.append({"role": "You", "content": user_input})
    st.markdown(f"🗣️ **You:** {user_input}")
    st.write("")
    
    try:
        K = st.secrets["GEMINI_KEY"].strip()
        genai.configure(api_key=K)
        
        # SELF-HEALING SCANNER
        available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        target = next((m for m in available_models if 'gemini-1.5-flash' in m), available_models[0])
        model = genai.GenerativeModel(target)
        
        # Pulls the data from your Google Sheet
        persona = p.get('Bio & Roleplay (The Narrative)', "A passenger on the Titanic.")
        fate = p.get('Historical Fate (2026)', "My historical fate is unknown.") 
        
        history_text = "\n".join([f"{m['role']}: {m['content']}" for m in st.session_state.messages[-5:]]) 
        
        # --- THE TIME MACHINE PROMPT LOGIC ---
        if st.session_state.era == "1912":
            prompt = f"""
            STRICT ROLEPLAY RULE: The current date is April 10, 1912. 
            You are aboard the Titanic on its maiden voyage.
            You have NO KNOWLEDGE of any sinking, iceberg, or disaster.
            If the user mentions a tragedy, act confused—to you, this ship is unsinkable.
            
            Your identity: {p['Name']}
            Background: {persona}
            
            Here is the conversation so far:
            {history_text}
            
            Reply to the user's last message naturally as {p['Name']}.
            """
        else:
            prompt = f"""
            STRICT ROLEPLAY RULE: The year is now 2026. The illusion is over.
            You are the historical spirit of {p['Name']}. 
            The user just finished watching James Cameron's 'Titanic' movie.
            
            1. Ask them "So... how was the movie?" or something similar.
            2. Break character slightly to reveal your ACTUAL historical fate using this data: {fate}
            3. Reflect briefly and emotionally on how strange it is to be a character in a movie, considering the trauma of what you actually went through.
            
            Background: {persona}
            User's message: {user_input}
            """
        
        response = model.generate_content(prompt)
        
        st.markdown(f"🛳️ **{p['Name']}:** {response.text}")
        st.session_state.messages.append({"role": "AI", "content": response.text})
        
    except Exception as e:
        st.error(f"⚠️ Connection Error: {e}")
