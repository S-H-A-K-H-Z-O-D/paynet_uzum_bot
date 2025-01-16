# import os
# import requests
# from dotenv import load_dotenv
# from .paynet import Paynet
# from .uzum import Uzum

# # Load environment variables from .env file
# load_dotenv(dotenv_path=".env")

# class GetData:
#     def __init__(self):
#         # Load the bot token from the .env file
#         self.BOT_TOKEN = os.getenv("BOT_TOKEN")
#         if not self.BOT_TOKEN:
#             raise ValueError("BOT_TOKEN is not set in the .env file.")
        
#         self.base_url = f"https://api.telegram.org/bot{self.BOT_TOKEN}"
#         self.offset = None  # Offset to avoid receiving duplicate messages
#         self.data = None  # Store the processed data

#     def get_updates(self):
#         """Fetch new updates (messages) from the bot."""
#         url = f"{self.base_url}/getUpdates"
#         params = {"offset": self.offset, "timeout": 10}
#         response = requests.get(url, params=params)
#         if response.status_code == 200:
#             return response.json()
#         else:
#             print(f"Error: {response.status_code}")
#             return None

#     def process_updates(self, updates):
#         """Process updates and filter messages in the group by the specified sender."""
#         if "result" in updates:
#             for update in updates["result"]:
#                 # Update the offset to avoid processing the same message again
#                 self.offset = update["update_id"] + 1

#                 # Extract message data
#                 if "message" in update:
#                     print(update)
#                     message = update["message"]
#                     chat_type = message.get("chat", {}).get("type", "")
#                     user = message.get("from", {})
#                     text = message.get("text", "")

#                     # Process messages only from groups or supergroups
#                     if chat_type in ["group", "supergroup"]:
#                         first_name = user.get("username", "")
#                         print(first_name)
#                         # if first_name == "paynet_transaction_bot":
#                         #     return Paynet(text).paynet_data()

#                         # elif first_name == "ApelsinAssistantbot":
#                         #     return Uzum(text).uzum_data()
#                         if first_name == "ShakhzodMatrasulov":
#                             return Paynet(text).paynet_data()

#                         elif first_name == "Shakhzod_Maab":
#                             return Uzum(text).uzum_data()
                        

import os
import requests
from dotenv import load_dotenv
from .paynet import Paynet
from .uzum import Uzum

# Load environment variables from .env file
load_dotenv(dotenv_path=".env")

class GetData:
    def __init__(self):
        # Load the bot token from the .env file
        self.BOT_TOKEN = "7340543076:AAFjPDt1KnA0HpC5tILP9SnmuJie7s-LC1U"
        if not self.BOT_TOKEN:
            raise ValueError("BOT_TOKEN is not set in the .env file.")
        
        self.base_url = f"https://api.telegram.org/bot{self.BOT_TOKEN}"
        self.offset = None  # Offset to avoid receiving duplicate messages
        self.data = None  # Store the processed data

    def get_updates(self):
        """Fetch new updates (messages) from the bot."""
        url = f"{self.base_url}/getUpdates"
        params = {"offset": self.offset, "timeout": 10}
        response = requests.get(url, params=params)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error: {response.status_code}")
            return None

    def process_updates(self, updates):
        """Process updates and filter messages in the group by the specified sender."""
        if "result" in updates:
            for update in updates["result"]:
                # Update the offset to avoid processing the same message again
                self.offset = update["update_id"] + 1

                # Extract message data
                if "message" in update:
                    print(update)
                    message = update["message"]
                    chat_type = message.get("chat", {}).get("type", "")
                    user = message.get("from", {})
                    text = message.get("text", "")

                    # Process messages only from groups or supergroups
                    if chat_type in ["group", "supergroup"]:
                        first_name = user.get("username", "")
                        print(first_name)
                        if first_name == "InformerBotUsername":  # Replace with the actual informer bot's username
                            return self.extract_payment_data(text)

                        elif first_name == "NURBEKOTAMURODOV":
                            return Paynet(text).paynet_data()

                        elif first_name == "NURBEKOTAMURODOV":
                            return Uzum(text).uzum_data()

    def extract_payment_data(self, text):
        """Parse and extract payment data."""
        data = {}
        if "payment" in text.lower():  # Replace with the actual logic to extract payment data
            data["payment"] = "1000"  # Replace with actual extracted payment value
        return data
    
from sheet import Sheet
import re
import json


class ReaderBot:
    def __init__(self, bot_token, group_chat_id):
        self.bot_token = bot_token
        self.group_chat_id = group_chat_id
        self.base_url = f"https://api.telegram.org/bot{self.bot_token}"
        self.offset = None  # Offset to avoid receiving duplicate messages

    def get_updates(self):
        """Fetch new updates (messages) from the bot."""
        url = f"{self.base_url}/getUpdates"
        params = {"offset": self.offset, "timeout": 10}
        response = requests.get(url, params=params)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error: {response.status_code}")
            return None

    def process_message(self, message):
        """Process incoming messages and extract payment data."""
        # Check if the message is from the informer bot (replace with actual username)
        if message.get("from", {}).get("username") == "NURBEKOTAMURODOV":  # Replace with actual informer bot username
            text = message.get("text", "")
            if "payment" in text.lower():  # Adjust this check as per the format of the payment message
                payment_data = self.extract_payment_data(text)
                if payment_data:
                    # Write the extracted data to Google Sheets
                    Sheet().write_to_google_sheet(payment_data)
                    print("Payment data written to Google Sheets.")

    def extract_payment_data(self, text):
        try:
            # Check for the presence of specific keywords to determine the format
            if "💰Сумма:" in text:  # First notification format
                # Match the payment amount
                amount_match = re.search(r"💰Сумма:\s*(\d+)", text)

                # Match the JSON-like user data
                user_data_match = re.search(r"🏷Данные пользователя:\s*({.*})", text)

                # Parse the user data JSON
                user_data = json.loads(user_data_match.group(1)) if user_data_match else {}

                # Extract data from user_data
                full_name = user_data.get("fio", "")
                contract_number = user_data.get("Shartnoma raqami", "")
                pinfl = user_data.get("ПИНФЛ", "")

                # Split full_name into first and last name
                name_parts = full_name.split()
                first_name = name_parts[0] if len(name_parts) > 0 else ""
                last_name = name_parts[-1] if len(name_parts) > 1 else ""

                return {
                    "payment": amount_match.group(1) if amount_match else "",
                    "contract_number": contract_number,
                    "first_name": first_name,
                    "last_name": last_name,
                    "pnfl": pinfl,
                }

            elif "Сумма транзакции:" in text:  # Second notification format
                # Match transaction amount
                amount_match = re.search(r"Сумма транзакции:\s*([\d\s]+)\s*сум", text)

                # Match client information
                client_match = re.search(r"Клиент:\s*([^\-]+)-(\d+)-(\d+)", text)

                # Extract data from client_match
                if client_match:
                    full_name = client_match.group(1).strip()
                    contract_number = client_match.group(2).strip()
                    pnfl = client_match.group(3).strip()

                    # Split full_name into first and last name
                    name_parts = full_name.split()
                    first_name = name_parts[0] if len(name_parts) > 0 else ""
                    last_name = name_parts[-1] if len(name_parts) > 1 else ""

                    return {
                        "payment": amount_match.group(1).replace(" ", "") if amount_match else "",
                        "contract_number": contract_number,
                        "first_name": first_name,
                        "last_name": last_name,
                        "pnfl": pnfl,
                    }

            else:
                print("Unrecognized notification format.")
                return None

        except Exception as e:
            print("Error parsing payment data:", e)
            return None

    def run(self):
        """Main loop to fetch and process updates."""
        print("Reader bot is running...")
        while True:
            updates = self.get_updates()
            if updates:
                for update in updates["result"]:
                    message = update.get("message", {})
                    self.process_message(message)
                    # Update the offset to avoid reprocessing the same message
                    self.offset = update["update_id"] + 1
