# The articulation guide has tabs for tongue position and mouth shape.
define ui_artic_dir = "images/articulation/"

define ui_artic_pages = [
    {
        "tab": "Tongue",
        "image": "s-articulation_guide.png",
        "title": "Tongue in. Air forward!",
        "steps": [
            "Part your front teeth slightly.",
            "Bring your tongue close to the gums\nbehind your top teeth. Leave a tiny gap.",
            "Blow air through the gap.\nTry making a 스으 sound.",
        ],
        "ghost": "Can you send the air forward like the blue arrow shows?",
    },
    {
        "tab": "Mouth",
        "image": "s-mouth_front.png",
        "title": "Relax your lips!",
        "steps": [
            "Relax your lips and stretch them\na little to the sides.",
            "Leave a little gap between your\ntop and bottom front teeth.",
            "Keep that shape and blow air.\nTry making a 스으 sound.",
        ],
        "ghost": "Part your front teeth like in the picture. Ready to say 스으 with me?",
    },
]


screen ui_articulation():

    modal True
    default page = 0
    $ p = ui_artic_pages[page]

    text "Practice the ㅅ Sound":
        style "intro_ch1_text"
        xpos 642
        ypos 95
        size 72
        bold True
        outlines [(3, "#0C1530", 0, 2)]

    # Tabs
    for i, t in enumerate(ui_artic_pages):
        button:
            xpos 642 + i * 242
            ypos 218
            xysize (226, 76)
            background Transform(intro_ch1_ui + "button_continue_disabled.png", xysize=(226, 76), fit="fill")
            selected_background Transform(intro_ch1_ui + "button_continue_idle.png", xysize=(226, 76), fit="fill")
            selected page == i
            action SetScreenVariable("page", i)

            text t["tab"]:
                style "intro_ch1_text"
                align (0.5, 0.5)
                size 38
                bold True
                color ("#FAF7FF" if page == i else "#C4BDD3")
                outlines []

    # Instruction card
    use ui_artic_card(p)

    # Little Ghost's dialogue
    window:
        style "window"

        window:
            style "namebox"
            text "Little Ghost" style "say_label" color "#B4DFFF"

        text p["ghost"] style "say_dialogue"

    fixed:
        xysize (240, 68)
        pos (1498, 890)
        # Next shows the Mouth tab first, so it isn't missed; on the last tab it closes the guide.
        use intro_ch1_button("Next", "continue",
            SetScreenVariable("page", page + 1) if page < len(ui_artic_pages) - 1 else Return(),
            width=240, height=68)


# The instruction card, shared with the pronunciation feedback screen.
screen ui_artic_card(p):

    fixed:
        xpos 598
        ypos 292
        xysize (1188, 488)

        add intro_ch1_ui + "panel_assessment.png" xysize (1188, 488) fit "fill" alpha 0.92
        # Use a light background so the diagram lines are visible.
        add ui_artic_dir + "panel_image.png" pos (59, 40)
        add ui_artic_dir + p["image"] pos (91, 40) xysize (408, 408) fit "contain"
        add Solid("#5A6AA0", xysize=(2, 352)) pos (548, 68)

        text p["title"]:
            style "intro_ch1_text"
            xpos 572
            ypos 88
            size 46
            bold True
            color "#FFF2C7"
            text_align 0.0
            outlines []

        for n, step in enumerate(p["steps"]):
            text (str(n + 1) + "."):
                style "intro_ch1_text"
                xpos 572
                ypos 183 + n * 85
                size 31
                color "#9FB4FF"
                outlines []
            text step:
                style "intro_ch1_text"
                xpos 614
                ypos 183 + n * 85
                size 31
                color "#F8F5FF"
                text_align 0.0
                outlines []


label ch1_articulation_guide:

    window hide

    # Hide the Dust Monster temporarily to keep the guide visible.
    hide ui_dust with Dissolve(0.2)
    show ui_ghost intro_explain with Dissolve(0.2)

    call screen ui_articulation

    show ui_dust before at ui_dust_corridor with Dissolve(0.2)
    show ui_ghost intro_talk_closed with Dissolve(0.2)

    window auto

    return
