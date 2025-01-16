import os
from telegramm import GetData, ReaderBot
from dotenv import load_dotenv

def main():
    # Load environment variables from .env file
    load_dotenv(dotenv_path=".env")
    
    bot_token = "7996386097:AAF_L8_MUsQT11ixUZT0Z2NW8-3FrQu7hB0"
    group_chat_id = "-1002253117682"

    if not bot_token or not group_chat_id:
        print("BOT_TOKEN or GROUP_CHAT_ID is missing in the .env file.")
        return

    # Initialize the GetData bot to listen for updates and extract payment data
    get_data_bot = GetData()

    # Initialize the ReaderBot to process messages from the group chat
    reader_bot = ReaderBot(bot_token, group_chat_id)

    print("Bot is running...")

    # Start the loop for both bots
    while True:
        # Get updates for GetData bot
        updates = get_data_bot.get_updates()
        if updates:
            data = get_data_bot.process_updates(updates)
            if data:
                # If payment data is extracted, write to Google Sheets
                print("Data processed successfully.")

        # Get updates for ReaderBot and process messages from the group
        group_updates = reader_bot.get_updates()
        if group_updates:
            for update in group_updates["result"]:
                message = update.get("message", {})
                reader_bot.process_message(message)
                # Update the offset to avoid reprocessing the same message
                reader_bot.offset = update["update_id"] + 1

if __name__ == "__main__":
    main()
