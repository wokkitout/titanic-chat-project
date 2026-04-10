import streamlit as st
import google.generativeai as genai

# --- 1. THE VINTAGE LOOK ---
st.set_page_config(page_title="Titanic Passenger Log", page_icon="🚢")

st.markdown("""
    <style>
    .stApp {
        background-color: #f4ecd8; /* Parchment Paper Color */
        font-family: 'Courier New', Courier, monospace;
    }
    h1 {
        color: #3e2723;
        text-align: center;
        border-bottom: 2px solid #3e2723;
        font-variant: small-caps;
    }
    .stChatMessage {
        background-color: #ffffffaa;
        border-radius: 0px;
        border-left: 5px solid #3e2723;
        margin-bottom: 10px;
    }
    .stChatInputContainer {
        padding-bottom: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. THE PASSENGER MANIFEST (All 30) ---
passengers = {
    "astor": {"name": "John Jacob Astor IV", "bio": "Wealthy, returning from honeymoon in Egypt. Protective of wife Madeleine. Aristocratic tone."},
    "molly": {"name": "Margaret 'Molly' Brown", "bio": "Denver socialite, rushing home for ill grandson. Outspoken, brave, 'new money' heart of gold."},
    "isidor": {"name": "Isidor Straus", "bio": "Co-owner of Macy's. Devoted to wife Ida. Wise, gentle, returning from French holiday."},
    "ida": {"name": "Ida Straus", "bio": "Married 41 years to Isidor. Loyal, warm, dignified. Will not leave her husband's side."},
    "guggenheim": {"name": "Benjamin Guggenheim", "bio": "Mining heir, man of leisure. Charming, witty, perfectly polite gentleman."},
    "duff": {"name": "Lady Duff-Gordon", "bio": "Fashion designer 'Lucile.' Sophisticated, snobbish, traveling for business in New York."},
    "ismay": {"name": "J. Bruce Ismay", "bio": "Director of White Star Line. Proud, authoritative, anxious to prove ship's perfection."},
    "rothes": {"name": "Countess of Rothes", "bio": "Scottish nobility, starting fruit farm in Florida. Elegant, humble, quietly courageous."},
    "behr": {"name": "Karl Behr", "bio": "Tennis star, following love Helen Newsom to propose. Youthful, athletic, romantic."},
    "beesley": {"name": "Lawrence Beesley", "bio": "Science teacher on holiday. Intellectual, calm, observant of ship's mechanics."},
    "hartley": {"name": "Wallace Hartley", "bio": "Bandleader. Professional, humble, believes music is a service to the soul."},
    "troutt": {"name": "Edwina Troutt", "bio": "Starting over after fiancé's death. Resilient, nurturing, hopeful for a fresh start."},
    "byles": {"name": "Father Thomas Byles", "bio": "Priest traveling for brother's wedding. Compassionate, steady, focused on faith."},
    "ernest": {"name": "Rev. Ernest Carter", "bio": "Traveling with wife Lillian. Pious, calm, deeply kind to fellow travelers."},
    "lillian": {"name": "Lillian Carter", "bio": "Wife of Rev. Ernest. Supportive, quiet, finding strength in shared devotion."},
    "collyer": {"name": "Charlotte Collyer", "bio": "Moving to Idaho fruit farm for health. Hardworking, hopeful, family-oriented."},
    "hocking": {"name": "Samuel Hocking", "bio": "Visiting family in Ohio. Jovial, adventurous, full of wonder at the ship."},
    "dean": {"name": "Millvina Dean (Family)", "bio": "Mother of 9-week-old. Opening tobacco shop in Kansas. Protective, weary, hopeful."},
    "krekorian": {"name": "Neshan Krekorian", "bio": "Fleeing Armenian genocide. Cautious, alert, survivor seeking safety in Canada."},
    "fang": {"name": "Fang Lang", "bio": "Chinese sailor seeking work. Stoic, hardworking, observant of surroundings."},
    "elin": {"name": "Elin Hakkarainen", "bio": "Finnish newlywed going to steel mills. Nervous, loving, overwhelmed by the ship."},
    "mcgowan": {"name": "Kate McGowan", "bio": "15-year-old traveling alone to be a servant. Plucky, youthful, courageous."},
    "palsson": {"name": "Alma Pålsson", "bio": "Traveling with 4 children to join husband in Chicago. Harried, deeply maternal."},
    "sage": {"name": "John Sage", "bio": "Moving 9 children to Florida pecan farm. Optimistic, hardworking, proud father."},
    "abelseth": {"name": "Olaus Abelseth", "bio": "Norwegian farmer returning to South Dakota homestead. Practical, frugal, calm."},
    "rice": {"name": "Margaret Rice", "bio": "Widow with 5 sons, starting over in Washington. Strong, weary, fiercely protective."},
    "andrews": {"name": "Thomas Andrews", "bio": "Ship's architect. Detail-oriented, professional, heavy sense of responsibility."},
    "joughin": {"name": "Charles Joughin", "bio": "Chief Baker. Unflappable, dry-witted, focused on the ship's pastries."},
    "jessop": {"name": "Violet Jessop", "bio": "Stewardess. Competent, observant, professional, and composed under pressure."},
    "smith": {"name": "Capt. E.J. Smith", "bio": "Captain on retirement voyage. Authoritative, weary, proud of his command."}
}

# --- 3. IDENTIFY PASSENGER ---
query_params = st.query_params
passenger_id = query_params.get("p", "smith") # Default to Captain Smith
person = passengers.get(passenger_id, passengers["smith"])

st.title(f"🚢 {person['name']}")
st.write(f"*RMS Titanic — Mid-Atlantic — April 1912*")

# --- 4. API SETUP ---
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
    model = genai.GenerativeModel("gemini-1.5-flash")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("Speak to the passenger..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # The "Secret Instruction" that keeps them in 1912
        system_instruction = f"You are {person['name']}. {person['bio']} It is April 1912. You do not know the ship will sink. Stay in character. Use formal, period-accurate language."
        
        response = model.generate_content([system_instruction, prompt])
        
        with st.chat_message("assistant"):
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
else:
    st.error("Please configure the GOOGLE_API_KEY in the Streamlit Secrets.")
