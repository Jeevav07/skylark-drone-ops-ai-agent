import os
import streamlit as st
import gspread
import pandas as pd
from google.oauth2.service_account import Credentials

# ================= CONFIG =================
SHEET_NAME = "Skylark_Drones"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CREDS_PATH = os.path.join(BASE_DIR, "credentials.json")

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

# ================= AUTH =================
def get_gspread_client():
    if not os.path.exists(CREDS_PATH):
        raise FileNotFoundError("credentials.json not found")

    creds = Credentials.from_service_account_file(
        CREDS_PATH,
        scopes=SCOPES
    )
    return gspread.authorize(creds)

# ================= READ (CACHED) =================
@st.cache_data(ttl=60)
def read_sheet(sheet_name: str) -> pd.DataFrame:
    """
    Reads a worksheet from Google Sheets and caches the result.
    Cache is cleared explicitly after any write operation.
    """
    client = get_gspread_client()
    sheet = client.open(SHEET_NAME).worksheet(sheet_name)
    return pd.DataFrame(sheet.get_all_records())

# ================= UPDATE PILOT =================
def update_pilot_status(pilot_name: str, new_status: str, assignment: str = "-") -> bool:
    client = get_gspread_client()
    sheet = client.open(SHEET_NAME).worksheet("PilotRoster")
    data = sheet.get_all_values()

    header = data[0]
    name_col = header.index("name") + 1
    status_col = header.index("status") + 1
    assignment_col = header.index("current_assignment") + 1

    for i, row in enumerate(data[1:], start=2):
        if row[name_col - 1] == pilot_name:
            sheet.update_cell(i, status_col, new_status)
            sheet.update_cell(i, assignment_col, assignment)
            read_sheet.clear()  # 🔥 force fresh read
            return True

    return False

# ================= UPDATE DRONE =================
def update_drone_status(drone_id: str, new_status: str, assignment: str = "-") -> bool:
    client = get_gspread_client()
    sheet = client.open(SHEET_NAME).worksheet("DroneFleet")
    data = sheet.get_all_values()

    header = data[0]
    id_col = header.index("drone_id") + 1
    status_col = header.index("status") + 1
    assignment_col = header.index("current_assignment") + 1

    for i, row in enumerate(data[1:], start=2):
        if row[id_col - 1] == drone_id:
            sheet.update_cell(i, status_col, new_status)
            sheet.update_cell(i, assignment_col, assignment)
            read_sheet.clear()  # 🔥 force fresh read
            return True

    return False
