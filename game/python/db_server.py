import json
import sqlite3
from pathlib import Path
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


class DBHandler(BaseHTTPRequestHandler):

    def do_POST(self):
        self.send_error(404)


init_db()
server = HTTPServer(("127.0.0.1", 8765), DBHandler)
print("SQLite connection server is running")
server.serve_forever()