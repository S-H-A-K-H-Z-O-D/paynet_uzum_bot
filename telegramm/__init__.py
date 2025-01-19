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
import json
import re
from telethon import TelegramClient, events
from google.oauth2.service_account import Credentials

from dotenv import load_dotenv
from sheet import Sheet
from .text_to_json import TextToJson


load_dotenv(dotenv_path=".env")


class ReaderBot:
    def __init__(self):
         self.api_id = os.getenv("API_ID")
         self.api_hash = os.getenv("API_HASH")
         self.session = "user"
         self.group_chat_id = os.getenv("GROUP_CHAT_ID")  # Get the group chat ID from .env

         if not self.api_id or not self.api_hash or not self.group_chat_id:
            raise ValueError(
                "API_ID, API_HASH or GROUP_CHAT_ID must be defined in .env"
            )

         self.client = TelegramClient(self.session, int(self.api_id), self.api_hash)

         self.informer_bot_id = None
         informer_bot_id_str = os.getenv("INFORMER_BOT_ID")

         if informer_bot_id_str is None:
            print("INFORMER_BOT_ID not found")

         try:
           self.informer_bot_id = int(informer_bot_id_str) #Cast the botid before even code started, to remove that issue
         except ValueError as e:
           print(f"Failed to convert INFORMER_BOT_ID to int: {e}")


    async def handle_message(self, event):
            """ Process message and write to google sheets """
            message = event.message
            
            if  message.from_id and message.from_id.user_id == self.informer_bot_id:

                 formatted_payment_data = TextToJson(message.message).check()
                 
                 if formatted_payment_data is not None:
                    
                    print(f"Processing message from user: {message.from_id.user_id}, Data: {formatted_payment_data}")
                    Sheet().write_to_google_sheet(formatted_payment_data)
                    print("Payment data written to Google Sheets.")

                    
    async def run(self):
        """ Fetch messages and process payment notifications """
        try:
          await self.client.start() #Client starting, async part
          print(f"Listening for new messages in group: {self.group_chat_id}")

          #Add an event handler here instead, that will be looping on an incoming user event message from given specific telegram ID:
          @self.client.on(events.NewMessage(chats=[int(self.group_chat_id)]))
          async def handler(event):
                await self.handle_message(event)
            
          await self.client.run_until_disconnected() #The client now *always runs until you disconnect*. All logic moves here!

        except Exception as e:
           print(f"An error occurred: {e}")
        finally:
          if self.client and self.client.is_connected():
            await self.client.disconnect() #Only when an event stops executing - then safely disconnect for memory purposes
            print("Disconnected...")