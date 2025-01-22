from http.server import BaseHTTPRequestHandler
from sheet import Sheet
from telegramm.text_to_json import TextToJson
import json

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['Content-Length']) # <--- Gets the size of data
        post_data = self.rfile.read(content_length) # <--- Gets the data itself
        print(post_data) # <-- Print post data for debugging

        # Process incoming update from Telegram
        update = json.loads(post_data.decode('utf-8'))
        if "message" in update:
            # Handle the message
            message = update['message']
            formatted_payment_data = TextToJson(message['text']).check()
            if formatted_payment_data:
                Sheet().write_to_google_sheet(formatted_payment_data)

        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write("Received".encode())
