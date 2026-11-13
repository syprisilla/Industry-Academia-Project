default ui_selected_training_word = ""


screen ui_word_selection(title, words):

    modal True
    default selected_word = None

    add "apartment lobby"
    add Solid("#15152599")

    add "ui_ghost intro_idle" at ghost_float:
        xysize (480, 560)
        fit "contain"
        align (0.05, 0.55)

    frame:
        xalign 0.85
        yalign 0.45
        xsize 1100
        padding (45, 40)
        background Solid("#29263EEB")

        vbox:
            spacing 30
            xfill True

            text title:
                xalign 0.5
                size 52
                color "#FFF2C7"

            text "연습할 단어를 하나 골라 주세요.":
                xalign 0.5
                size 30
                color "#FFFFFF"

            viewport:
                xsize 1010
                ysize 340
                mousewheel True
                draggable True
                scrollbars "vertical"

                vpgrid:
                    cols 3
                    spacing 20

                    for word in words:
                        textbutton word:
                            xysize (310, 145)

                            background Solid("#48415F")
                            hover_background Solid("#625779")
                            selected_background Solid("#8265A7")
                            selected_hover_background Solid("#9375B8")

                            text_size 44
                            text_color "#FFFFFF"
                            text_xalign 0.5
                            text_yalign 0.5

                            selected selected_word == word
                            action SetScreenVariable(
                                "selected_word", word
                            )

            textbutton "선택 완료":
                xalign 0.5
                padding (45, 18)

                background Solid("#705497")
                hover_background Solid("#9170BB")
                insensitive_background Solid("#454052")

                text_size 34
                text_color "#FFFFFF"
                text_insensitive_color "#999999"

                sensitive selected_word is not None
                action Return(selected_word)
