default ui_selected_training_word = ""

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
            text "연습할 단어를 하나 골라 주세요." style "intro_ch1_caption" xalign 0.5

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
                use intro_ch1_button("선택 완료", "continue", Return(selected_word),
                    width=330, height=82, enabled=selected_word is not None, icon="icon_next")
