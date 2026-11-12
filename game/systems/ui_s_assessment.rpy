screen ui_s_assessment(record_action=None):

    modal True

    default syllable_index = 0

    $ syllables = ("시", "세", "사", "서", "소", "수", "스")

    # 위쪽 평가 패널
    frame:
        xalign 0.5
        ypos 50
        xsize 1400
        padding (50, 15)
        background Solid("#FFF4DE")

        vbox:
            xfill True
            spacing 8

            text "초기 발음 평가":
                xalign 0.5
                size 28
                color "#665779"

            text "아래 글자를 천천히 말해 주세요.":
                xalign 0.5
                size 26
                color "#30263F"

            text syllables[syllable_index]:
                xalign 0.5
                size 80
                color "#30263F"

            text "{} / 7".format(syllable_index + 1):
                xalign 0.5
                size 24
                color "#665779"

    # 녹음 및 진행 버튼
    vbox:
        xalign 0.5
        ypos 340
        spacing 20

        textbutton "녹음 시작":
            xalign 0.5
            xysize (280, 90)

            background Solid("#705497")
            hover_background Solid("#9170BB")
            insensitive_background Solid("#55505F")

            text_size 36
            text_color "#FFFFFF"
            text_insensitive_color "#BBBBBB"
            text_xalign 0.5
            text_yalign 0.5

            sensitive record_action is not None
            action record_action

        if syllable_index < len(syllables) - 1:

            textbutton "다음 음절":
                xalign 0.5
                padding (35, 15)

                background Solid("#705497")
                hover_background Solid("#9170BB")

                text_size 32
                text_color "#FFFFFF"

                action SetScreenVariable(
                    "syllable_index",
                    syllable_index + 1
                )

        else:

            textbutton "마치기":
                xalign 0.5
                padding (35, 15)

                background Solid("#705497")
                hover_background Solid("#9170BB")

                text_size 32
                text_color "#FFFFFF"

                action Return()