import json
import sqlite3
from pathlib import Path
from urllib.parse import urlparse, parse_qs
from http.server import BaseHTTPRequestHandler, HTTPServer

DB_PATH = Path(__file__).resolve().parent.parent / "data" / "pronunciation.db"
SCHEMA_PATH = DB_PATH.parent.parent / "database" / "schema.sql"
WORDS_PATH = DB_PATH.parent / "words.json"
REFERENCE_PATH = DB_PATH.parent / "reference_by_syllable.json"


def init_db():
    """Create the tables and fill the word list and reference values."""
    with sqlite3.connect(DB_PATH) as conn:
        conn.executescript(SCHEMA_PATH.read_text(encoding="utf-8"))

        # shortcut: seeds only an empty table, add an update script when words.json changes
        if not conn.execute("SELECT 1 FROM target_words LIMIT 1").fetchone():
            rows = []
            for syllable, lists in json.loads(WORDS_PATH.read_text(encoding="utf-8")).items():
                rows += [(w, None, None, syllable, "core") for w in lists["core"]]
                for slot, words in lists["target"].items():
                    chapter, level = slot.split("_")   # "ch2_m1" -> chapter 2, level "m1"
                    rows += [(w, int(chapter[2:]), level, syllable, "target") for w in words]
            conn.executemany("INSERT INTO target_words (word_text, chapter, difficulty_level, syllable, pool_type)"
                             " VALUES (?, ?, ?, ?, ?)", rows)

        # cog_hz is CoG; sd_hz (spread) is the spectral variance. REPLACE keeps them in step with the JSON.
        reference = json.loads(REFERENCE_PATH.read_text(encoding="utf-8"))
        conn.executemany("INSERT OR REPLACE INTO reference_stats VALUES (?, ?, ?, ?, ?)",
                         [(s, r["cog_hz"]["mean"], r["cog_hz"]["std"], r["sd_hz"]["mean"], r["sd_hz"]["std"])
                          for s, r in reference.items()])


def get_words(conn, q):
    """Return one syllable's lists in the same shape as a words.json entry."""
    out = {"core": [], "target": {}}
    rows = conn.execute("SELECT word_text, chapter, difficulty_level, pool_type FROM target_words"
                        " WHERE syllable = ? ORDER BY word_id", (q["syllable"],))
    for word, chapter, level, pool in rows:
        if pool == "core":
            out["core"].append(word)
        else:
            out["target"].setdefault("ch%d_%s" % (chapter, level), []).append(word)
    if not out["core"]:
        raise KeyError(q["syllable"])
    return out


GET_ROUTES = {"/words": get_words}


class DBHandler(BaseHTTPRequestHandler):

    def send_json(self, data):
        response = json.dumps(dict(ok=True, **data), ensure_ascii=False).encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(response)

    def run_route(self, handler, data):
        try:
            with sqlite3.connect(DB_PATH) as conn:
                result = handler(conn, data)
        except (KeyError, ValueError, TypeError, sqlite3.Error) as e:
            # Missing or bad fields: report them instead of dropping the connection.
            self.send_error(400, repr(e))
            return
        self.send_json(result)

    def do_GET(self):
        url = urlparse(self.path)
        if url.path not in GET_ROUTES:
            self.send_error(404)
            return
        self.run_route(GET_ROUTES[url.path], {k: v[0] for k, v in parse_qs(url.query).items()})

    def do_POST(self):
        self.send_error(404)


init_db()
server = HTTPServer(("127.0.0.1", 8765), DBHandler)
print("SQLite connection server is running")
server.serve_forever()