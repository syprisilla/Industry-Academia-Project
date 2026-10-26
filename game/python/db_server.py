import json
import sqlite3
from pathlib import Path
from http.server import BaseHTTPRequestHandler, HTTPServer

DB_PATH = Path(__file__).resolve().parent.parent / "data" / "pronunciation.db"


class DBHandler(BaseHTTPRequestHandler):

    def do_POST(self):
        if self.path != "/players":
            self.send_error(404)
            return

        length = int(self.headers.get("Content-Length", 0))
        data = json.loads(self.rfile.read(length))
        name = data["name"]

        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.execute(
                "INSERT INTO players (name) VALUES (?)",
                (name,)
            )
            player_id = cursor.lastrowid
            conn.commit()

        response = json.dumps({
            "ok": True,
            "player_id": player_id
        }).encode("utf-8")

        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(response)


server = HTTPServer(("127.0.0.1", 8765), DBHandler)
print("SQLite 연결 서버 실행 중")
server.serve_forever()