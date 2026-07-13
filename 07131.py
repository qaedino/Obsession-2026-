import streamlit as st
import requests

st.set_page_config(page_title="Obsession 2026 Vote", page_icon="🎬", layout="centered")

st.image(
    "https://i.pinimg.com/736x/52/0d/dc/520ddc5586cba7aa06f929c6ca871cc3.jpg", 
    use_container_width=True
)

st.title(":red[Obsession, 2026]")
st.header("Who's the Ultimate Villain? 😈")       
st.write("Cast your vote below to reveal where the group stands!")

# --- Connect to JSONBin Database ---
BIN_ID = st.secrets["BIN_ID"]
API_KEY = st.secrets["API_KEY"]

# FIXED: Added /id/ to target the raw record directly
URL = f"https://api.jsonbin.io/v3/b/{BIN_ID}"
HEADERS = {
    "X-Master-Key": API_KEY,
    "Content-Type": "application/json",
    "X-Bin-Meta": "false"  # Forces JSONBin to return just our data, no extra junk
}

# Function to fetch the current live votes safely
def get_votes():
    try:
        req = requests.get(URL, headers=HEADERS)
        if req.status_code == 200:
            return req.json()
    except Exception:
        pass
    return {"bear": 0, "nikki": 0}  # Emergency fallback digits

# Function to save new votes to the database
def update_votes(new_data):
    try:
        requests.put(URL, json=new_data, headers=HEADERS)
    except Exception:
        pass

# --- Local Session Syncing ---
if "voted" not in st.session_state:
    st.session_state.voted = False

vote = st.radio("Choose your side:", ("Bear 🐻", "Nikki 💅"))

if st.button("Submit Vote"):
    st.session_state.voted = True  
    
    # 1. Pull current global numbers
    current_votes = get_votes()
    
    # 2. Increment the selected variable
    if vote == "Bear 🐻":
        current_votes["bear"] = current_votes.get("bear", 0) + 1
        st.success("You sided with Bear! 🐻")
    elif vote == "Nikki 💅":
        current_votes["nikki"] = current_votes.get("nikki", 0) + 1
        st.success("You sided with Nikki! 💅")
        
    # 3. Push back to the cloud
    update_votes(current_votes)
    
    # 4. Save locally so it renders immediately
    st.session_state["latest_bear"] = current_votes["bear"]
    st.session_state["latest_nikki"] = current_votes["nikki"]

# --- Display Live Results ---
if st.session_state.voted:
    st.write("---")
    st.subheader("Current Live Results:")
    
    # Grab the numbers we just saved during submission
    bear_total = st.session_state.get("latest_bear", 0)
    nikki_total = st.session_state.get("latest_nikki", 0)

    col1, col2 = st.columns(2)
    with col1:
        st.metric(label="Votes for Bear", value=bear_total)
    with col2:
        st.metric(label="Votes for Nikki", value=nikki_total)
else:
    st.write("---")
    st.info("🔒 Results are hidden until you submit your vote!")
