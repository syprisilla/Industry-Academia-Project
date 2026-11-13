screen ui_s_assessment(record_action=None):

    modal True

    default syllable_index = 0
    default syll_state = "ready"          # ready → done (글자별)
    default phase = "record"              # record(7글자 녹음) → result(선정 결과)
    default syll_result = {"status": None, "selected": None, "image": ""}

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

            if phase == "record":

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

            else:   # result

                text "가장 정확하게 발음한 글자예요!":
                    xalign 0.5
                    size 28
                    color "#70558F"

    if phase == "record":

        vbox:
            xalign 0.5
            ypos 365
            spacing 20

            if syll_state == "recording":

                # 녹음 중 메시지 + 타이머가 실제 녹음 실행
                text "🎙 녹음 중... 말하세요!":
                    xalign 0.5
                    size 34
                    color "#73558F"

                timer 0.05 action Function(do_syll_record, syllables[syllable_index], syllable_index + 1)

            else:

                # 녹음 버튼 (ready/done)
                button:
                    xalign 0.5
                    padding (24, 14)
                    background Solid("#73558F")
                    hover_background Solid("#8B6BAB")
                    sensitive syll_state == "ready"
                    action SetScreenVariable("syll_state", "recording")

                    hbox:
                        spacing 14
                        add "images/ui/mic.png":
                            xysize (48, 48)
                            fit "contain"
                            yalign 0.5
                        text ("녹음 시작" if syll_state == "ready" else "녹음 완료 ✓"):
                            size 32
                            color "#FFFFFF"
                            yalign 0.5

                # 녹음 완료해야만 다음으로
                if syll_state == "done":

                    if syllable_index < len(syllables) - 1:
                        textbutton "다음 음절":
                            xalign 0.5
                            action [
                                SetScreenVariable("syll_state", "ready"),
                                SetScreenVariable("syllable_index", syllable_index + 1),
                            ]
                    else:
                        textbutton "평가 마치기":
                            xalign 0.5
                            action [
                                Function(do_syll_select),
                                SetScreenVariable("phase", "result"),
                            ]
    else:   # phase == "result"

        vbox:
            xalign 0.5
            ypos 330
            spacing 20

            if syll_result.get("selected"):
                add im.Image(syll_result["image"]):
                    xysize (300, 300)
                    fit "contain"
                    xalign 0.5
                text syll_result["selected"]:
                    xalign 0.5
                    size 48
                    color "#342743"
            else:
                text "선정할 글자를 찾지 못했어요. 다시 평가해 주세요.":
                    xalign 0.5
                    size 28
                    color "#342743"

            textbutton "확인":
                xalign 0.5
                action Return(syll_result.get("selected"))