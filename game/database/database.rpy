# --------------------------------------------------
# PPT p16 tables (children, sessions, attempt_log, target_words, reference_stats)
# Every call fails quietly, so the game runs as before when db_server.py is off.
# --------------------------------------------------
init python:
    import json, urllib.parse, urllib.request

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
