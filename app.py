import streamlit as st
import google.generativeai as genai
import pandas as pd

# --- 1. VINTAGE STYLING ---
st.set_page_config(page_title="Titanic Passenger Log", page_icon="🚢")
st.markdown("""
    <style>
    .stApp { background-color: #f4ecd8; font-family: 'Courier New', Courier, monospace; }
    .stApp p, .stMarkdown, .stChatMessage, span, div, label { color: #000000 !important; }
    h1, h2, h3 { color: #3e2723 !important; text-align: center; border-bottom: 2px solid #3e2723; font-variant: small-caps; }
    [data-testid="stSidebar"] { background-color: #3e2723; }
    [data-testid="stSidebar"] * { color: #ffffff !important; }
    .stChatMessage { background-color: #ffffffcc !important; border-radius: 0px; border-left: 5px solid #3e2723; margin-bottom: 10px; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. DATA LOADING ---
SHEET_URL = "https://docs.google.com/spreadsheets/d/1ELXfthW0Eni6MGMWDjyGAaSreKuf0lj_7LAundUj1yY/export?format=csv&gid=1264206782"

@st.cache_data
def load_data():
    df = pd.read_csv(SHEET_URL)
    df['Name_Lower'] = df['Name'].str.lower().str.strip()
    return df.set_index('Name_Lower').to_dict('index')

try:
    passengers_dict = load_data()
except Exception as e:
    st.error(f"⚠️ Logbook connection failed: {e}")
    st.stop()

# --- 3. IDENTIFY PASSENGER ---
query_params = st.query_params
p_query = query_params.get("p", "Capt. E.J. Smith").lower().strip()
person = passengers_dict.get(p_query, passengers_dict.get("capt. e.j. smith"))

if not person:
    st.error("Passenger not found.")
    st.stop()

st.markdown(f"## 🚢 {person['Name']}")

# --- 4. IMAGE DISPLAY ---
image_url = person.get("ImageLink")
if isinstance(image_url, str) and image_url.strip().startswith("http"):
    clean_url = image_url.strip()
    if "drive.google.com" in clean_url and "view" in clean_url:
        clean_url = clean_url.replace("/view", "/uc?export=download&id=").split("?")[0]
    st.image(clean_url, width=300)

# --- 5. CHAT LOGIC WITH AUTO-TUNING ---
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Speak to the passenger..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    if "GOOGLE_API_KEY" not in st.secrets:
        st.error("Missing GOOGLE_API_KEY in Secrets!")
    else:
        try:
            # Configure the API right away
            genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
            
            # Auto-fetch available models for your specific API key
            available_models = []
            for m in genai.list_models():
                if 'generateContent' in m.supported_generation_methods:
                    # Remove the 'models/' prefix so it looks clean
                    available_models.append(m.name.replace('models/', ''))
            
            if not available_models:
                st.error("Your API key is valid, but it has no AI models enabled on it!")
                st.stop()

            # Automatically pick the best available model from your personal list
            # It will prioritize gemini-1.5-flash if it exists, otherwise it grabs the first one
            best_model = next((m for m in available_models if '1.5-flash' in m), available_models[0])

            # Sidebar display (so you can see what it actually found)
            with st.sidebar:
                st.title("⚙️ Engine Room")
                st.success(f"Successfully connected to: {best_model}")
                st.write("Other available frequencies:")
                st.write(available_models)

            # Build instructions and generate response
            bio = person.get("Bio & Roleplay (The Narrative)", "A passenger on the Titanic.")
            instructions = f"You are {person['Name']}. {bio} It is April 1912. Stay in character."
            
            model = genai.GenerativeModel(best_model, system_instruction=instructions)
            response = model.generate_content(prompt)

            if response and response.text:
                with st.chat_message("assistant"):
                    st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
            else:
                st.warning("The passenger is silent. Try again.")
                
        except Exception as e:
            st.error(f"Telegraph error: {e}")
