default ui_selected_training_word = ""
default ui_selected_core_word = ""

# Word lists from data/words.json, keyed by the Korean syllable group.
init python:
    import json, os

    with renpy.open_file("data/words.json", encoding="utf-8") as _f:
        ui_word_pool = json.load(_f)

    # The assessment screen labels syllables in English; words.json uses Korean keys.
    UI_SYLLABLE_KEYS = {"Si": "시", "Se": "세", "Sa": "사", "Seo": "서", "So": "소", "Su": "수", "Seu": "스"}

    def ui_core_words():
        """Return the key-word choices for the best syllable in syllable_result.json."""
        syllable = None
        try:
            # Read from disk: the voice engine rewrites this file after each assessment.
            with open(os.path.join(renpy.config.gamedir, "data", "syllable_result.json"), encoding="utf-8") as f:
                syllable = json.load(f).get("best")
        except Exception as e:
            renpy.log("Could not read syllable_result.json: %r" % e)
        key = UI_SYLLABLE_KEYS.get(syllable, syllable)
        # Fall back to 사 so the screen never opens empty if the result is missing.
        return tuple(ui_word_pool.get(key, ui_word_pool["사"])["core"])

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
