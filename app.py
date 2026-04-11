import streamlit as st
import pandas as pd
import urllib.parse

# --- 1. PAGE CONFIG & VINTAGE AESTHETICS ---
st.set_page_config(page_title="Titanic Manifest", page_icon="🚢")

st.markdown("""
    <style>
    .stApp {
        background-color: #f5f5dc; /* Classic Beige */
    }
    .main-title {
        color: #2c3e50;
        font-family: 'Georgia', serif;
        text-align: center;
        padding-top: 20px;
    }
    .bio-box {
        background-color: #ffffff;
        padding: 20px;
        border-radius: 10px;
        border: 1px solid #d3d3d3;
        color: #000000;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. THE LUCILLE FIX (URL DECODER) ---
try:
    raw_name = st.query_params.get("passenger", "Edward John Smith")
except:
    raw_name = st.experimental_get_query_params().get("passenger", ["Edward John Smith"])[0]

passenger_name = urllib.parse.unquote(raw_name).strip()

# --- 3. DATA LOADING ---
SHEET_URL = "https://docs.google.com/spreadsheets/d/1ELXfthW0Eni6MGMWDjyGAaSreKuf0lj_7LAundUj1yY/export?format=csv&gid=1264206782"

@st.cache_data(ttl=60)
def load_data():
    return pd.read_csv(SHEET_URL)

df = load_data()

# --- 4. PASSENGER LOOKUP ---
passenger_data = df[df['Name'].str.strip() == passenger_name]

if passenger_data.empty:
    p = df[df['Name'].str.strip() == "Edward John Smith"].iloc[0]
else:
    p = passenger_data.iloc[0]

# --- 5. DISPLAY HEADER ---
st.markdown(f"<h1 class='main-title'>🚢 {p['Name']}</h1>", unsafe_allow_html=True)
st.write("---")

# --- 6. IMAGE DISPLAY ---
# Using the Postimg link logic we set up
if 'ImageLink' in p and pd.notna(p['ImageLink']):
    st.image(p['ImageLink'], use_container_width=True)

# --- 7. BIOGRAPHY (The "Find Anything" Fix) ---
st.subheader("Passenger Details")

# This looks for any column that even SLIGHTLY looks like 'Bio' or 'Story'
# It handles lowercase, uppercase, and accidental spaces
bio_col = None
for col in df.columns:
    c_clean = col.strip().lower()
    if c_clean in ['biography', 'bio', 'details', 'story', 'description', 'about']:
        bio_col = col
        break

if bio_col:
    # We found it! Display it in the white box
    st.markdown(f"<div class='bio-box'>{p[bio_col]}</div>", unsafe_allow_html=True)
else:
    # If it still fails, we will print ALL your column names so you can see the right one
    st.error(f"Could not find Bio column. Your columns are: {list(df.columns)}")

# This checks if your column is named 'Biography' or 'Bio' or 'Details'
bio_col = next((c for c in ['Biography', 'Bio', 'Details', 'Story'] if c in p), None)

if bio_col:
    st.markdown(f"<div class='bio-box'>{p[bio_col]}</div>", unsafe_allow_html=True)
else:
    st.error("Could not find the Biography column in your sheet. Please check the column header name!")

# --- 8. RESTORED CHAT BOX ---
st.write("---")
st.subheader(f"Speak with {p['Name'].split()[0]}")
user_input = st.text_input("Ask about my life or the ship:", placeholder="What class are you traveling in?")

if user_input:
    st.info(f"*{p['Name']} is considering your question...*")
    # Your Gemini API code goes right here!
