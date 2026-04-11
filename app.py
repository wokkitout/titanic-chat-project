# --- 5. THE BRAIN (THE NO-FAIL VERSION) ---
if user_input:
    try:
        api_key = st.secrets["GEMINI_KEY"].strip()
        genai.configure(api_key=api_key)
        
        # We try 3 different names for the same brain. One WILL work.
        model_names = ['gemini-1.5-flash', 'models/gemini-1.5-flash', 'gemini-pro']
        
        success = False
        for name in model_names:
            try:
                model = genai.GenerativeModel(name)
                response = model.generate_content(f"You are {p['Name']} in 1912. Reply: {user_input}")
                st.write(f"**{p['Name']}:** {response.text}")
                success = True
                break # Stop if one works!
            except:
                continue # Try the next name if it fails
        
        if not success:
            st.error("Google doesn't recognize any model names. Let's check requirements.txt.")

    except Exception as e:
        st.error(f"⚠️ {e}")
