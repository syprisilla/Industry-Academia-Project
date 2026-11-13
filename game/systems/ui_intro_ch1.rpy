define intro_ch1_ui = "images/ui/intro_ch1/"

style intro_ch1_text is default:
    font gui.interface_text_font
    color "#F8F5FF"
    text_align 0.5
    outlines [(1, "#15152B88", 0, 1)]

style intro_ch1_caption is intro_ch1_text:
    color "#DFD2FF"
    size 32

init python:
    def intro_ch1_button_face(kind, state, width, height):
        return Transform(
            intro_ch1_ui + "button_{}_{}.png".format(kind, state),
            xysize=(width, height), fit="fill",
        )

screen intro_ch1_button(label, kind, on_click, width=300, height=76, enabled=True, chosen=False, icon=None):
    fixed:
        xysize (width, height)

        imagebutton:
            idle intro_ch1_button_face(kind, "idle", width, height)
            hover intro_ch1_button_face(kind, "hover", width, height)
            activate_child intro_ch1_button_face(kind, "pressed", width, height)
            insensitive intro_ch1_button_face(kind, "disabled", width, height)
            selected_idle intro_ch1_button_face(kind, "pressed", width, height)
            selected_hover intro_ch1_button_face(kind, "hover", width, height)
            focus_mask True
            action on_click
            sensitive enabled
            selected chosen
            alt label

        hbox:
            align (0.5, 0.48)
            spacing 10
            if icon:
                add intro_ch1_ui + icon + ".png" xysize (56, 56) yalign 0.5
            text label style "intro_ch1_text":
                size (38 if height >= 100 else 29)
                color ("#FAF7FF" if enabled else "#C4BDD3")
                yalign 0.5

screen intro_ch1_recorder(state, on_click, enabled=True, width=550):
    $ label = {"ready": "녹음 시작", "recording": "녹음 완료하기", "done": "녹음 완료"}[state]

    use intro_ch1_button(label, "recording" if state == "recording" else "record", on_click,
        width=width, height=118, enabled=enabled and state != "done", icon="icon_microphone")

    fixed:
        xysize (width, 118)
        add intro_ch1_ui + "icon_waveform.png":
            xysize (72, 24)
            xalign 0.92
            yalign 0.48
            alpha 0.66

screen intro_ch1_status(message, wide=False):
    fixed:
        xysize ((600, 62) if wide else (460, 56))
        add intro_ch1_ui + ("panel_hint.png" if wide else "panel_recorder_status.png"):
            xysize ((600, 62) if wide else (460, 56))
            fit "fill"
            alpha 0.84
        text message style "intro_ch1_text":
            align (0.5, 0.5)
            size 23
