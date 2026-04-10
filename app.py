import streamlit as st
from google import genai
import pandas as pd

# --- 1. VINTAGE STYLING ---
st.set_page_config(page_title="Titanic Passenger Log", page_icon="🚢")
st.markdown("""
    <style>
    .stApp { background-color: #f4ecd8; font-family: 'Courier New', Courier, monospace; }
    .stApp p, .stMarkdown, .stChatMessage, span { color: #000000 !important; }
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
    # Convert sheet to a dictionary using 'Name' as the key
    data_dict = df.set_index('Name').to_dict('index')
    return df, data_dict

# Load data and STOP if it fails
try:
    passengers_df, passengers_dict = load_data()
except Exception as e:
    st.error(f"⚠️ Logbook connection failed: {e}")
    st.stop()

# --- 3. IDENTIFY PASSENGER ---
query_params = st.query_params
p_name = query_params.get("p", "Capt. E.J. Smith") 

# This defines 'person' - if they aren't in the list, we default to the Captain
person = passengers_dict.get(p_name, passengers_dict.get("Capt. E.J. Smith"))

if not person:
    st.error("The passenger manifest is empty. Please check your Google Sheet.")
    st.stop()

st.title(f"🚢 {p_name}")

# --- 4. IMAGE EXTRACTOR ---
image_col = [c for c in passengers_df.columns if 'image' in c.lower()]
if image_col:
    raw_url = person.get(image_col[0])
    if isinstance(raw_url, str) and raw_url.strip().startswith("http"):
        clean_url = raw_url.strip()
        if "drive.google.com" in clean_url and "view" in clean_url:
            clean_url = clean_url.replace("/view", "/uc?export=download&id=").split("?")[0]
        st.image(clean_url, width=300)
    else:
        st.info("No portrait found in the archives for this passenger.")

# --- 5. CHAT LOGIC ---
with st.sidebar:
    st.title("⚙️ Engine Room")
    model_choice = st.selectbox("Frequency:", ["gemini-3-flash", "gemini-2.0-flash-lite"])

if "GOOGLE_API_KEY" in st.secrets:
    client = genai.Client(api_key=st.secrets["GOOGLE_API_KEY"])
    if "messages"
