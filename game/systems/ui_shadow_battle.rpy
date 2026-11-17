# ==================================================
# 그림자 괴물 이미지
# ==================================================

image ui_shadow before = "images/characters/shadow_before.png"
image ui_shadow talk = "images/characters/shadow_talk.png"
image ui_shadow angry = "images/characters/shadow_angry.png"
image ui_shadow hit1 = "images/characters/shadow_surprised.png"
image ui_shadow hit2 = "images/characters/shadow_hit2.png"
image ui_shadow hit3 = "images/characters/shadow_hit3.png"
image ui_shadow after = "images/characters/shadow_after.png"

default shadow_success_count = 0


# ==================================================
# 위치와 크기
# 메아리보다 크게 표시
# ==================================================

transform ui_shadow_position:
    xysize (700, 700)
    fit "contain"
    anchor (0.5, 0.5)
    pos (1435, 536)

    zoom 1.0
    alpha 1.0
    xoffset 0
    yoffset 0


transform ui_shadow_after_position:
    xysize (420, 420)
    fit "contain"
    anchor (0.5, 0.5)
    pos (1350, 580)

    zoom 1.0
    alpha 1.0
    xoffset 0
    yoffset 0


# 바닥의 그림자에서 솟아오르는 연출
transform ui_shadow_emerge:
    subpixel True
    alpha 0.0
    zoom 0.65
    yoffset 100

    easeout 0.8 alpha 1.0 zoom 1.0 yoffset 0

    ui_dust_idle


# ==================================================
# 그림자 괴물 HP
# ==================================================

screen ui_shadow_hp():

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

            text "Shadow Monster":
                style "intro_ch1_text"
                size 28

            text "HP Left: [3 - shadow_success_count] / 3":
                style "intro_ch1_caption"
                size 23

            hbox:
                spacing 4

                for segment in range(3):

                    if segment < 3 - shadow_success_count:
                        add intro_ch1_ui + "hp_segment_full.png":
                            xysize (86, 24)
                            fit "fill"

                    else:
                        add intro_ch1_ui + "hp_segment_empty.png":
                            xysize (86, 24)
                            fit "fill"


# ==================================================
# 공격과 피격
# ==================================================

label ui_shadow_light_attack:

    $ play_scene_sound(scene_wave_sound)

    show dust_wave_launch at ui_dust_wave_launch
    pause 0.12

    show dust_wave_flight at ui_dust_wave_flight
    show dust_wave_sparkles at ui_dust_wave_glint
    pause 0.7

    hide dust_wave_launch
    hide dust_wave_flight
    hide dust_wave_sparkles

    $ shadow_success_count += 1

    $ shadow_hit_pose = (
        "ui_shadow hit1",
        "ui_shadow hit2",
        "ui_shadow hit3"
    )[shadow_success_count - 1]

    show expression shadow_hit_pose as ui_shadow at ui_shadow_position, ui_dust_hit

    show dust_wave_impact at ui_dust_wave_center, ui_dust_wave_expand(460, 0.42, 1.22)
    show dust_wave_sparkles at ui_dust_wave_center, ui_dust_wave_expand(500, 0.44, 1.25)

    pause 0.3

    show expression shadow_hit_pose as ui_shadow at ui_shadow_position, ui_dust_idle

    pause 0.25

    hide dust_wave_impact
    hide dust_wave_sparkles

    return


# ==================================================
# 정화 중 → 정화 완료
# ==================================================

label ui_shadow_purification:

    show ui_shadow hit3 at ui_shadow_position, ui_dust_idle

    show dust_wave_purify_ring at ui_dust_wave_center, ui_dust_wave_expand(600, 0.85, 1.28, 1.0, 30)

    pause 0.5

    show dust_wave_purify_burst at ui_dust_wave_center, ui_dust_wave_expand(630, 0.72, 1.35)

    pause 0.2

    show ui_shadow after at ui_shadow_after_position, ui_dust_idle with Dissolve(0.6)

    pause 0.3

    hide dust_wave_purify_ring
    hide dust_wave_purify_burst

    return


# ==================================================
# 그림자 괴물 전투
# ==================================================

label ch1_m3_battle:

    $ shadow_success_count = 0

    # 기존 먼지·메아리 전투와 같은 임시 단어 설정
    $ ui_shadow_core_word = ui_selected_core_word or "사과"
    $ ui_shadow_training_word = ui_selected_training_word or "가수"


    show ui_shadow before at ui_shadow_position, ui_dust_idle
    show screen ui_shadow_hp

    while shadow_success_count < 3:

        window hide

        $ play_scene_music(scene_battle_music, volume=scene_battle_volume)

        # 기존 공통 단어·녹음 화면 재사용
        call screen ui_dust_word(ui_shadow_core_word)
        call screen ui_dust_word(ui_shadow_training_word, training=True)

        $ ui_shadow_result = _return

        $ play_scene_music(scene_battle_music, volume=scene_battle_volume)

        if ui_shadow_result == "success":

            call ui_shadow_light_attack

            window auto

            if shadow_success_count == 1:
                call ch1_m3_success_1

            elif shadow_success_count == 2:
                call ch1_m3_success_2

            else:
                call ch1_m3_success_3

        elif ui_shadow_result == "fail":

            # 실패해도 HP와 피격 모습 유지
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

    hide screen ui_shadow_hp

    window auto

    jump ch1_m3_clear