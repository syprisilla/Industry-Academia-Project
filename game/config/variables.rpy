# --------------------------------------------------
# Player name
# --------------------------------------------------

default persistent.last_player_name = None
default player_name = persistent.last_player_name or "MC"

init python:
    def remember_player_name(name):
        if persistent.last_player_name != name:
            persistent.last_player_name = name
            renpy.save_persistent()

    def remember_legacy_player_name():
        if persistent.last_player_name is None and player_name and player_name != "MC":
            remember_player_name(player_name)

    config.after_load_callbacks.append(remember_legacy_player_name)


# --------------------------------------------------
# Choose a Korean particle based on the preceding word.
# --------------------------------------------------

init python:
    def josa(word, with_batchim, without_batchim):
        if not word:
            return without_batchim

        last = word[-1]


        if with_batchim == "이의" and without_batchim == "의":

            # The player entered a family name and given name.
            if len(word) >= 3:
                return "의"

            # The player entered only a given name.
            if '가' <= last <= '힣':
                jong = (ord(last) - ord('가')) % 28

                if jong != 0:
                    return "이의"
                else:
                    return "의"

            return "의"


        # --------------------------------------------------
        # General particle handling.
        # --------------------------------------------------

        # Check whether the last character is a Hangul syllable.
        if '가' <= last <= '힣':
            jong = (ord(last) - ord('가')) % 28

            # A syllable with a final consonant takes with_batchim.
            if jong != 0:
                return with_batchim

            # An open syllable takes without_batchim.
            return without_batchim

        # A non-Hangul character takes without_batchim by default.
        return without_batchim
