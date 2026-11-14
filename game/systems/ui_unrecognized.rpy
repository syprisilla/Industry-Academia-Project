# 인식 불가 안내: 원인(너무 작음/너무 큼/마이크 없음)에 따라 안내를 바꿔 보여준다.
define ui_unrec_info = {
    "quiet": {
        "title": "목소리가 잘 안 들렸어요",
        "head": "마이크 가까이에서 말해 봐요!",
        "tips": [
            "마이크 쪽으로 얼굴을 가까이 가져가요.",
            "주변 소리를 줄이고 조용한 곳에서\n말해요.",
            "또박또박 조금 더 크게 말해 봐요.",
        ],
    },
    "loud": {
        "title": "목소리가 너무 크게 들렸어요",
        "head": "마이크에서 조금 떨어져 말해 봐요!",
        "tips": [
            "마이크에서 한 뼘 정도 물러나요.",
            "평소에 이야기할 때처럼 편하게\n말해요.",
            "준비되면 같은 단어를 다시 말해요.",
        ],
    },
    "mic": {
        "title": "마이크 연결을 확인해 주세요",
        "head": "마이크가 켜져 있는지 확인해 봐요!",
        "tips": [
            "마이크가 기기에 연결되어 있는지 봐요.",
            "마이크가 음소거되어 있으면 풀고,\n게임의 마이크 사용을 허용해요.",
            "확인했으면 같은 단어를 다시 말해요.",
        ],
    },
}

# word.json 의 reason/status -> 안내 종류. 목록에 없는 원인은 "quiet" 로 처리한다.
define ui_unrec_kind_of = {"too_quiet": "quiet", "clipping": "loud", "no_device": "mic"}

default ui_unrec_kind = "quiet"

init python:
    def ui_unrec_set_kind(code):
        store.ui_unrec_kind = ui_unrec_kind_of.get(code, "quiet")

    def ui_unrec_next_test():
        # 개발용 버튼: 누를 때마다 안내 종류를 돌려 가며 보여준다.
        kinds = ["quiet", "loud", "mic"]
        store.ui_unrec_kind = kinds[(kinds.index(store.ui_unrec_kind) + 1) % 3]


screen ui_unrecognized(kind):

    modal True
    $ info = ui_unrec_info[kind]

    # 안내에 집중하도록 주변을 어둡게 한다.
    add Solid("#10152F88")

    text info["title"]:
        style "intro_ch1_text"
        xpos 893
        ypos 270
        anchor (0.5, 0.5)
        size 52
        bold True
        outlines [(3, "#0C1530", 0, 2)]

    # 안내 카드
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

        # 줄바꿈이 있는 안내는 다음 항목을 그만큼 아래로 민다.
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
        use intro_ch1_button("다시 말하기", "continue", Return(), width=240, height=68)
