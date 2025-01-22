import os
from telethon import TelegramClient, events

from dotenv import load_dotenv
from sheet import Sheet
from .text_to_json import TextToJson


load_dotenv(dotenv_path=".env")

api_id = os.getenv("API_ID")
api_hash = os.getenv("API_HASH")
session = "user"

paynet_group_chat_id = int(os.getenv("PAYNET_GROUP_CHAT_ID"))
paynet_bot_id = int(os.getenv("PAYNET_BOT_ID"))

uzum_group_chat_id = int(os.getenv("UZUM_GROUP_CHAT_ID"))
uzum_bot_id = int(os.getenv("UZUM_BOT_ID"))


class ReaderBot:
         
    def __init__(self):
         if not api_id or not api_hash or not paynet_group_chat_id:
            raise ValueError(
                "API_ID, API_HASH or GROUP_CHAT_ID must be defined in .env"
            )

         self.client = TelegramClient(session, int(api_id), api_hash)


    async def handle_message(self, event):
            """ Process message and write to google sheets """
            message = event.message
            
            if  message.from_id and (message.from_id.user_id == paynet_bot_id or message.from_id.user_id == uzum_bot_id):
                 formatted_payment_data = TextToJson(message.message).check()
                 
                 if formatted_payment_data is not None:                    
                    print(f"Processing message from user: {message.from_id.user_id}, Data: {formatted_payment_data}")
                    Sheet().write_to_google_sheet(formatted_payment_data)
                    print("Payment data written to Google Sheets.")

                    
    async def run(self):
        """ Fetch messages and process payment notifications """
        try:
          await self.client.start() #Client starting, async part
          print(f"Listening for new messages in groups: {paynet_group_chat_id} and {uzum_group_chat_id}")

          #Add an event handler here instead, that will be looping on an incoming user event message from given specific telegram ID:
          @self.client.on(events.NewMessage(chats=[paynet_group_chat_id, uzum_group_chat_id]))
          async def handler(event):
                await self.handle_message(event)
            
          await self.client.run_until_disconnected()

        except Exception as e:
           print(f"An error occurred: {e}")
        finally:
          if self.client and self.client.is_connected():
            await self.client.disconnect() #Only when an event stops executing - then safely disconnect for memory purposes
            print("Disconnected...")