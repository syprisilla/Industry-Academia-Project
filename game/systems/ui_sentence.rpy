screen ui_sentence(sentence, record_action=None):

    modal True
    default ui_record_state = "ready"

    fixed:
        xysize (1640, 270)
        xalign 0.5
        ypos 140

        add intro_ch1_ui + "panel_sentence.png" xysize (1640, 270) fit "fill" alpha 0.82

        text "Read the sentence below" style "intro_ch1_caption":
            xalign 0.5
            ypos 32

        text sentence style "intro_ch1_text":
            xalign 0.5
            yalign 0.63
            xmaximum 1440
            size 66
            bold True

    vbox:
        xalign 0.5
        ypos 543
        spacing 14

        fixed:
            xysize (620, 128)
            xalign 0.5

            fixed:
                xysize (620, 118)
                align (0.5, 0.5)
                use intro_ch1_recorder(ui_record_state,
                    SetScreenVariable("ui_record_state", "done" if ui_record_state == "recording" else "recording"),
                    width=620)

        $ status = {"ready": "Ready to record.", "recording": "Recording...", "done": "Recording complete."}[ui_record_state]
        text status style "intro_ch1_caption" xalign 0.5 size 28

        fixed:
            xysize (600, 62)
            xalign 0.5
            use intro_ch1_status("Press the button and read the sentence clearly!", wide=True)

        textbutton "Next":
            xalign 0.5
            action Return()
            text_style "intro_ch1_caption"
            text_size 27
            text_color ("#EDE5FF" if ui_record_state == "done" else "#BDB1CD")
