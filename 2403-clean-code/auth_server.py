from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qsl


class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()

        self.server: "Server"
        self.server.query_params = dict(parse_qsl(self.path.split("?")[1]))
        self.wfile.write(b"<h1>Authorised!</h1>")


class Server(HTTPServer):
    def __init__(self, host: str, port: int) -> None:
        super().__init__((host, port), RequestHandler)
        self.query_params: dict[str, str] = {}
