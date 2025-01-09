from http.server import BaseHTTPRequestHandler
import json
from sheet import Sheet
from telegram import GetData

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length).decode('utf-8')
        update = json.loads(post_data)  # This will contain the update from Telegram
        
        bot = GetData()
        data = bot.process_updates(json.loads(update))  # Process the Telegram update
        if data:
            Sheet().write_to_google_sheet(data)
            response_message = "Data processed and written successfully."
        else:
            response_message = "No relevant data to process."

        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(response_message.encode())
