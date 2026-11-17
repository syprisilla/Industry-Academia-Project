init python:
    def ui_assess_ghost(show):
        # Hide the ghost during the failure notice; restore its position and float on restart.
        if show:
            renpy.show("ui_ghost intro_explain", at_list=[ui_ghost_position, ghost_float])
            renpy.transition(Dissolve(0.2), layer="master")
        else:
            renpy.hide("ui_ghost")

    def ui_assess_finish():
        do_syll_select()
        if renpy.get_screen_variable("syll_result", screen="ui_s_assessment").get("status") != "ok":
            ui_assess_ghost(False)

screen ui_s_assessment(record_action=None):

    modal True
    default syllable_index = 0
    default syll_state = "ready"
    default ui_record_state = "ready"
    default phase = "record"
    default syll_result = {"status": None, "selected": None, "image": ""}

    $ syllables = ("Si", "Se", "Sa", "Seo", "So", "Su", "Seu")
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
                        Function(ui_assess_finish),
                        SetScreenVariable("phase", "result"),
                    ])

    elif syll_result.get("status") == "ok":

        # Best/worst result cards
        text "Sound Check Results" style "intro_ch1_text" size 68 bold True xpos 852 xanchor 0.5 ypos 175 yanchor 0.5

        fixed:
            xysize (868, 484)
            xpos 852
            xanchor 0.5
            ypos 240
            add intro_ch1_ui + "panel_assessment.png" xysize (868, 484) fit "fill" alpha 0.84

            for i, (card, label, color, syl) in enumerate((
                    ("card_clearest.png", "Clearest sound", "#8FE3C0", syll_result.get("best")),
                    ("card_practice.png", "Sound to practice", "#C3BDF5", syll_result.get("worst")))):
                fixed:
                    xysize (380, 360)
                    pos (45 + i * 398, 62)
                    add intro_ch1_ui + card
                    text label style "intro_ch1_text" color color size 34 bold True xalign 0.5 ypos 80 yanchor 0.5
                    text syl style "intro_ch1_text" size 120 xalign 0.5 ypos 240 yanchor 0.5

        fixed:
            xysize (246, 64)
            xpos 852
            xanchor 0.5
            ypos 778
            use intro_ch1_button("Continue", "continue",
                Return((syll_result.get("best"), syll_result.get("worst"))),
                width=246, height=64)

    else:

        # Not enough valid sounds: restart the assessment from the first sound.
        add Solid("#10152F88")

        text "Sound Check" style "intro_ch1_text" size 68 bold True xalign 0.5 ypos 177 yanchor 0.5

        fixed:
            xysize (836, 470)
            xalign 0.5
            ypos 243
            add intro_ch1_ui + "panel_assessment.png" xysize (836, 470) fit "fill" alpha 0.84

            add intro_ch1_ui + "icon_ring.png" xysize (104, 104) xalign 0.5 ypos 122 yanchor 0.5
            add intro_ch1_ui + "icon_microphone.png" xysize (64, 64) fit "contain" xalign 0.5 ypos 122 yanchor 0.5
            text "Let’s try again" style "intro_ch1_text" color "#FFF1C4" size 60 bold True xalign 0.5 ypos 230 yanchor 0.5
            text "We didn’t get enough clear recordings." style "intro_ch1_text" size 34 xalign 0.5 ypos 306 yanchor 0.5
            text "Find a quiet spot and say each sound slowly." style "intro_ch1_caption" size 30 xalign 0.5 ypos 361 yanchor 0.5

        fixed:
            xysize (362, 64)
            xalign 0.5
            ypos 764
            use intro_ch1_button("Restart Sound Check", "record", [
                Function(ui_assess_ghost, True),
                SetScreenVariable("syllable_index", 0),
                SetScreenVariable("ui_record_state", "ready"),
                SetScreenVariable("phase", "record"),
            ], width=362, height=64)
