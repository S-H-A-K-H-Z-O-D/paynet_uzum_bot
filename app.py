from telegram import GetData
from sheet import Sheet

def main():

    bot = GetData()
    data = None

    print("Bot is running...")
    while True:
        updates = bot.get_updates()
        if updates:
            data = bot.process_updates(updates)
            if data:
                Sheet().write_to_google_sheet(data)
                print("Data written successfully.")
            else:
                print("No data available.")



if __name__ == "__main__":
    main()

