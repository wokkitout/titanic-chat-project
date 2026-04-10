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
    [data-testid="stSidebar"] { background-color: #3e2723; color: white; }
    [data-testid="stSidebar"] * { color: white !important; }
    .stChatMessage { background-color: #ffffffcc !important; border-radius: 0px; border-left: 5px solid #3e2723; margin-bottom: 10px; }
   #MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# --- 2. DATA LOADING ---
SHEET_URL = "https://docs.google.com/spreadsheets/d/1ELXfthW0Eni6MGMWDjyGAaSreKuf0lj_7LAundUj1yY/export?format=csv"

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

# --- 4. IMAGE DISPLAY (DEBUG VERSION) ---
image_url = person.get("ImageLink")

# Print the actual link to the screen so we can see if it's empty/wrong

if isinstance(image_url, str) and len(image_url.strip()) > 10:
    url = image_url.strip()
    
    # Simple logic: If it's Drive, convert it. If not, use as-is.
    if "drive.google.com" in url:
        import re
        id_match = re.search(r'[-\w]{25,}', url)
        clean_url = f"https://drive.google.com/thumbnail?id={id_match.group()}&sz=w1000" if id_match else url
    else:
        clean_url = url
        
    st.image(clean_url, width=300)
else:
    st.warning("No valid image link found for this passenger in the Google Sheet.")
# --- 5. SECRETS & ENGINE ROOM (FIXED MODEL LOGIC) ---
if "GOOGLE_API_KEY" not in st.secrets:
    st.error("Missing GOOGLE_API_KEY!")
    st.stop()

genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

try:
    available_models = [m.name.replace('models/', '') for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
    
    # Updated Priority to avoid the 404 error
    # We look for 1.5-flash first as it is fast and currently available
    best_model = next((m for m in available_models if '1.5-flash' in m), 
                 next((m for m in available_models if '1.5-pro' in m), available_models[0]))
    
    with st.sidebar:
        st.title("⚙️ ENGINE ROOM")
        st.success(f"Connected to: {best_model}")
        st.info("Available Frequencies:")
        st.write(available_models)
except Exception as e:
    best_model = "gemini-1.5-flash"

# --- 6. CHAT LOGIC ---
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Speak to the passenger..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    try:
        bio = person.get("Bio & Roleplay (The Narrative)", "A passenger on the Titanic.")
        instructions = f"You are {person['Name']}. {bio} It is April 1912. Stay in character. Keep responses brief."
        
        model = genai.GenerativeModel(best_model, system_instruction=instructions)
        
        response = model.generate_content(
            prompt, 
            stream=True,
            generation_config=genai.types.GenerationConfig(
                max_output_tokens=300,
                temperature=0.7
            )
        )

        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = ""
            for chunk in response:
                if chunk.text: 
                    full_response += chunk.text
                    message_placeholder.markdown(full_response + "▌")
            
            message_placeholder.markdown(full_response)
            
        st.session_state.messages.append({"role": "assistant", "content": full_response})
            
    except Exception as e:
        st.error(f"Telegraph error: {e}")
