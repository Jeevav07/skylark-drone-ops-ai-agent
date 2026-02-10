import streamlit as st
import gspread
import pandas as pd
from google.oauth2.service_account import Credentials

# ---------------- CONFIG ----------------
SHEET_NAME = "Skylark_Drones"

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
]

# ---------------- AUTH CLIENT ----------------
def get_gspread_client():
    if "gcp_service_account" not in st.secrets:
        raise RuntimeError("Google service account not found in Streamlit secrets")

    creds = Credentials.from_service_account_info(
        st.secrets["gcp_service_account"],
        scopes=SCOPES
    )
    return gspread.authorize(creds)

# ---------------- READ (CACHED) ----------------
@st.cache_data(ttl=60)
def read_sheet(sheet_name):
    client = get_gspread_client()
    sheet = client.open(SHEET_NAME).worksheet(sheet_name)
    return pd.DataFrame(sheet.get_all_records())

# ---------------- UPDATE PILOT ----------------
def update_pilot_status(pilot_name, new_status, assignment="-"):
    client = get_gspread_client()
    sheet = client.open(SHEET_NAME).worksheet("PilotRoster")
    data = sheet.get_all_values()

    header = data[0]
    name_col = header.index("name")
    status_col = header.index("status")
    assignment_col = header.index("current_assignment")

    for i, row in enumerate(data[1:], start=2):
        if row[name_col] == pilot_name:
            sheet.update_cell(i, status_col + 1, new_status)
            sheet.update_cell(i, assignment_col + 1, assignment)
            read_sheet.clear()
            return True

    return False

# ---------------- UPDATE DRONE ----------------
def update_drone_status(drone_id, new_status, assignment="-"):
    client = get_gspread_client()
    sheet = client.open(SHEET_NAME).worksheet("DroneFleet")
    data = sheet.get_all_values()

    header = data[0]
    id_col = header.index("drone_id")
    status_col = header.index("status")
    assignment_col = header.index("current_assignment")

    for i, row in enumerate(data[1:], start=2):
        if row[id_col] == drone_id:
            sheet.update_cell(i, status_col + 1, new_status)
            sheet.update_cell(i, assignment_col + 1, assignment)
            read_sheet.clear()
            return True

    return False
