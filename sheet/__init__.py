# import gspread
# import os
# from google.oauth2.service_account import Credentials
# from dotenv import load_dotenv

# load_dotenv(dotenv_path=".env")

# class Sheet:
#     def __init__(self):
#         self.sheet_id = os.getenv("SHEET_ID")

#     def write_to_google_sheet(self, data):
#         # Set up the credentials using google-auth
#         creds = Credentials.from_service_account_file(
#             'gs-keys.json',
#             scopes=["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
#         )

#         # Authorize the client
#         client = gspread.authorize(creds)

#         # Open the Google Sheet by its ID
#         sheet = client.open_by_key(self.sheet_id).sheet1

#         # Prepare the row to insert based on the column structure
#         row = [
#             data.get("first_name", ""),           # Ismi
#             data.get("last_name", ""),            # Familiyasi
#             data.get("middle_name", ""),          # Sharifi
#             data.get("contract_number", ""),      # Shartnoma raqami
#             data.get("pnfl", ""),                 # PINFL
#             data.get("payment", ""),              # To'lov summasi
#             data.get("payment_app", ""),            # To'lov ilovasi
#             data.get("Дата", ""),                 # Sanasi
#         ]

#         # Append the row to the sheet
#         sheet.append_row(row)
#         print("Data written successfully!")


import gspread
import os
import json
from google.oauth2.service_account import Credentials
from dotenv import load_dotenv

load_dotenv(dotenv_path=".env")

class Sheet:
    def __init__(self):
        self.sheet_id = os.getenv("SHEET_ID")
        self.creds = self._get_credentials()

    def _get_credentials(self):
        """Retrieve credentials from an environment variable."""
        creds_json = os.getenv('GOOGLE_CREDENTIALS')
        if creds_json is None:
            raise ValueError("GOOGLE_CREDENTIALS environment variable not set.")
        creds_dict = json.loads(creds_json)
        return Credentials.from_service_account_info(creds_dict, scopes=[
            "https://spreadsheets.google.com/feeds", 
            "https://www.googleapis.com/auth/drive"
        ])

    def write_to_google_sheet(self, data):
        # Authorize the client with credentials
        client = gspread.authorize(self.creds)

        # Open the Google Sheet by its ID
        sheet = client.open_by_key(self.sheet_id).sheet1

        # Prepare the row to insert based on the column structure
        row = [
            data.get("first_name", ""),           # Ismi
            data.get("last_name", ""),            # Familiyasi
            data.get("middle_name", ""),          # Sharifi
            data.get("contract_number", ""),      # Shartnoma raqami
            data.get("pnfl", ""),                 # PINFL
            data.get("payment", ""),              # To'lov summasi
            data.get("payment_app", ""),          # To'lov ilovasi
            data.get("Дата", ""),                 # Sanasi
        ]

        # Append the row to the sheet
        sheet.append_row(row)
        print("Data written successfully!")

