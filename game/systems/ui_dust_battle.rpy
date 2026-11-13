# 빛 공격 이미지
image ui_light_attack = "images/effects/light_attack.png"

default success_count = 0


# 빛이 왼쪽에서 괴물 쪽으로 이동
transform ui_light_flight:
    xysize (360, 360)
    fit "contain"
    anchor (0.5, 0.5)
    pos (0.25, 0.50)
    alpha 0.0

    linear 0.15 alpha 1.0
    linear 0.8 xpos 0.78 ypos 0.48


# 괴물 피격: 좌우로 짧게 흔들기
transform ui_dust_hit:
    xoffset 0

    linear 0.05 xoffset 22
    linear 0.05 xoffset -22
    linear 0.05 xoffset 16
    linear 0.05 xoffset -16
    linear 0.05 xoffset 8
    linear 0.05 xoffset 0


# 피격 후 위치 복원
transform ui_dust_still:
    xoffset 0
    yoffset 0
    alpha 1.0


# 괴물 HP 표시
screen ui_dust_hp():

    zorder 10

    frame:
        xalign 0.95
        ypos 65
        xsize 360
        padding (24, 18)
        background Solid("#241D35DD")

        vbox:
            spacing 12

            text "먼지 괴물":
                size 30
                color "#FFFFFF"

            text "남은 HP: [3 - success_count] / 3":
                size 26
                color "#FFFFFF"

            bar:
                value StaticValue(3 - success_count, 3)
                xsize 312
                ysize 24
                left_bar Solid("#B89ADB")
                right_bar Solid("#44394F")
                thumb None


# 핵심단어 / 훈련단어 표시
screen ui_dust_word(word, training=False):

    modal True

    default ui_record_state = "ready"
    default ui_voice = {"result": None, "feedback": "", "gauges": {}}

    frame:
        xalign 0.22
        ypos 65
        xsize 1100
        padding (30, 20)
        background Solid("#FFF4DC")

        vbox:
            xalign 0.5
            spacing 10

            if training:
                text "훈련단어를 말해서 공격해 보자!":
                    xalign 0.5
                    size 30
                    color "#70558F"
            else:
                text "먼저 핵심단어로 목소리를 준비해 보자!":
                    xalign 0.5
                    size 30
                    color "#70558F"

            text word:
                xalign 0.5
                size 64
                color "#342743"

    vbox:
        xalign 0.5
        ypos 300
        spacing 18

        if training:

            if ui_record_state == "ready":

                # 녹음 시작 버튼 (voice_engine.exe 호출)
                button:
                    xalign 0.5
                    padding (24, 14)
                    background Solid("#62596F")
                    action Function(do_record, word)

                    hbox:
                        spacing 14
                        add "images/ui/mic.png":
                            xysize (48, 48)
                            fit "contain"
                            yalign 0.5
                        text "녹음 시작":
                            size 32
                            color "#DDDDDD"
                            yalign 0.5

                text "개발용 테스트 (실제 녹음 및 발음 판정 아님)":
                    xalign 0.5
                    size 24
                    color "#FFFFFF"
                    outlines [(2, "#241D35", 0, 0)]

                # 비상용 수동 버튼
                hbox:
                    xalign 0.5
                    spacing 20
                    textbutton "성공":
                        action Return("success")
                    textbutton "실패":
                        action Return("fail")
                    textbutton "인식 불가":
                        action Return("unrecognized")

            else:

                # 게이지 이미지 2장
                hbox:
                    xalign 0.5
                    spacing 20
                    for feat in ("cog_hz", "sd_hz"):
                        if feat in ui_voice["gauges"]:
                            add im.Image(ui_voice["gauges"][feat]):
                                xysize (380, 150)
                                fit "contain"

                # 피드백 문구
                text ui_voice["feedback"]:
                    xalign 0.5
                    size 30
                    color "#FFFFFF"
                    outlines [(2, "#241D35", 0, 0)]

                # 확인 -> 판정 결과를 battle_manager 로 반환
                textbutton "확인":
                    xalign 0.5
                    action Return(ui_voice["result"])

        else:

            # 핵심단어 화면 -> 훈련단어 화면으로
            textbutton "훈련단어로 넘어가기":
                xalign 0.5
                action Return()



# 성공했을 때 실행할 공격 연출
label ui_dust_light_attack:

    # 빛이 괴물에게 날아감
    show ui_light_attack at ui_light_flight
    pause 0.95

    # 현재 모습 그대로 흔들림
    show ui_dust at ui_dust_corridor, ui_dust_hit
    pause 0.3

    # success_count가 증가하기 전에 이미지 변경
    if success_count == 0:
        show ui_dust hit1 at ui_dust_corridor, ui_dust_still
    else:
        show ui_dust hit2 at ui_dust_corridor, ui_dust_still

    pause 0.25
    hide ui_light_attack with Dissolve(0.35)

    return