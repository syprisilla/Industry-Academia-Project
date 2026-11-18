# ==================================================
# 메아리 괴물 이미지
# ==================================================

image ui_echo before = "images/characters/echo_before.png"
image ui_echo talk = "images/characters/echo_talk.png"
image ui_echo angry = "images/characters/echo_angry.png"
image ui_echo hit1 = "images/characters/echo_surprised.png"
image ui_echo hit2 = "images/characters/echo_hit2.png"
image ui_echo hit3 = "images/characters/echo_hit3.png"
image ui_echo after = "images/characters/echo_after.png"

default echo_success_count = 0
default ui_selected_training_word = None


# ==================================================
# 메아리 괴물 크기와 위치
# 공격 효과가 도착하는 위치에 맞춤
# ==================================================

transform ui_echo_position:
    xysize (680, 454)
    fit "contain"
    anchor (0.5, 0.5)
    pos (1435, 536)

    zoom 1.0
    alpha 1.0
    xoffset 0
    yoffset 0


transform ui_echo_after_position:
    xysize (680, 454)
    fit "contain"
    anchor (0.5, 0.5)
    pos (1435, 536)

    zoom 1.0
    alpha 1.0
    xoffset 0
    yoffset 0


# ==================================================
# 메아리 괴물 HP
# ==================================================

screen ui_echo_hp():

    zorder 10

    fixed:
        xysize (328, 157)
        xpos 1538
        ypos 124

        add intro_ch1_ui + "panel_hp.png":
            xysize (328, 157)
            fit "fill"
            alpha 0.88

        vbox:
            xpos 28
            ypos 15
            spacing 4

            text "Echo Monster":
                style "intro_ch1_text"
                size 28

            text "HP Left: [3 - echo_success_count] / 3":
                style "intro_ch1_caption"
                size 23

            hbox:
                spacing 4

                for segment in range(3):

                    if segment < 3 - echo_success_count:
                        add intro_ch1_ui + "hp_segment_full.png":
                            xysize (86, 24)
                            fit "fill"
                    else:
                        add intro_ch1_ui + "hp_segment_empty.png":
                            xysize (86, 24)
                            fit "fill"


# ==================================================
# 공격 성공: 기존 먼지 괴물의 음파 효과 재사용
# ==================================================

label ui_echo_light_attack:

    $ play_scene_sound(scene_wave_sound)

    show dust_wave_launch at ui_dust_wave_launch
    pause 0.12

    show dust_wave_flight at ui_dust_wave_flight
    show dust_wave_sparkles at ui_dust_wave_glint
    pause 0.7

    hide dust_wave_launch
    hide dust_wave_flight
    hide dust_wave_sparkles

    # 공격 명중 시 성공 횟수 증가
    $ echo_success_count += 1

    # 첫 피격 → 두 번째 피격 → 정화 중
    if echo_success_count == 1:
        show ui_echo hit1 at ui_echo_position, ui_dust_hit

    elif echo_success_count == 2:
        show ui_echo hit2 at ui_echo_position, ui_dust_hit

    else:
        show ui_echo hit3 at ui_echo_position, ui_dust_hit

    show dust_wave_impact at ui_dust_wave_center, ui_dust_wave_expand(410, 0.42, 1.22)
    show dust_wave_sparkles at ui_dust_wave_center, ui_dust_wave_expand(450, 0.44, 1.25)

    pause 0.3

    # 흔들림을 끝내고 현재 피격 모습으로 떠다니기
    if echo_success_count == 1:
        show ui_echo hit1 at ui_echo_position, ui_dust_idle

    elif echo_success_count == 2:
        show ui_echo hit2 at ui_echo_position, ui_dust_idle

    else:
        show ui_echo hit3 at ui_echo_position, ui_dust_idle

    pause 0.25

    hide dust_wave_impact
    hide dust_wave_sparkles

    return


# ==================================================
# 정화 연출
# ==================================================

label ui_echo_purification:

    show ui_echo hit3 at ui_echo_position, ui_dust_idle

    show dust_wave_purify_ring at ui_dust_wave_center, ui_dust_wave_expand(530, 0.85, 1.28, 1.0, 30)
    pause 0.5

    show dust_wave_purify_burst at ui_dust_wave_center, ui_dust_wave_expand(560, 0.72, 1.35)
    pause 0.2

    show ui_echo after at ui_echo_after_position, ui_dust_idle with Dissolve(0.5)

    pause 0.3

    hide dust_wave_purify_ring
    hide dust_wave_purify_burst

    return


# ==================================================
# 메아리 괴물 전투
# 기존 먼지 괴물의 단어·녹음 화면을 그대로 사용
# ==================================================

label ch1_m2_battle:

    $ echo_success_count = 0

    # 현재 먼지 괴물 전투와 같은 임시 핵심단어
    $ ui_echo_core_word = ui_selected_core_word or "사과"
    $ ui_echo_training_word = ui_selected_training_word or "가수"


    show ui_echo before at ui_echo_position, ui_dust_idle
    show screen ui_echo_hp

    while echo_success_count < 3:

        window hide

        $ play_scene_music(scene_battle_music, volume=scene_battle_volume)

        # 핵심단어 화면
        call screen ui_dust_word(ui_echo_core_word)

        # 훈련단어 녹음 화면
        call screen ui_dust_word(ui_echo_training_word, training=True)
        $ ui_echo_result = _return

        $ play_scene_music(scene_battle_music, volume=scene_battle_volume)

        if ui_echo_result == "success":

            call ui_echo_light_attack

            window auto

            if echo_success_count == 1:
                call ch1_m2_success_1

            elif echo_success_count == 2:
                call ch1_m2_success_2

            else:
                call ch1_m2_success_3

        elif ui_echo_result == "fail":

            # 실패해도 HP와 현재 피격 모습 유지
            window auto

            show ui_ghost intro_encourage with Dissolve(0.2)
            ghost "That's okay! Let's try the word again slowly."
            show ui_ghost intro_idle with Dissolve(0.2)

        else:

            # 인식 불가 안내 후 다시 시도
            window auto

            show ui_ghost intro_curious with Dissolve(0.2)
            ghost "I couldn't hear that clearly. Let's check the microphone."

            show ui_ghost intro_idle at ui_ghost_corridor

            window hide None
            call screen ui_unrecognized(ui_unrec_kind)
            window auto

            show ui_ghost intro_idle at ui_ghost_corridor, ghost_float

    hide screen ui_echo_hp

    window auto

    jump ch1_m2_clear