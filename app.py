import streamlit as st
from google import genai
import pandas as pd

# --- 1. CONNECT TO YOUR GOOGLE SHEET ---
# Replace this with your Google Sheet URL
# The 'gid' tells the app exactly which tab to read
SHEET_URL = "https://docs.google.com/spreadsheets/d/1ELXfthW0Eni6MGMWDjyGAaSreKuf0lj_7LAundUj1yY/export?format=csv&gid=1264206782"

@st.cache_data
def load_data():
    df = pd.read_csv(SHEET_URL)
    # Convert the sheet into a dictionary the app can use
    return df.set_index('Name').to_dict('index')

passengers_data = load_data()

# --- 2. IDENTIFY PASSENGER FROM URL ---
query_params = st.query_params
# Use the passenger name from the URL or default to Captain Smith
p_name = query_params.get("p", "Capt. E.J. Smith") 
person = passengers_data.get(p_name, passengers_data["Capt. E.J. Smith"])

st.title(f"🚢 {p_name}")

# --- 3. EXTRACT AND DISPLAY IMAGE (The "No More Errors" Version) ---
# This looks for the column name even if there are weird spaces or characters
image_col = [c for c in passengers_df.columns if 'image' in c.lower()]

if image_col:
    raw_url = person.get(image_col[0])
    
    # 1. Clean up the link (removes accidental spaces from the spreadsheet)
    if isinstance(raw_url, str):
        clean_url = raw_url.strip()
        
        # 2. Check if it's a valid link
        if clean_url.startswith("http"):
            # 3. Handle Google Drive "Share" links (they usually don't work in st.image directly)
            if "drive.google.com" in clean_url and "view" in clean_url:
                # This converts a 'view' link into a 'direct' link
                clean_url = clean_url.replace("/view", "/uc?export=download&id=").split("?")[0]
            
            st.image(clean_url, width=300)
        else:
            st.info("The link in the spreadsheet doesn't look like a standard web address (http).")
    else:
        st.info("No portrait link found in the archives for this passenger.")
