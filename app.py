import os
import asyncio
from dotenv import load_dotenv
from telegramm import ReaderBot


def main():
    # Load environment variables from .env file
    load_dotenv(dotenv_path=".env")
  
    # Initialize ReaderBot - User Bot handling messages
    reader_bot = ReaderBot()

    print("User bot is running...")

    # Run user bot handler loop asynchronously. Telethon requires event handling, asyncio loop handles everything.
    async def start_bot():
        await reader_bot.run() #Call run not handle_messages. The logic already exists with loop via `run()`  that was defined internally
    
    asyncio.run(start_bot()) #Execute loop.


if __name__ == "__main__":
    main()