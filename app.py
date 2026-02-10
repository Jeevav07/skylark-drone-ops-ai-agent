import streamlit as st
from agent import get_available_pilots, get_available_drones, urgent_reassignment

st.set_page_config(page_title="Skylark Drone Ops AI", layout="wide")
st.title("🚁 Skylark Drone Operations AI Agent")

query = st.text_input(
    "Ask me (examples: available pilots, available drones, urgent reassignment)"
)

if st.button("Submit"):
    q = query.lower()

    if "available pilots" in q:
        pilots = get_available_pilots("mapping", "Bangalore")
        st.subheader("Available Pilots")
        st.dataframe(pilots)

    elif "available drones" in q:
        drones = get_available_drones("camera", "Bangalore")
        st.subheader("Available Drones")
        st.dataframe(drones)

    elif "urgent reassignment" in q:
        result = urgent_reassignment()
        st.warning(result)

    else:
        st.info("Try: available pilots | available drones | urgent reassignment")
