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

    fixed:
        xysize (328, 157)
        xpos 1538
        ypos 124

        add intro_ch1_ui + "panel_hp.png" xysize (328, 157) fit "fill" alpha 0.88

        vbox:
            xpos 28
            ypos 15
            spacing 4

            text "먼지 괴물" style "intro_ch1_text" size 28
            text "남은 HP: [3 - success_count] / 3" style "intro_ch1_caption" size 23

            hbox:
                spacing 4
                for segment in range(3):
                    add intro_ch1_ui + ("hp_segment_full.png" if segment < 3 - success_count else "hp_segment_empty.png"):
                        xysize (86, 24)
                        fit "fill"


screen ui_dust_word(word, training=False):

    modal True
    default ui_record_state = "ready"
    default ui_voice = {"result": None, "feedback": "", "gauges": {}}

    fixed:
        xysize (1140, 252)
        xpos 342
        ypos 116

        add intro_ch1_ui + ("panel_training_word.png" if training else "panel_core_word.png"):
            xysize (1140, 252)
            fit "fill"
            alpha 0.84

        text ("훈련단어를 말해서 공격해 보자!" if training else "먼저 핵심단어로 목소리를 준비해 보자!"):
            style "intro_ch1_caption"
            xalign 0.5
            ypos 29
            size 34

        fixed:
            xysize (300, 116)
            align (0.5, 0.76)
            if training:

                add intro_ch1_ui + "panel_word_focus.png" xysize (300, 116) fit "fill"
            text word style "intro_ch1_text" align (0.5, 0.5) size 70 bold True


    if training:

        if ui_record_state == "result" and ui_voice["result"] == "unrecognized":

            # 인식 불가는 결과 패널 없이 바로 안내 화면으로 넘어간다.
            timer 0.01 action Return("unrecognized")

        elif ui_record_state == "result":

            # 녹음 결과: 게이지(폴백 아니면) + 피드백 + 확인
            fixed:
                xysize (900, 400)
                xalign 0.5
                ypos 500

                vbox:
                    xalign 0.5
                    spacing 20

                    if not ui_voice.get("segment_estimated"):
                        hbox:
                            xalign 0.5
                            spacing 20
                            for feat in ("cog_hz", "sd_hz"):
                                if feat in ui_voice["gauges"]:
                                    add im.Image(ui_voice["gauges"][feat]):
                                        xysize (360, 142)
                                        fit "contain"

                    text ui_voice["feedback"]:
                        xalign 0.5
                        size 30
                        color "#FFFFFF"
                        outlines [(2, "#241D35", 0, 0)]

                    use intro_ch1_button("확인", "continue", Return(ui_voice["result"]),
                        width=200, height=70)

        else:

            # 녹음 버튼 (ready/recording)
            fixed:
                xysize (500, 118)
                xalign 0.5
                ypos 535
                use intro_ch1_recorder(ui_record_state, Function(do_record, word),
                    enabled=True, width=500)

            fixed:
                xysize (460, 56)
                xalign 0.5
                ypos 674
                use intro_ch1_status("개발용 테스트 (실제 녹음 및 발음 판정 아님)")

            hbox:
                xalign 0.5
                ypos 758
                spacing 12
                use intro_ch1_button("다음", "next", None, width=140, height=60, enabled=False)
                use intro_ch1_button("성공", "success", Return("success"), width=140, height=60)
                use intro_ch1_button("실패", "fail", Return("fail"), width=140, height=60)
                use intro_ch1_button("인식 불가", "unrecognized", [Function(ui_unrec_next_test), Return("unrecognized")], width=160, height=60)

    else:
        fixed:
            xysize (420, 84)
            xalign 0.5
            ypos 533
            use intro_ch1_button("훈련단어로 넘어가기", "continue", Return(),
                width=420, height=84, icon="icon_next")




# 성공 횟수는 음파가 명중한 순간 한 번만 갱신한다.
label ui_dust_light_attack:
    $ play_scene_sound(scene_wave_sound)
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
