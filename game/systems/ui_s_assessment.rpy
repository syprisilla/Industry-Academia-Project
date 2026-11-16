screen ui_s_assessment(record_action=None):

    modal True
    default syllable_index = 0
    default syll_state = "ready"
    default ui_record_state = "ready"
    default phase = "record"
    default syll_result = {"status": None, "selected": None, "image": ""}

    $ syllables = ("시", "세", "사", "서", "소", "수", "스")
    $ total_syllables = len(syllables)

    if phase == "record":

        fixed:
            xysize (1240, 350)
            xalign 0.5
            ypos 76
            add intro_ch1_ui + "panel_assessment.png" xysize (1240, 350) fit "fill" alpha 0.84

            vbox:
                xalign 0.5
                ypos 26
                spacing 8

                text "Sound Check" style "intro_ch1_caption" xalign 0.5 size 36
                text "Say the sound below slowly." style "intro_ch1_text" xalign 0.5 size 30

                fixed:
                    xysize (310, 126)
                    xalign 0.5
                    add intro_ch1_ui + "panel_word_focus.png" xysize (310, 126) fit "fill"
                    text syllables[syllable_index] style "intro_ch1_text" align (0.5, 0.5) size 75 bold True

                text "[syllable_index + 1] / [total_syllables]" style "intro_ch1_caption" xalign 0.5 size 28

                hbox:
                    xalign 0.5
                    spacing 10
                    for index in range(total_syllables):
                        $ dot = "done" if index < syllable_index else ("active" if index == syllable_index else "idle")
                        add intro_ch1_ui + "progress_dot_" + dot + ".png" xysize (24, 24)

        fixed:
            xysize (550, 118)
            xalign 0.5
            ypos 554
            use intro_ch1_recorder(ui_record_state,
                Function(do_syll_record, syllables[syllable_index], syllable_index + 1),
                enabled=True, width=550)

        if ui_record_state == "done":
            fixed:
                xysize (300, 76)
                xalign 0.5
                ypos 708
                if syllable_index < total_syllables - 1:
                    use intro_ch1_button("Next Sound", "next", [
                        SetScreenVariable("ui_record_state", "ready"),
                        SetScreenVariable("syllable_index", syllable_index + 1),
                    ])
                else:
                    use intro_ch1_button("Finish", "continue", [
                        Function(do_syll_select),
                        SetScreenVariable("phase", "result"),
                    ])

    else:

        fixed:
            xysize (700, 500)
            xalign 0.5
            ypos 120

            vbox:
                xalign 0.5
                spacing 20

                if syll_result.get("selected"):
                    text "This was your clearest sound!" style "intro_ch1_caption" xalign 0.5 size 34
                    add im.Image(syll_result["image"]):
                        xysize (300, 300)
                        fit "contain"
                        xalign 0.5
                    text syll_result["selected"] style "intro_ch1_text" xalign 0.5 size 60 bold True
                else:
                    text "No sound was picked. Please try again." style "intro_ch1_text" xalign 0.5 size 30

                use intro_ch1_button("OK", "continue", Return(syll_result.get("selected")),
                    width=200, height=70)