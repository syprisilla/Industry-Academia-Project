# 조음 안내: 혀 위치와 입 모양을 탭으로 보여준다.
define ui_artic_dir = "images/articulation/"

define ui_artic_pages = [
    {
        "tab": "혀 위치",
        "image": "s-articulation_guide.png",
        "title": "혀 끝은 입 안에, 바람은 앞으로!",
        "steps": [
            "앞니 사이를 살짝 벌려요.",
            "혀 앞부분을 윗니 뒤 잇몸 가까이\n가져가요. 작은 틈을 남겨요.",
            "그 틈으로 바람을 내보내며\n“스으—” 소리를 내 봐요.",
        ],
        "ghost": "파란 화살표를 따라 바람을 앞으로 보내 볼까?",
    },
    {
        "tab": "입 모양",
        "image": "s-mouth_front.png",
        "title": "입술은 편하게, 앞니는 살짝!",
        "steps": [
            "입술에 힘을 빼고 양옆으로 살짝 펴요.",
            "위아래 앞니 사이에 작은 틈을 만들어요.",
            "그 모양으로 바람을 내보내며\n“스으—” 소리를 내 봐요.",
        ],
        "ghost": "그림처럼 앞니를 살짝 벌리고, 나랑 같이 ‘스으—’ 해 볼까?",
    },
]


screen ui_articulation():

    modal True
    default page = 0
    $ p = ui_artic_pages[page]
    $ img = ui_artic_dir + p["image"]

    text "ㅅ 발음 연습":
        style "intro_ch1_text"
        xpos 642
        ypos 95
        size 72
        bold True
        outlines [(3, "#0C1530", 0, 2)]

    # 탭
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

    # 안내 카드
    fixed:
        xpos 598
        ypos 292
        xysize (1188, 488)

        add intro_ch1_ui + "panel_assessment.png" xysize (1188, 488) fit "fill" alpha 0.92
        # 그림은 밝은 바탕 위에 올려야 선이 보인다.
        add ui_artic_dir + "panel_image.png" pos (59, 40)
        add img pos (91, 40) xysize (408, 408) fit "contain"
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

    # 작은 유령 말풍선
    window:
        style "window"

        window:
            style "namebox"
            text "작은 유령" style "say_label" color "#B4DFFF"

        text p["ghost"] style "say_dialogue"

    fixed:
        xysize (240, 68)
        pos (1498, 890)
        use intro_ch1_button("준비하기", "continue", Return(), width=240, height=68)


label ch1_articulation_guide:

    window hide

    # 화면이 가려지지 않도록 먼지 괴물을 잠시 숨긴다.
    hide ui_dust with Dissolve(0.2)
    show ui_ghost intro_explain with Dissolve(0.2)

    call screen ui_articulation

    show ui_dust before at ui_dust_corridor with Dissolve(0.2)
    show ui_ghost intro_talk_closed with Dissolve(0.2)

    window auto

    return
