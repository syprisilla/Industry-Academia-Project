# Feedback after a failed practice word: gauges first, then the shared tongue guide.
define ui_feedback_cards = [("cog_hz", "Center of gravity (CoG)"), ("sd_hz", "Spread")]

# Set by pronunciation_battle; the default only covers screens shown outside a battle.
default hp_screen = "ui_dust_hp"

init python:
    def ui_feedback_show_hp(monster_name):
        """Bring back the monster HP screen hidden by the feedback screen."""
        # Only ui_dust_hp takes the monster name; the other HP screens take no arguments.
        if hp_screen == "ui_dust_hp":
            renpy.show_screen(hp_screen, monster_name)
        else:
            renpy.show_screen(hp_screen)

    def ui_feedback_image(tag, fallback):
        """Return the image now shown for tag (e.g. "apartment corridor_1"), or the fallback."""
        attrs = renpy.get_attributes(tag)
        return " ".join((tag,) + tuple(attrs)) if attrs else fallback


screen ui_pronunciation_feedback(data, done):

    # Weak frication has no reliable gauges, so it goes straight to the tongue guide.
    default step = "guide" if data.get("segment_estimated") else "result"

    # The HP screen sits above this one (zorder 10), so hide it while feedback is open.
    timer 0.01 action Hide(hp_screen)

    # Redraw the background and Little Ghost on top so the monster behind is covered.
    add ui_feedback_image("apartment", "apartment corridor_1")
    add ui_feedback_image("ui_ghost", "ui_ghost intro_idle") at ui_ghost_corridor, ui_ghost_idle

    text "Pronunciation Feedback":
        style "intro_ch1_text"
        xpos 642
        ypos 125
        size 72
        bold True
        outlines [(3, "#0C1530", 0, 2)]

    if step == "result":

        fixed:
            xpos 598
            ypos 292
            xysize (1188, 488)

            add intro_ch1_ui + "panel_assessment.png" xysize (1188, 488) fit "fill" alpha 0.92

            text "Let's practice once more":
                style "intro_ch1_text"
                xalign 0.5
                ypos 46
                size 46
                bold True
                color "#FFF2C7"
                outlines []

            hbox:
                xalign 0.5
                ypos 132
                spacing 30

                for feat, label in ui_feedback_cards:
                    fixed:
                        xysize (520, 300)
                        add Frame(intro_ch1_ui + "panel_hint.png", 30, 30) xysize (520, 300)
                        text label:
                            style "intro_ch1_text"
                            xpos 48
                            ypos 26
                            size 32
                            bold True
                            text_align 0.0
                            outlines []
                        add Solid("#5A6AA0", xysize=(424, 2)) pos (48, 80)
                        if feat in data["gauges"]:
                            add im.Image(data["gauges"][feat]) pos (10, 92) xysize (500, 197) fit "contain"

        $ ghost_line = data["feedback"]
        # SetLocalVariable: this screen is included with "use", so SetScreenVariable would miss "step".
        $ button = ("Next", SetLocalVariable("step", "guide"))

    else:

        use ui_artic_card(ui_artic_pages[0])

        # Weak frication keeps the engine's line so the child knows why the guide appeared.
        $ ghost_line = data["feedback"] if data.get("segment_estimated") else ui_artic_pages[0]["ghost"]
        $ button = ("Try Again", done)

    # Little Ghost's dialogue
    window:
        style "window"

        window:
            style "namebox"
            text "Little Ghost" style "say_label" color "#B4DFFF"

        text ghost_line style "say_dialogue"

    fixed:
        xysize (240, 68)
        pos (1498, 890)
        use intro_ch1_button(button[0], "continue", button[1], width=240, height=68)
