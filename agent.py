import pandas as pd
from sheets import (
    read_sheet,
    update_pilot_status,
    update_drone_status
)

# ---------------- BASIC QUERY FUNCTIONS ----------------

def get_all_available_pilots():
    pilots = read_sheet("PilotRoster")
    pilots["status"] = pilots["status"].astype(str).str.strip().str.lower()
    return pilots[pilots["status"] == "available"]


def get_all_available_drones():
    drones = read_sheet("DroneFleet")
    drones["status"] = drones["status"].astype(str).str.strip().str.lower()
    return drones[drones["status"] == "available"]


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


# ---------------- URGENT REASSIGNMENT ----------------

def urgent_reassignment():
    pilots = read_sheet("PilotRoster")
    drones = read_sheet("DroneFleet")

    pilots["status"] = pilots["status"].str.lower().str.strip()
    drones["status"] = drones["status"].str.lower().str.strip()

    # 1️⃣ Find available pilot
    available_pilots = pilots[pilots["status"] == "available"]
    if available_pilots.empty:
        return "❌ No available pilots for urgent reassignment."

    pilot = available_pilots.iloc[0]

    # 2️⃣ Find available drone in SAME LOCATION
    available_drones = drones[
        (drones["status"] == "available") &
        (drones["location"] == pilot["current_location"])
    ]

    if available_drones.empty:
        return f"❌ No available drones in {pilot['current_location']}."

    drone = available_drones.iloc[0]

    mission_id = "Urgent-Mission"

    # 3️⃣ ASSIGN BOTH
    update_pilot_status(
        pilot_name=pilot["name"],
        new_status="Assigned",
        assignment=mission_id
    )

    update_drone_status(
        drone_id=drone["drone_id"],
        new_status="Assigned",
        assignment=mission_id
    )

    return (
        f"🚨 Urgent reassignment completed:\n\n"
        f"👨‍✈️ Pilot: {pilot['name']} ({pilot['current_location']})\n"
        f"🚁 Drone: {drone['drone_id']} ({drone['model']})"
    )



# ---------------- CONVERSATIONAL AGENT ----------------

def handle_user_query(query):
    q = query.lower()

    # -------- detect location --------
    location = None
    if "mumbai" in q:
        location = "Mumbai"
    elif "bangalore" in q:
        location = "Bangalore"

    # -------- pilot intents --------
    if (
        "pilot" in q or
        "pilots" in q
    ):
        if location:
            return ("SHOW_PILOTS_BY_LOCATION", location)
        return ("SHOW_ALL_PILOTS", None)

    # -------- drone intents --------
    if (
        "drone" in q or
        "drones" in q
    ):
        if location:
            return ("SHOW_DRONES_BY_LOCATION", location)
        return ("SHOW_ALL_DRONES", None)

    # -------- urgent intents --------
    if (
        "urgent" in q or
        "emergency" in q or
        "immediate" in q
    ):
        return ("URGENT", None)

    return ("UNKNOWN", None)

