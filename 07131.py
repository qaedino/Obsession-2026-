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
URL = f"https://api.jsonbin.io/v3/b/{BIN_ID}/latest"
HEADERS = {
    "X-Master-Key": API_KEY,
    "Content-Type": "application/json"
}

# Function to fetch the current live votes
def get_votes():
    req = requests.get(URL, headers=HEADERS)
    return req.json()["record"]

# Function to save new votes to the database
def update_votes(new_data):
    requests.put(URL, json=new_data, headers=HEADERS)

# --- Local Voting State ---
if "voted" not in st.session_state:
    st.session_state.voted = False

vote = st.radio("Choose your side:", ("Bear 🐻", "Nikki 💅"))

if st.button("Submit Vote"):
    st.session_state.voted = True  
    
    # 1. Get the absolute latest votes from the cloud
    current_votes = get_votes()
    
    # 2. Add the user's new vote
    if vote == "Bear 🐻":
        current_votes["Bear 🐻"] += 1
        st.success("You sided with Bear! 🐻")
    elif vote == "Nikki 💅":
        current_votes["Nikki 💅"] += 1
        st.success("You sided with Nikki! 💅")
        
    # 3. Save the new totals permanently back to the cloud
    update_votes(current_votes)

# --- Display Live Results ---
if st.session_state.voted:
    st.write("---")
    st.subheader("Current Live Results:")
    
    # Fetch the numbers again so they see everyone's combined votes
    latest_votes = get_votes()

    col1, col2 = st.columns(2)
    with col1:
        st.metric(label="Votes for Bear", value=latest_votes["Bear 🐻"])
    with col2:
        st.metric(label="Votes for Nikki", value=latest_votes["Nikki 💅"])
else:
    st.write("---")
    st.info("🔒 Results are hidden until you submit your vote!")
