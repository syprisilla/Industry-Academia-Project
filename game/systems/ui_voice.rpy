# 발음 분석 결과창 (전투용) — 게이지 + 피드백
screen voice_result(data):
    modal True

    frame:
        xalign 0.5
        yalign 0.5
        xsize 900
        padding (40, 30)
        background Solid("#241D35EE")

        vbox:
            xalign 0.5
            spacing 24

            # 폴백(마찰음 약함)이 아닐 때만 게이지
            if not data.get("segment_estimated"):
                hbox:
                    xalign 0.5
                    spacing 20
                    for feat in ("cog_hz", "sd_hz"):
                        if feat in data["gauges"]:
                            add im.Image(data["gauges"][feat]):
                                xysize (380, 150)
                                fit "contain"

            text data["feedback"]:
                xalign 0.5
                size 32
                color "#FFFFFF"

            textbutton "확인":
                xalign 0.5
                action Return()