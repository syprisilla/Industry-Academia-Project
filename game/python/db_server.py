import json
import sqlite3
from pathlib import Path
from http.server import BaseHTTPRequestHandler, HTTPServer

DB_PATH = Path(__file__).resolve().parent.parent / "data" / "pronunciation.db"


class DBHandler(BaseHTTPRequestHandler):

    def do_POST(self):
        self.send_error(404)


server = HTTPServer(("127.0.0.1", 8765), DBHandler)
print("SQLite connection server is running")
server.serve_forever()