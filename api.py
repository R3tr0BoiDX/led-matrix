from http.server import BaseHTTPRequestHandler, HTTPServer
import json

# todo: add this to led display, receive brightness, color, and effect

# Define a simple HTTP server that listens on port 8080
class SimpleHandler(BaseHTTPRequestHandler):

    def do_POST(self):
        # Check if content type is application/json
        content_length = int(self.headers["Content-Length"])
        post_data = self.rfile.read(content_length).decode("utf-8")

        try:
            # Parse the JSON payload
            data = json.loads(post_data)
            print(f"Received data: {data}")

            # Respond with the received JSON data
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            response = {"code": 200, "message": "OK"}
            self.wfile.write(json.dumps(response).encode("utf-8"))

        except json.JSONDecodeError:
            # Handle invalid JSON
            self.send_response(400)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"error": "Invalid JSON"}).encode("utf-8"))


def run(server_class=HTTPServer, handler_class=SimpleHandler, port=8080):
    server_address = ("", port)
    httpd = server_class(server_address, handler_class)
    print(f"Starting server on port {port}")
    httpd.serve_forever()


if __name__ == "__main__":
    run()
