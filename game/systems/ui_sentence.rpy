screen ui_sentence(sentence, record_action=None):

    modal True

    # 화면 위쪽 문장 패널
    frame:
        xalign 0.5
        ypos 90
        xsize 1400
        yminimum 220
        padding (50, 35)
        background Solid("#FFF4DE")

        vbox:
            xfill True
            spacing 20

            text "아래 문장을 읽어 주세요":
                xalign 0.5
                size 30
                color "#665779"

            text sentence:
                xalign 0.5
                xmaximum 1300
                textalign 0.5
                size 48
                color "#30263F"

    # 패널 아래 버튼
    vbox:
        xalign 0.5
        ypos 350
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

        textbutton "다음":
            xalign 0.5
            padding (35, 12)
            text_size 32
            action Return()