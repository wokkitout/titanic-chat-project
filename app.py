import streamlit as st
from google import genai

# --- 1. VINTAGE STYLING ---
st.set_page_config(page_title="Titanic Passenger Log", page_icon="🚢")
st.markdown("""
    <style>
    .stApp { background-color: #f4ecd8; font-family: 'Courier New', Courier, monospace; }
    h1 { color: #3e2723; text-align: center; border-bottom: 2px solid #3e2723; font-variant: small-caps; }
    .stChatMessage { background-color: #ffffffaa; border-radius: 0px; border-left: 5px solid #3e2723; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. THE PASSENGER MANIFEST ---
passengers = {
    "astor": {"name": "John Jacob Astor IV", "bio": "Wealthy, returning from honeymoon. Protective of wife Madeleine. Aristocratic tone."},
    "molly": {"name": "Margaret 'Molly' Brown", "bio": "Denver socialite. Outspoken, brave, 'new money' heart of gold."},
    "smith": {"name": "Capt. E.J. Smith", "bio": "Captain on retirement voyage. Authoritative, weary, proud of his command."},
}

# --- 3. IDENTIFY PASSENGER ---
query_params = st.query_params
p_id = query_params.get("p", "smith") 
person = passengers.get(p_id, passengers["smith"])

st.title(f"🚢 {person['name']}")
st.write(f"*RMS Titanic — April 1912*")

# --- 4. THE SMART API SETUP ---
if "GOOGLE_API_KEY" in st.secrets:
    client = genai.Client(api_key=st.secrets["GOOGLE_API_KEY"])

    # --- AUTO-DETECT THE BEST MODEL ---
    if "active_model" not in st.session_state:
        try:
            # Look at what your key is actually allowed to use
            available_models = [m.name for m in client.models.list() if 'generateContent' in m.supported_variants]
            # Priority list for 2026
            priority = ["gemini-3-flash", "gemini-2.5-flash", "gemini-1.5-flash", "gemini-1.5-pro"]
            
            # Pick the first one that matches your account
            st.session_state.active_model = next((m for m in priority if any(m in avail for avail in available_models)), "gemini-1.5-flash")
        except:
            st.session_state.active_model = "gemini-1.5-flash" # Fallback

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("Speak to the passenger..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        system_prompt = f"You are {person['name']}. {person['bio']} It is April 1912. Do not know the ship will sink. Stay in character."
        
        try:
            # Use the model we auto-detected
            response = client.models.generate_content(
                model=st.session_state.active_model,
                config={'system_instruction': system_prompt},
                contents=prompt
            )
            
            with st.chat_message("assistant"):
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error(f"The telegraph line is cut! Error: {e}")
            st.info(f"Tried using model: {st.session_state.active_model}")
else:
    st.error("Missing API Key in Secrets!")
