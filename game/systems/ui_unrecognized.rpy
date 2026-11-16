# Show guidance for quiet recordings, loud recordings, or a missing mic.
define ui_unrec_info = {
    "quiet": {
        "title": "Your voice was too quiet",
        "head": "Try speaking closer to the mic!",
        "tips": [
            "Move your face a little closer to the mic.",
            "Find a quiet spot with less noise.",
            "Speak clearly and a little louder.",
        ],
    },
    "loud": {
        "title": "Your voice was too loud",
        "head": "Move a little farther from the mic!",
        "tips": [
            "Move one hand span away from the mic.",
            "Speak in your usual voice.",
            "When ready, say the same word again.",
        ],
    },
    "mic": {
        "title": "Check your microphone",
        "head": "Make sure your mic is on!",
        "tips": [
            "Make sure your mic is connected.",
            "Unmute the mic and allow mic access\nin your device settings.",
            "Once it's ready, say the same word again.",
        ],
    },
}

# Map word.json reason or status to help text. Unknown codes use "quiet".
define ui_unrec_kind_of = {"too_quiet": "quiet", "clipping": "loud", "no_device": "mic"}

default ui_unrec_kind = "quiet"

init python:
    def ui_unrec_set_kind(code):
        store.ui_unrec_kind = ui_unrec_kind_of.get(code, "quiet")

    def ui_unrec_next_test():
        # Cycle through the help screens when the test button is pressed.
        kinds = ["quiet", "loud", "mic"]
        store.ui_unrec_kind = kinds[(kinds.index(store.ui_unrec_kind) + 1) % 3]


screen ui_unrecognized(kind):

    modal True
    $ info = ui_unrec_info[kind]

    # Dim the background to draw attention to the instructions.
    add Solid("#10152F88")

    text info["title"]:
        style "intro_ch1_text"
        xpos 893
        ypos 270
        anchor (0.5, 0.5)
        size 52
        bold True
        outlines [(3, "#0C1530", 0, 2)]

    # Instruction card
    fixed:
        xpos 512
        ypos 338
        xysize (760, 392)

        add intro_ch1_ui + "panel_assessment.png" xysize (760, 392) fit "fill" alpha 0.92
        add intro_ch1_ui + "icon_microphone.png" pos (102, 196) anchor (0.5, 0.5) xysize (130, 130) fit "contain"
        add Solid("#5A6AA0", xysize=(2, 275)) pos (177, 72)

        text info["head"]:
            style "intro_ch1_text"
            xpos 200
            ypos 62
            size 33
            bold True
            color "#FFF2C7"
            text_align 0.0
            outlines []

        # Move later tips down for each extra line in the preceding tips.
        $ y = 146
        for n, tip in enumerate(info["tips"]):
            text (str(n + 1) + "."):
                style "intro_ch1_text"
                xpos 200
                ypos y
                size 29
                color "#9FB4FF"
                outlines []
            text tip:
                style "intro_ch1_text"
                xpos 235
                ypos y
                size 29
                color "#F8F5FF"
                text_align 0.0
                outlines []
            $ y += 62 + 42 * tip.count("\n")

    fixed:
        xysize (240, 68)
        pos (1498, 890)
        use intro_ch1_button("Try Again", "continue", Return(), width=240, height=68)
