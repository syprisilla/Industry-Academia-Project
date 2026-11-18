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

            text "HP Left: [3 - success_count] / 3":
                style "intro_ch1_caption"
                size 23

            hbox:
                spacing 4

                for segment in range(3):

                    if segment < 3 - success_count:
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

    $ success_count += 1

    $ shadow_hit_pose = (
        "ui_shadow hit1",
        "ui_shadow hit2",
        "ui_shadow hit3"
    )[success_count - 1]

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
    call pronunciation_battle("ch1_m3", "Shadow Monster", scene_battle_music, "shadow", ui_shadow_position,
        core_word=ui_selected_core_word or "사과", target_word=ui_selected_training_word or "가수") from ch1_m3_pronunciation_battle_done
    jump ch1_m3_clear
