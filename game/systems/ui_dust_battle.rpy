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


# 음파와 정화 효과는 복도에서 괴물의 몸 중심에 맞춘다.
image dust_wave_launch = "images/effects/dust_wave_launch.png"
image dust_wave_flight = "images/effects/dust_wave_flight.png"
image dust_wave_impact = "images/effects/dust_wave_impact.png"
image dust_wave_sparkles = "images/effects/dust_wave_sparkles.png"
image dust_wave_purify_ring = "images/effects/dust_wave_purify_ring.png"
image dust_wave_purify_burst = "images/effects/dust_wave_purify_burst.png"

transform ui_dust_wave_launch:
    subpixel True
    anchor (0.5, 0.5)
    pos (0.25, 0.50)
    xysize (180, 180)
    fit "contain"
    zoom 0.65
    alpha 0.0
    easeout 0.12 alpha 0.9 zoom 1.0
    linear 0.26 alpha 0.0 zoom 1.16

transform ui_dust_wave_flight:
    subpixel True
    anchor (0.5, 0.5)
    pos (0.25, 0.50)
    xysize (380, 220)
    fit "contain"
    alpha 0.0
    parallel:
        linear 0.08 alpha 1.0
    parallel:
        easein 0.7 pos (1435, 536)

transform ui_dust_wave_glint:
    subpixel True
    anchor (0.5, 0.5)
    pos (0.30, 0.46)
    xysize (105, 105)
    fit "contain"
    alpha 0.0
    parallel:
        pause 0.13
        linear 0.12 alpha 0.7
        linear 0.35 alpha 0.0
    parallel:
        easein 0.7 pos (1350, 501)

transform ui_dust_wave_center:
    subpixel True
    anchor (0.5, 0.5)
    pos (1435, 536)

transform ui_dust_wave_expand(size, duration, end_zoom, peak=1.0, turn=0):
    xysize (size, size)
    fit "contain"
    zoom 0.68
    alpha 0.0
    rotate 0
    easeout 0.1 alpha peak zoom 0.9
    easeout duration alpha 0.0 zoom end_zoom rotate turn

# 괴물 피격: 좌우로 짧게 흔들기
transform ui_dust_hit:
    subpixel True
    alpha 1.0
    zoom 1.0
    linear 0.05 xoffset 22 yoffset 0
    linear 0.05 xoffset -22
    linear 0.05 xoffset 16
    linear 0.05 xoffset -16
    linear 0.05 xoffset 8
    linear 0.05 xoffset 0


# 기존 저장에서 복원할 수 있는 이전 피격 후 트랜스폼.
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
                    action SetScreenVariable("ui_record_state", "recording")

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
            elif ui_record_state == "recording":
                # 녹음 중 메시지 + 타이머가 실제 녹음 실행
                text "🎙 녹음 중... 말하세요!":
                    xalign 0.5
                    size 36
                    color "#FFFFFF"
                    outlines [(2, "#241D35", 0, 0)]

                timer 0.05 action Function(do_record, word)

            else:

                # 폴백(마찰음 약함)이 아닐 때만 게이지 표시
                if not ui_voice.get("segment_estimated"):
                    hbox:
                        xalign 0.5
                        spacing 20
                        for feat in ("cog_hz", "sd_hz"):
                            if feat in ui_voice["gauges"]:
                                add im.Image(ui_voice["gauges"][feat]):
                                    xysize (380, 150)
                                    fit "contain"

                # 피드백 문구 (폴백이면 "ㅅ 소리를 내보자" 쪽이 옴)
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



# 성공 횟수는 음파가 명중한 순간 한 번만 갱신한다.
label ui_dust_light_attack:
    show dust_wave_launch at ui_dust_wave_launch
    pause 0.12
    show dust_wave_flight at ui_dust_wave_flight
    show dust_wave_sparkles at ui_dust_wave_glint
    pause 0.7

    hide dust_wave_launch
    hide dust_wave_flight
    hide dust_wave_sparkles

    $ success_count += 1
    $ dust_hit_pose = ("ui_dust hit1", "ui_dust hit2", "ui_dust hit3")[success_count - 1]
    show expression dust_hit_pose as ui_dust at ui_dust_corridor, ui_dust_hit
    show dust_wave_impact at ui_dust_wave_center, ui_dust_wave_expand(410, 0.42, 1.08 + 0.14 * success_count)
    show dust_wave_sparkles at ui_dust_wave_center, ui_dust_wave_expand(450, 0.44, 1.25, 0.45 + 0.17 * success_count)
    pause 0.3


    show expression dust_hit_pose as ui_dust at ui_dust_corridor, ui_dust_idle

    pause 0.25
    hide dust_wave_impact
    hide dust_wave_sparkles
    return


label ui_dust_purification:
    show dust_wave_purify_ring at ui_dust_wave_center, ui_dust_wave_expand(530, 0.85, 1.28, 1.0, 30)
    pause 0.32
    show dust_wave_purify_burst at ui_dust_wave_center, ui_dust_wave_expand(560, 0.72, 1.35)
    pause 0.15
    show ui_dust after at ui_dust_corridor, ui_dust_purified
    pause 0.69
    hide dust_wave_purify_ring
    hide dust_wave_purify_burst
    return
