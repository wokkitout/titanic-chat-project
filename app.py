import streamlit as st
import pandas as pd
import urllib.parse

# 1. Get the raw name from the URL
# This handles the Lucille%20Carter -> Lucille Carter conversion automatically
try:
    # Try the newest Streamlit way first
    raw_name = st.query_params.get("passenger", "Edward John Smith")
except:
    # Fallback for older Streamlit versions
    raw_name = st.experimental_get_query_params().get("passenger", ["Edward John Smith"])[0]

# Decode the URL (removes the %20)
passenger_name = urllib.parse.unquote(raw_name)

# --- THE REST OF YOUR APP CONTINUES HERE ---
