import streamlit as st
from google import genai

# --- 1. VINTAGE STYLING (The Black Ink Fix) ---
st.set_page_config(page_title="Titanic Passenger Log", page_icon="🚢")

st.markdown("""
    <style>
    /* Global Background and Text */
    .stApp { 
        background-color: #f4ecd8; 
        font-family: 'Courier New', Courier, monospace;
    }
    
    /* Force all chat and paragraph text to be DEEP BLACK */
    .stApp p, .stMarkdown, .stChatMessage, span {
        color: #000000 !important;
    }

    /* Header styling */
    h1 { 
        color: #3e2723 !important; 
        text-align: center; 
        border-bottom: 2px solid #3e2723; 
        font-variant: small-caps; 
    }

    /* Sidebar Styling */
    [data-testid="stSidebar"] { 
        background-color: #3e2723; 
    }
    [data-testid="stSidebar"] * {
        color: #ffffff !important;
    }

    /* Message Bubble Styling */
    .stChatMessage { 
        background-color: #ffffffcc !important; 
        border-radius: 0px; 
        border-left: 5px solid #3e2723; 
        margin-bottom: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. THE PASSENGER MANIFEST ---
passengers = {
    "astor": {"name": "John Jacob Astor IV", "bio": "Wealthy, returning from honeymoon. Protective of wife Madeleine."},
    "molly": {"name": "Margaret 'Molly' Brown", "bio": "Denver socialite. Outspoken, brave, 'new money' heart of gold."},
    "smith": {"name": "Capt. E.J. Smith", "bio": "Captain on retirement voyage. Authoritative, weary, proud."},
}

# --- 3. SIDEBAR CONTROLS ---
with st.sidebar:
    st.title("⚙️ Engine Room")
    model_choice = st.selectbox(
        "Select Telegraph Frequency:",
        ["gemini-3-flash-preview", "gemini-2-flash", "gemini-2.0-flash-lite"],
        help="Try a different one if you get a 404 error!"
    )
    st.info("April 10, 1912 - Mid-Atlantic")

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
            response = client.models.generate_content(
                model=model_choice,
                config={'system_instruction': system_prompt},
                contents=prompt
            )
            
            with st.chat_message("assistant"):
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error(f"Telegraph error: {e}")
else:
    st.error("Missing API Key in Secrets!")
