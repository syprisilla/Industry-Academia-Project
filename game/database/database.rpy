# --------------------------------------------------
# PPT p16 tables (children, sessions, attempt_log, target_words, reference_stats)
# Every call fails quietly, so the game runs as before when db_server.py is off.
# --------------------------------------------------
default db_child_id = None
default db_session_id = None

init python:
    import json, os, urllib.parse, urllib.request

    def db_request(path, data=None):
        """Call db_server.py (POST when data is given); return the reply, or None if the server is not running."""
        # urllib, not renpy.fetch: renpy.fetch hangs when called from a button action.
        body = None if data is None else json.dumps(data).encode("utf-8")
        request = urllib.request.Request("http://127.0.0.1:8765" + path, data=body,
                                         headers={"Content-Type": "application/json"})
        try:
            with urllib.request.urlopen(request, timeout=1) as response:
                reply = json.load(response)
        except Exception as e:
            renpy.log("DB request failed (%s): %r" % (path, e))
            return None
        return reply if reply.get("ok") else None

    def db_words(syllable):
        """Return one syllable's word lists from target_words, shaped like a words.json entry."""
        return db_request("/words?syllable=" + urllib.parse.quote(syllable))

    def db_start_session():
        """Find or create the child by name and open a session."""
        reply = db_request("/sessions", {"name": player_name})
        if reply:
            store.db_child_id, store.db_session_id = reply["child_id"], reply["session_id"]

    def db_save_core_word(word):
        if db_child_id is None:
            db_start_session()
        try:
            with open(os.path.join(config.gamedir, "data", "syllable_result.json"), encoding="utf-8") as f:
                best = json.load(f).get("best")
        except Exception:
            best = None
        if db_child_id is not None:
            db_request("/children/core", {"child_id": db_child_id, "core_word": word,
                                          "syllable": UI_SYLLABLE_KEYS.get(best, best)})

    def db_log_attempt(monster_name, result, word, is_test):
        """Save one recorded attempt; test buttons and non-attempt events are skipped."""
        if is_test or not word:
            return
        if db_session_id is None:
            # Started from chapter select, so no session was opened at the name prompt.
            db_start_session()
        if db_session_id is None:
            return
        features = {}
        try:
            # word.json holds the latest recording; it is fresh only for a scored try of this word.
            if result in ("success", "fail"):
                with open(os.path.join(config.gamedir, "data", "word.json"), encoding="utf-8") as f:
                    data = json.load(f)
                if data.get("word") == word:
                    features = data.get("features") or {}
        except Exception:
            pass
        db_request("/attempts", {"session_id": db_session_id, "word_text": word,
                                 "slot": getattr(store, "monster", None),  # e.g. "ch2_m1" during a battle
                                 "set_number": success_count + 1, "result": result,
                                 "cog": features.get("cog_hz"), "spectral_variance": features.get("sd_hz")})

    def db_end_boss(result):
        if db_session_id is not None:
            db_request("/sessions/boss", {"session_id": db_session_id, "boss_result": result})
