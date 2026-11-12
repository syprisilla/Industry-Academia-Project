screen ui_sentence(sentence, record_action=None):

    default ui_record_state = "ready"

    #기존 패널 코드 유지

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

        
        button:
            xalign 0.5
            padding (24, 14)

            background Solid("#73558F")
            hover_background Solid("#8B6BAB")

            sensitive ui_record_state != "done"

            if ui_record_state == "ready":
                action SetScreenVariable("ui_record_state", "recording")
            elif ui_record_state == "recording":
                action SetScreenVariable("ui_record_state", "done")
            else:
                action SetScreenVariable("ui_record_state", "recording")

            hbox:
                spacing 14

                add "images/ui/mic.png":
                    xysize (48, 48)
                    fit"contain"
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


        textbutton "다음":
            xalign 0.5
            padding (35, 12)
            text_size 32
            action Return()