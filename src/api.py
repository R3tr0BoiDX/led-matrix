import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from typing import Dict

from src import settings, log
from src.display.base import Display, StubDisplay

PORT = settings.Network().get_api_port()

logger = log.get_logger(__name__)


# Define a simple HTTP server that listens on the specified port
class SimpleHandler(BaseHTTPRequestHandler):

    def __init__(self, *args, display: Display, **kwargs):
        self.display = display
        super().__init__(*args, **kwargs)

    def do_POST(self):
        # Check if content type is application/json
        content_length = int(self.headers["Content-Length"])
        post_data = self.rfile.read(content_length).decode("utf-8")

        try:
            # Parse the JSON payload
            data = json.loads(post_data)
            logger.debug("Received data: %s", data)

            # Respond with the received JSON data
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            response = {"code": 200, "message": "OK"}
            self.wfile.write(json.dumps(response).encode("utf-8"))
            logger.debug("Response sent: %s", response)

            # Process the received data
            self.process_data(data)

        except json.JSONDecodeError:
            # Handle invalid JSON
            self.send_response(400)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"error": "Invalid JSON"}).encode("utf-8"))
            logger.warning("Invalid JSON data received")

    def process_data(self, data: Dict):
        if "brightness" in data:
            logger.debug("Brightness found in data: %s", data["brightness"])
            brightness = int(data["brightness"])
            self.display.set_brightness(brightness)


def run(display=None):
    def handler(*args, **kwargs):
        # Pass the display to the handler
        SimpleHandler(display=display, *args, **kwargs)

    server_address = ("", PORT)
    httpd = HTTPServer(server_address, handler)
    logger.info("Starting server on port %s", PORT)
    httpd.serve_forever()


if __name__ == "__main__":
    stub = StubDisplay()
    run(display=stub)
