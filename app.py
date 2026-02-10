import streamlit as st

# ================= IMPORTS =================
from agent import (
    get_all_available_pilots,
    get_all_available_drones,
    urgent_reassignment,
    handle_user_query,
)

from sheets import (
    read_sheet,
    update_pilot_status,
    update_drone_status,
)
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []


# ================= PAGE CONFIG =================
st.set_page_config(
    page_title="Skylark Drone Operations AI Agent",
    layout="wide"
)

# ================= HEADER =================
st.title("🚁 Skylark Drone Operations AI Agent")
st.caption("AI-powered dashboard for pilot and drone coordination")

# ================= SIDEBAR =================
st.sidebar.header("🔧 Filters (Optional)")
city = st.sidebar.selectbox("Select Location", ["Bangalore", "Mumbai"])

# ================= HELPER FUNCTIONS (UI ONLY) =================
def get_available_pilots_by_location(location):
    pilots = read_sheet("PilotRoster")
    pilots["status"] = pilots["status"].astype(str).str.strip().str.lower()

    return pilots[
        (pilots["status"] == "available") &
        (pilots["current_location"] == location)
    ]


def get_available_drones_by_location(location):
    drones = read_sheet("DroneFleet")
    drones["status"] = drones["status"].astype(str).str.strip().str.lower()

    return drones[
        (drones["status"] == "available") &
        (drones["location"] == location)
    ]

# ================= CONVERSATIONAL AGENT =================
# ================= CONVERSATIONAL AGENT =================
st.divider()
st.subheader("💬 Conversational Agent")

with st.form("chat_form", clear_on_submit=True):
    user_query = st.text_input(
        "Ask me anything (e.g. 'I need a pilot in Mumbai', "
        "'find drones in Bangalore', 'urgent mission')"
    )
    submitted = st.form_submit_button("Ask")

if submitted and user_query:
    # 🔄 Reset chat (single-turn conversation)
    st.session_state.chat_history = []

    st.session_state.chat_history.append(("user", user_query))
    action, value = handle_user_query(user_query)

    # ---------- PILOTS ----------
    if action == "SHOW_PILOTS_BY_LOCATION":
        st.markdown(
            f"🤖 **Agent:** Sure 😊 Here are the pilots currently available in **{value}**."
        )
        pilots = get_available_pilots_by_location(value)

        if pilots.empty:
            st.warning("No available pilots found in this location.")
        else:
            st.dataframe(pilots, use_container_width=True)

    # ---------- DRONES ----------
    elif action == "SHOW_DRONES_BY_LOCATION":
        st.markdown(
            f"🤖 **Agent:** 🚁 These drones are available in **{value}**."
        )
        drones = get_available_drones_by_location(value)

        if drones.empty:
            st.warning("No available drones found in this location.")
        else:
            st.dataframe(drones, use_container_width=True)

    # ---------- URGENT ----------
    elif action == "URGENT":
        result = urgent_reassignment()
        st.markdown(f"🤖 **Agent:** {result}")

    # ---------- FALLBACK ----------
    else:
        st.markdown(
            "🤖 **Agent:** Hmm 🤔 I didn’t fully understand that.\n\n"
            "Try:\n"
            "- I need a pilot in Mumbai\n"
            "- Find drones in Bangalore\n"
            "- Urgent mission"
        )


# ================= TABS =================
tab1, tab2, tab3 = st.tabs(
    ["👨‍✈️ Pilot Roster", "🚁 Drone Fleet", "🚨 Urgent Actions"]
)

# ================= PILOT TAB =================
with tab1:
    st.subheader("Available Pilots (All Locations)")
    available_pilots = get_all_available_pilots()

    if available_pilots.empty:
        st.warning("No available pilots found.")
    else:
        st.dataframe(available_pilots, use_container_width=True)

    st.divider()
    st.subheader("All Pilots")
    all_pilots = read_sheet("PilotRoster")
    st.dataframe(all_pilots, use_container_width=True)

    st.divider()
    st.subheader("✅ Mark Pilot as Available")

    pilot_name = st.selectbox(
        "Select pilot",
        all_pilots["name"].tolist()
    )

    if st.button("Mark Pilot Available"):
        update_pilot_status(pilot_name, "Available", "-")
        st.success(f"Pilot {pilot_name} is now Available")
        st.rerun()

# ================= DRONE TAB =================
with tab2:
    st.subheader("Available Drones (All Locations)")
    available_drones = get_all_available_drones()

    if available_drones.empty:
        st.warning("No available drones found.")
    else:
        st.dataframe(available_drones, use_container_width=True)

    st.divider()
    st.subheader("All Drones")
    all_drones = read_sheet("DroneFleet")
    st.dataframe(all_drones, use_container_width=True)

    st.divider()
    st.subheader("🚁 Mark Drone as Available")

    drone_id = st.selectbox(
        "Select drone",
        all_drones["drone_id"].tolist()
    )

    if st.button("Mark Drone Available"):
        update_drone_status(drone_id, "Available", "-")
        st.success(f"Drone {drone_id} is now Available")
        st.rerun()

# ================= URGENT TAB =================
with tab3:
    st.subheader("🚨 Urgent Reassignment")
    st.write(
        "Use this when a high-priority mission requires immediate pilot "
        "and drone reassignment."
    )

    if st.button("⚡ Trigger Urgent Reassignment"):
        result = urgent_reassignment()
        st.success(result)
        st.rerun()
