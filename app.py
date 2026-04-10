# --- 4. IMAGE & QR DISPLAY ---
import urllib.parse
import qrcode

# Put your actual Streamlit URL right here:
BASE_URL = "https://your-repo-name.streamlit.app/"

col1, col2 = st.columns([2, 1]) # Splits the screen to look like a ticket

with col1:
    image_url = person.get("ImageLink")
    if isinstance(image_url, str) and image_url.strip().startswith("http"):
        clean_url = image_url.strip().replace("/view", "/uc?export=download&id=").split("?")[0] if "drive.google.com" in image_url else image_url.strip()
        st.image(clean_url, width=300)

with col2:
    # Build the safe URL for this specific passenger
    safe_name = urllib.parse.quote(person['Name'])
    passenger_url = f"{BASE_URL}?p={safe_name}"
    
    # Generate the QR Code ink
    qr = qrcode.make(passenger_url)
    st.image(qr.get_image(), width=150, caption="Scan to open Telegraph")
