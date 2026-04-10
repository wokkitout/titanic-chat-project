import streamlit as st
from google import genai
import pandas as pd

# --- 1. VINTAGE STYLING ---
st.set_page_config(page_title="Titanic Passenger Log", page_icon="🚢")
st.markdown("""
    <style>
    .stApp { background-color: #f4ecd8; font-family: 'Courier New', Courier, monospace; }
    .stApp p, .stMarkdown, .stChatMessage, span, div, label { color: #000000 !important; }
    h1 { color: #3e2723 !important; text-align: center; border-bottom: 2px solid #3e2723; font-variant: small-caps; }
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
    data_dict = df.set_index('Name_Lower').to_dict('index')
    return data_dict

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
    st.error("Passenger not found in the manifest.")
    st.stop()

st.title(f"🚢 {person['Name']}")

# --- 4. IMAGE DISPLAY ---
image_url = person.get("ImageLink")
if isinstance(image_url, str) and image_url.strip().startswith("http"):
    clean_url = image_url.strip()
    if "drive.google.com" in clean_url and "view" in clean_url:
        clean_url = clean_url.replace("/view", "/uc?export=download&id=").split("?")[0]
    st.image(clean_url, width=300)
else:
    st.info("No portrait found in the archives for this passenger.")

# --- 5. CHAT LOGIC ---
with st.sidebar:
    st.title("⚙️ Engine Room")
    # Updated to the 2026 Stable Models
    model_choice = st.selectbox("Telegraph Frequency:", ["gemini-3-flash", "gemini-1.5-flash"])

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
            st.markdown
