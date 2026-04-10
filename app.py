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
    "astor": {"name": "John Jacob Astor IV", "bio": "Wealthy, returning from honeymoon in Egypt. Protective of wife Madeleine. Aristocratic tone."},
    "molly": {"name": "Margaret 'Molly' Brown", "bio": "Denver socialite, rushing home for ill grandson. Outspoken, brave, 'new money' heart of gold."},
    "smith": {"name": "Capt. E.J. Smith", "bio": "Captain on retirement voyage. Authoritative, weary, proud of his command."},
}

# --- 3. IDENTIFY PASSENGER ---
query_params = st.query_params
p_id = query_params.get("p", "smith") 
person = passengers.get(p_id, passengers["smith"])

st.title(f"🚢 {person['name']}")
st.write(f"*RMS Titanic — Mid-Atlantic — April 10, 1912*")

# --- 4. API SETUP (2026 STABLE VERSION) ---
if "GOOGLE_API_KEY" in st.secrets:
    client = genai.Client(api_key=st.secrets["GOOGLE_API_KEY"])

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("Speak to the passenger..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        system_prompt = f"You are {person['name']}. {person['bio']} It is April 1912. You do not know the ship will sink. Stay in character."
        
        try:
            # We are switching to gemini-2.5-flash (STABLE)
            # Or use "gemini-3-flash-preview" for the absolute newest.
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                config={'system_instruction': system_prompt},
                contents=prompt
            )
            
            with st.chat_message("assistant"):
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            # If 2.5 fails, it will show the reason here
            st.error(f"The telegraph is sputtering! {e}")
else:
    st.error("Missing API Key in Streamlit Secrets!")
