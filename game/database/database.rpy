init python:

    def save_player_to_db(name):

        result = renpy.fetch(
            "http://127.0.0.1:8765/players",
            json={"name": name},
            result="json"
        )

        if not result.get("ok"):
            raise Exception("Could not save to the database.")

        return result["player_id"]