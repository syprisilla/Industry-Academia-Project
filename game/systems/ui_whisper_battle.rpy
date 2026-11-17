# ==================================================
# 속삭임 괴물: 이미지와 전투
# 기존 녹음 화면 및 빛 공격 효과 사용
# ==================================================

default whisper_success_count = 0

image ui_whisper before = "images/characters/whisper_before.png"
image ui_whisper talk = "images/characters/whisper_talk.png"
image ui_whisper angry = "images/characters/whisper_angry.png"
image ui_whisper hit1 = "images/characters/whisper_surprised.png"
image ui_whisper hit2 = "images/characters/whisper_hit2.png"
image ui_whisper hit3 = "images/characters/whisper_hit3.png"
image ui_whisper after = "images/characters/whisper_after.png"


# 정화 전 크기와 위치
transform ui_whisper_position:
    xysize (500, 500)
    fit "contain"
    anchor (0.5, 0.5)
    pos (1435, 536)

    zoom 1.0
    alpha 1.0
    xoffset 0
    yoffset 0


# 정화 후 크기와 위치
transform ui_whisper_after_position:
    xysize (500, 500)
    fit "contain"
    anchor (0.5, 0.5)
    pos (1350, 580)

    zoom 1.0
    alpha 1.0
    xoffset 0
    yoffset 0


# HP 표시
screen ui_whisper_hp():

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

            text "Whisper Monster":
                style "intro_ch1_text"
                size 28

            text "HP Left: [3 - whisper_success_count] / 3":
                style "intro_ch1_caption"
                size 23

            hbox:
                spacing 4

                for segment in range(3):
                    add intro_ch1_ui + (
                        "hp_segment_full.png"
                        if segment < 3 - whisper_success_count
                        else "hp_segment_empty.png"
                    ):
                        xysize (86, 24)
                        fit "fill"


# ==================================================
# 성공: 빛 공격과 피격 모습 변경
# ==================================================

label ui_whisper_light_attack:

    $ play_scene_sound(scene_wave_sound)

    show dust_wave_launch at ui_dust_wave_launch
    pause 0.12

    show dust_wave_flight at ui_dust_wave_flight
    show dust_wave_sparkles at ui_dust_wave_glint
    pause 0.7

    hide dust_wave_launch
    hide dust_wave_flight
    hide dust_wave_sparkles

    $ whisper_success_count += 1

    if whisper_success_count == 1:
        show ui_whisper hit1 at ui_whisper_position, ui_dust_hit

    elif whisper_success_count == 2:
        show ui_whisper hit2 at ui_whisper_position, ui_dust_hit

    else:
        show ui_whisper hit3 at ui_whisper_position, ui_dust_hit

    show dust_wave_impact at ui_dust_wave_center, ui_dust_wave_expand(460, 0.42, 1.22)
    show dust_wave_sparkles at ui_dust_wave_center, ui_dust_wave_expand(500, 0.44, 1.25)

    pause 0.3

    # 흔들림이 끝나면 현재 피격 모습을 유지
    if whisper_success_count == 1:
        show ui_whisper hit1 at ui_whisper_position, ui_dust_idle

    elif whisper_success_count == 2:
        show ui_whisper hit2 at ui_whisper_position, ui_dust_idle

    else:
        show ui_whisper hit3 at ui_whisper_position, ui_dust_idle

    pause 0.4

    hide dust_wave_impact
    hide dust_wave_sparkles

    return


# ==================================================
# 정화 중 → 정화 완료
# ==================================================

label ui_whisper_purification:

    show ui_whisper hit3 at ui_whisper_position, ui_dust_idle

    show dust_wave_purify_ring at ui_dust_wave_center, ui_dust_wave_expand(600, 0.85, 1.28, 1.0, 30)
    pause 0.5

    show dust_wave_purify_burst at ui_dust_wave_center, ui_dust_wave_expand(630, 0.72, 1.35)
    pause 0.3

    show ui_whisper after at ui_whisper_after_position, ui_dust_idle with Dissolve(0.6)

    pause 0.8

    hide dust_wave_purify_ring
    hide dust_wave_purify_burst

    return


# ==================================================
# 전투 진행
# ==================================================

label ch2_m1_battle:

    $ whisper_success_count = 0

    # 기존 전투의 단어 선택 방식 사용
    $ ui_whisper_core_word = ui_selected_core_word or "사과"
    $ ui_whisper_training_word = ui_selected_training_word or "가수"


    show ui_whisper before at ui_whisper_position, ui_dust_idle
    show screen ui_whisper_hp

    while whisper_success_count < 3:

        window hide

        $ play_scene_music(scene_battle_music, volume=scene_battle_volume)

        # 기존 공통 녹음 화면
        call screen ui_dust_word(ui_whisper_core_word)
        call screen ui_dust_word(ui_whisper_training_word, training=True)

        $ ui_whisper_result = _return

        $ play_scene_music(scene_battle_music, volume=scene_battle_volume)

        if ui_whisper_result == "success":

            call ui_whisper_light_attack

            window auto

            if whisper_success_count == 1:
                call ch2_m1_success_1

            elif whisper_success_count == 2:
                call ch2_m1_success_2

            else:
                call ch2_m1_success_3

        elif ui_whisper_result == "fail":

            window auto

            show ui_ghost intro_encourage with Dissolve(0.2)
            ghost "That's okay! Let's try the word again slowly."
            show ui_ghost intro_idle with Dissolve(0.2)

        else:

            window auto

            show ui_ghost intro_curious with Dissolve(0.2)
            ghost "I couldn't hear that clearly. Let's check the microphone."

            show ui_ghost intro_idle at ui_ghost_corridor

            window hide
            call screen ui_unrecognized(ui_unrec_kind)
            window auto

            show ui_ghost intro_idle at ui_ghost_corridor, ghost_float

    hide screen ui_whisper_hp

    window auto

    jump ch2_m1_clear