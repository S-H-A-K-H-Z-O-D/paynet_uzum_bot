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
                        

from dotenv import load_dotenv
from .paynet import Paynet
from .uzum import Uzum

# Load environment variables from .env file
load_dotenv(dotenv_path=".env")

class GetData:
    def __init__(self):
        pass  # No initialization required for BOT_TOKEN here
    
    def process_updates(self, update):
        message = update.get('message', {})
        chat_type = message.get("chat", {}).get("type", "")
        user = message.get("from", {})
        first_name = user.get("username", "")
        
        # if chat_type in ["group", "supergroup"] and first_name in ["paynet_transaction_bot", "ApelsinAssistantbot"]:
        #     if first_name == "paynet_transaction_bot":
        #         return Paynet(message.get("text", "")).paynet_data()
        #     elif first_name == "ApelsinAssistantbot":
        #         return Uzum(message.get("text", "")).uzum_data()
        # return None

        # if chat_type in ["group", "supergroup", "channel"]:
            # if first_name == "ShakhzodMatrasulov":
        return Paynet(message.get("text", "")).paynet_data()
            # elif first_name == "jhbwefkcjsb_bot":
                # return Uzum(message.get("text", "")).uzum_data()
        # return None
