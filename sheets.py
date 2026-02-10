import gspread
import pandas as pd
from oauth2client.service_account import ServiceAccountCredentials

SHEET_NAME = "Skylark_Drones"

scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive"
]

creds = ServiceAccountCredentials.from_json_keyfile_name(
    "credentials.json", scope
)
client = gspread.authorize(creds)

def read_sheet(sheet_name):
    sheet = client.open(SHEET_NAME).worksheet(sheet_name)
    return pd.DataFrame(sheet.get_all_records())

def update_pilot_status(pilot_name, new_status):
    sheet = client.open(SHEET_NAME).worksheet("PilotRoster")
    data = sheet.get_all_values()

    header = data[0]
    status_col = header.index("status") + 1  # dynamically find column

    for i, row in enumerate(data[1:], start=2):
        if row[1] == pilot_name:  # name column
            sheet.update_cell(i, status_col, new_status)
            return True

    return False

