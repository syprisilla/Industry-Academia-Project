screen ui_s_assessment(record_action=None):

    modal True

    default syllable_index = 0
    default ui_record_state = "ready"

    $ syllables = ("시", "세", "사", "서", "소", "수", "스")

    frame:
        xalign 0.5
        ypos 55
        xsize 1500
        padding (30, 18)
        background Solid("#FFF4DC")

        vbox:
            xalign 0.5
            spacing 10

            text "초기 발음 평가":
                xalign 0.5
                size 28
                color "#70558F"

            text "아래 글자를 천천히 말해 주세요.":
                xalign 0.5
                size 26
                color "#342743"

            text syllables[syllable_index]:
                xalign 0.5
                size 76
                color "#342743"

            text "[syllable_index + 1] / 7":
                xalign 0.5
                size 24
                color "#70558F"

    vbox:
        xalign 0.5
        ypos 365
        spacing 20

        button:
            xalign 0.5
            padding (24, 14)
            background Solid("#73558F")
            hover_background Solid("#8B6BAB")

            sensitive ui_record_state != "done"

            action SetScreenVariable(
                "ui_record_state",
                "done" if ui_record_state == "recording" else "recording"
            )

            hbox:
                spacing 14

                add "images/ui/mic.png":
                    xysize (48, 48)
                    fit "contain"
                    yalign 0.5

                if ui_record_state == "ready":
                    text "녹음 시작":
                        size 32
                        color "#FFFFFF"
                        yalign 0.5

                elif ui_record_state == "recording":
                    text "녹음중 (누르면 완료)":
                        size 32
                        color "#FFFFFF"
                        yalign 0.5

                else:
                    text "녹음 완료":
                        size 32
                        color "#FFFFFF"
                        yalign 0.5

        if syllable_index < len(syllables) - 1:

            textbutton "다음 음절":
                xalign 0.5
                action [
                    SetScreenVariable("ui_record_state", "ready"),
                    SetScreenVariable(
                        "syllable_index",
                        syllable_index + 1
                    )
                ]

        else:

            textbutton "평가 마치기":
                xalign 0.5
                action Return()