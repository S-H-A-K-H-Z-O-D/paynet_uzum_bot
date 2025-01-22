import asyncio
from telegramm import ReaderBot


def main():
  
    # Initialize ReaderBot - User Bot handling messages
    reader_bot = ReaderBot()

    print("User bot is running...")

    # Run user bot handler loop asynchronously. Telethon requires event handling, asyncio loop handles everything.
    async def start_bot():
        await reader_bot.run()
    
    asyncio.run(start_bot()) #Execute loop.


if __name__ == "__main__":
    main()