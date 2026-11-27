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


def start_session(conn, d):
    """Find or create the child by name, then open a new session."""
    # Look up first: INSERT OR IGNORE would still use up an AUTOINCREMENT id and leave gaps.
    row = conn.execute("SELECT child_id FROM children WHERE name = ?", (d["name"],)).fetchone()
    child_id = row[0] if row else conn.execute("INSERT INTO children (name) VALUES (?)", (d["name"],)).lastrowid
    session_id = conn.execute("INSERT INTO sessions (child_id) VALUES (?)", (child_id,)).lastrowid
    return {"child_id": child_id, "session_id": session_id}


def save_core_word(conn, d):
    conn.execute("UPDATE children SET core_word = ?, vowel_environment = ? WHERE child_id = ?",
                 (d["core_word"], d.get("syllable"), d["child_id"]))
    return {}


def log_attempt(conn, d):
    # The same text can be a core word and a target word; prefer this monster's slot, then any target.
    chapter, _, level = (d.get("slot") or "").partition("_")
    word = conn.execute("SELECT word_id FROM target_words WHERE word_text = ?"
                        " ORDER BY (chapter = ? AND difficulty_level = ?) DESC, pool_type = 'core', word_id LIMIT 1",
                        (d["word_text"], int(chapter[2:]) if chapter[2:].isdigit() else None, level)).fetchone()
    attempt_number = conn.execute("SELECT COUNT(*) + 1 FROM attempt_log WHERE session_id = ? AND set_number = ?",
                                  (d["session_id"], d["set_number"])).fetchone()[0]
    attempt_id = conn.execute(
        "INSERT INTO attempt_log (session_id, word_id, word_text, set_number, attempt_number, result, cog, spectral_variance)"
        " VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
        (d["session_id"], word and word[0], d["word_text"], d["set_number"], attempt_number,
         d["result"], d.get("cog"), d.get("spectral_variance"))).lastrowid
    return {"attempt_id": attempt_id, "attempt_number": attempt_number}


def end_boss(conn, d):
    conn.execute("UPDATE sessions SET boss_result = ? WHERE session_id = ?", (d["boss_result"], d["session_id"]))
    return {}


GET_ROUTES = {"/words": get_words}
POST_ROUTES = {"/sessions": start_session, "/children/core": save_core_word,
               "/attempts": log_attempt, "/sessions/boss": end_boss}


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
        if self.path in POST_ROUTES:
            length = int(self.headers.get("Content-Length", 0))
            try:
                data = json.loads(self.rfile.read(length) or b"{}")
            except ValueError as e:
                self.send_error(400, repr(e))
                return
            self.run_route(POST_ROUTES[self.path], data)
            return
        self.send_error(404)


init_db()
server = HTTPServer(("127.0.0.1", 8765), DBHandler)
print("SQLite connection server is running")
server.serve_forever()