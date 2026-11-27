default ui_selected_core_word = ""
# Kept across restarts so chapter select still uses the child's key word.
default persistent.ui_core_word = ""

# Word lists from data/words.json, keyed by the Korean syllable group.
init python:
    import json, os

    with renpy.open_file("data/words.json", encoding="utf-8") as _f:
        ui_word_pool = json.load(_f)

    # The assessment screen labels syllables in English; words.json uses Korean keys.
    UI_SYLLABLE_KEYS = {"Si": "시", "Se": "세", "Sa": "사", "Seo": "서", "So": "소", "Su": "수", "Seu": "스"}

    def ui_result_words(field, fallback):
        """Return the word lists for the "best" or "worst" syllable in syllable_result.json."""
        syllable = None
        try:
            # Read from disk: the voice engine rewrites this file after each assessment.
            with open(os.path.join(renpy.config.gamedir, "data", "syllable_result.json"), encoding="utf-8") as f:
                syllable = json.load(f).get(field)
        except Exception as e:
            renpy.log("Could not read syllable_result.json: %r" % e)
        key = UI_SYLLABLE_KEYS.get(syllable, syllable)
        # Use a fixed syllable when the result is missing (e.g. a chapter started from chapter select).
        key = key if key in ui_word_pool else fallback
        # Read from the DB (target_words) when db_server.py is running, otherwise from words.json.
        return db_words(key) or ui_word_pool[key]

    def ui_core_words():
        """Return the key-word choices for the best syllable."""
        return ui_result_words("best", "사")["core"]

    def ui_saved_core_word():
        """Return the last chosen key word, or the first best-syllable word if it no longer fits."""
        words = ui_core_words()
        # A newer assessment may have a different best syllable than the saved word.
        return persistent.ui_core_word if persistent.ui_core_word in words else words[0]

    def ui_target_words():
        # Fallback 수 differs from the key-word fallback 사, so the two never share a syllable.
        return ui_result_words("worst", "수")["target"]

    def ui_target_word(monster, targets=None):
        targets = ui_target_words() if targets is None else targets
        return renpy.random.choice(targets[monster])

    def ui_retry_target_words(monster, current_word, targets=None):
        targets = ui_target_words() if targets is None else targets
        alternatives = [word for word in targets.get(monster, []) if word != current_word]
        return alternatives or [current_word]

    def ui_final_boss_words(targets):
        # The opening CV item is the assessed syllable itself.
        syllable = ui_target_word("ch1_m1", targets)
        chapter2_words = targets.get("ch2_m1", [])
        matching_words = [word for word in chapter2_words if word.startswith(syllable)]
        return (syllable, renpy.random.choice(matching_words or [syllable]),
                intro_recording_sentence)

screen ui_word_selection(title, words):

    modal True
    default selected_word = None

    add "apartment lobby"
    add Solid("#10152F42")

    add "ui_ghost intro_idle" at ghost_float:
        xysize (480, 560)
        fit "contain"
        align (0.05, 0.55)

    fixed:
        xysize (1150, 648)
        xpos 640
        ypos 172

        add intro_ch1_ui + "panel_assessment.png" xysize (1150, 648) fit "fill" alpha 0.85

        vbox:
            xalign 0.5
            ypos 36
            spacing 17

            text title style "intro_ch1_text" xalign 0.5 size 51 bold True
            text "Pick one word you like." style "intro_ch1_caption" xalign 0.5

            viewport:
                xsize 940
                ysize 313
                mousewheel True
                draggable True
                scrollbars "vertical"

                vpgrid:
                    cols 3
                    spacing 18

                    for word in words:
                        use intro_ch1_button(word, "next", SetScreenVariable("selected_word", word),
                            width=285, height=135, chosen=selected_word == word)

            fixed:
                xysize (330, 82)
                xalign 0.5
                use intro_ch1_button("Done", "continue", Return(selected_word),
                    width=330, height=82, enabled=selected_word is not None)
