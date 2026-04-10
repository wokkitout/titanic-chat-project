import streamlit as st
from google import genai

# --- 1. VINTAGE STYLING ---
st.set_page_config(page_title="Titanic Passenger Log", page_icon="🚢")
st.markdown("""
    <style>
    .stApp { background-color: #f4ecd8; font-family: 'Courier New', Courier, monospace; }
    [data-testid="stSidebar"] { background-color: #3e2723; color: white; }
    h1 { color: #3e2723; text-align: center; border-bottom: 2px solid #3e2723; font-variant: small-caps; }
    .stChatMessage { background-color: #ffffffaa; border-radius: 0px; border-left: 5px solid #3e2723; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. THE PASSENGER MANIFEST ---
passengers = {
    "astor": {"name": "John Jacob Astor IV", "bio": "Wealthy, returning from honeymoon. Protective of wife Madeleine."},
    "molly": {"name": "Margaret 'Molly' Brown", "bio": "Denver socialite. Outspoken, brave, 'new money' heart of gold."},
    "smith": {"name": "Capt. E.J. Smith", "bio": "Captain on retirement voyage. Authoritative, weary, proud."},
}

# --- 3. THE "TELEGRAPH" SIDEBAR (The Fix) ---
with st.sidebar:
    st.title("⚙️ Engine Room")
    # In 2026, one of these THREE will work for your account
    model_choice = st.selectbox(
        "Select Telegraph Frequency:",
        ["gemini-2-flash", "gemini-3-flash-preview", "gemini-2.0-flash-lite"],
        help="If one gives a 404 error, try the next one in the list!"
    )
    st.info("April 10, 1912 - Position: 41.73 N, 49.95 W")

query_params = st.query_params
p_id = query_params.get("p", "smith") 
person = passengers.get(p_id, passengers["smith"])

st.title(f"🚢 {person['name']}")

# --- 4. API SETUP ---
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

        system_prompt = f"You are {person['name']}. {person['bio']} It is April 1912. Stay in character."
        
        try:
            # We use the model you picked in the sidebar
            response = client.models.generate_content(
                model=model_choice,
                config={'system_instruction': system_prompt},
                contents=prompt
            )
            
            with st.chat_message("assistant"):
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error(f"Telegraph Frequency {model_choice} is jammed!")
            st.warning(f"Technical Reason: {e}")
            st.info("Try selecting a different frequency in the sidebar.")
else:
    st.error("Missing API Key in Secrets!")
