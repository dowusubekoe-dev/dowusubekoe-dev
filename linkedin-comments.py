import pandas as pd
import gspread
from google.oauth2.service_account import Credentials

# Load Excel sheet
excel_path = "LinkedIn_Comment_Tracker_Custom.xlsx"
sheet_name = "Comment Tracker"  # Adjust this if needed
df = pd.read_excel(excel_path, sheet_name=sheet_name)

# Authenticate with Google Sheets API
scopes = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]
credentials = Credentials.from_service_account_file(
    "credentials.json", scopes=scopes
)
gc = gspread.authorize(credentials)

# Create a new Google Sheet
spreadsheet = gc.create("LinkedIn Comment Tracker (Synced)")
spreadsheet.share('dowusubekoe@gmail.com', perm_type='user', role='writer')  # Optional: Share with your Gmail

# Select the first worksheet and update it with Excel content
worksheet = spreadsheet.sheet1
worksheet.update([df.columns.values.tolist()] + df.values.tolist())

print("✅ Google Sheet created and synced successfully.")
print(f"🔗 Sheet URL: https://docs.google.com/spreadsheets/d/{spreadsheet.id}")
