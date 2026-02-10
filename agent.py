from sheets import read_sheet, update_pilot_status

def get_available_pilots(skill, location):
    pilots = read_sheet("PilotRoster")
    return pilots[
        (pilots["status"] == "Available") &
        (pilots["skills"].str.contains(skill, case=False)) &
        (pilots["current_location"] == location)
    ]

def get_available_drones(capability, location):
    drones = read_sheet("DroneFleet")
    return drones[
        (drones["status"] == "Available") &
        (drones["capabilities"].str.contains(capability, case=False)) &
        (drones["location"] == location)
    ]

def urgent_reassignment():
    pilots = read_sheet("PilotRoster")
    available = pilots[pilots["status"] == "Available"]

    if available.empty:
        return "❌ No pilots available for urgent reassignment"

    chosen = available.iloc[0]
    update_pilot_status(chosen["name"], "Assigned")
    return f"🚨 Urgently reassigned pilot: {chosen['name']}"
