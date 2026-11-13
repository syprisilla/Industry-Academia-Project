screen ui_s_assessment(record_action=None):

    modal True
    default syllable_index = 0
    default syll_state = "ready"          # ready → done (글자별)
    default phase = "record"              # record(7글자 녹음) → result(선정 결과)
    default syll_result = {"status": None, "selected": None, "image": ""}

    $ syllables = ("시", "세", "사", "서", "소", "수", "스")
    $ total_syllables = len(syllables)

    fixed:
        xysize (1240, 350)
        xalign 0.5
        ypos 76
        add intro_ch1_ui + "panel_assessment.png" xysize (1240, 350) fit "fill" alpha 0.84

        vbox:
            xalign 0.5
            ypos 26
            spacing 8


            text "초기 발음 평가" style "intro_ch1_caption" xalign 0.5 size 36
            text "아래 글자를 천천히 말해 주세요." style "intro_ch1_text" xalign 0.5 size 30

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
            SetScreenVariable("ui_record_state", "done" if ui_record_state == "recording" else "recording"))

    fixed:
        xysize (300, 76)
        xalign 0.5
        ypos 708
        if syllable_index < total_syllables - 1:
            use intro_ch1_button("다음 음절", "next", [
                SetScreenVariable("ui_record_state", "ready"),
                SetScreenVariable("syllable_index", syllable_index + 1),
            ])
        else:
            use intro_ch1_button("평가 마치기", "continue", Return())

