# ==========================================
# 가시덩굴 괴물 이미지
# ==========================================

image ui_vine before = "images/characters/thorny_vine_before.png"
image ui_vine talk = "images/characters/thorny_vine_talk.png"
image ui_vine angry = "images/characters/thorny_vine_angry.png"

image ui_vine hit1 = "images/characters/thorny_vine_surprised.png"
image ui_vine hit2 = "images/characters/thorny_vine_hit2.png"
image ui_vine hit3 = "images/characters/thorny_vine_hit3.png"

image ui_vine after = "images/characters/thorny_vine_after.png"
image ui_vine after_worried = "images/characters/thorny_vine_after_worried.png"


# ==========================================
# 크기와 위치
# ==========================================

transform ui_vine_position:
    xysize (440, 440)
    fit "contain"
    anchor (0.5, 0.5)
    pos (1435, 550)

    zoom 1.0
    alpha 1.0
    xoffset 0
    yoffset 0


transform ui_vine_effect_center:
    anchor (0.5, 0.5)
    pos (1435, 550)


transform ui_vine_wave_flight:
    subpixel True
    xysize (380, 220)
    fit "contain"
    anchor (0.5, 0.5)
    pos (0.25, 0.50)
    alpha 0.0

    parallel:
        linear 0.08 alpha 1.0

    parallel:
        easein 0.7 pos (1435, 550)


transform ui_vine_wave_glint:
    subpixel True
    xysize (105, 105)
    fit "contain"
    anchor (0.5, 0.5)
    pos (0.30, 0.46)
    alpha 0.0

    parallel:
        pause 0.13
        linear 0.12 alpha 0.7
        linear 0.35 alpha 0.0

    parallel:
        easein 0.7 pos (1350, 515)


# ==========================================
# HP 패널
# ==========================================

screen ui_vine_hp():
    use ui_dust_hp("Thorny Vine Monster")


# ==========================================
# 공통 발음 전투 연결
# ==========================================

label ch3_m2_battle:

    call pronunciation_battle(
        "ch3_m2",
        "Thorny Vine Monster",
        scene_battle_music,
        "vine",
        ui_vine_position
    ) from ch3_m2_pronunciation_battle_done

    jump ch3_m2_clear


# ==========================================
# 공격 성공 연출
# 성공 횟수는 여기에서 한 번만 증가
# ==========================================

label ui_vine_light_attack:

    window hide

    $ play_scene_sound(scene_wave_sound)

    show dust_wave_launch at ui_dust_wave_launch
    pause 0.12

    show dust_wave_flight at ui_vine_wave_flight
    show dust_wave_sparkles at ui_vine_wave_glint
    pause 0.7

    hide dust_wave_launch
    hide dust_wave_flight
    hide dust_wave_sparkles

    $ success_count += 1

    if success_count == 1:
        show ui_vine hit1 at ui_vine_position, ui_dust_hit
    elif success_count == 2:
        show ui_vine hit2 at ui_vine_position, ui_dust_hit
    else:
        show ui_vine hit3 at ui_vine_position, ui_dust_hit

    show dust_wave_impact at ui_vine_effect_center, ui_dust_wave_expand(460, 0.42, 1.22)
    show dust_wave_sparkles at ui_vine_effect_center, ui_dust_wave_expand(500, 0.44, 1.25)

    pause 0.3

    if success_count == 1:
        show ui_vine hit1 at ui_vine_position, ui_dust_idle
    elif success_count == 2:
        show ui_vine hit2 at ui_vine_position, ui_dust_idle
    else:
        show ui_vine hit3 at ui_vine_position, ui_dust_idle

    pause 0.3

    hide dust_wave_impact
    hide dust_wave_sparkles

    return


# ==========================================
# 정화 연출
# 꽃이 피어난 모습으로 변경
# ==========================================

label ui_vine_purification:

    window hide

    show ui_vine hit3 at ui_vine_position, ui_dust_idle

    show dust_wave_purify_ring at ui_vine_effect_center, ui_dust_wave_expand(540, 0.85, 1.28, 1.0, 30)
    pause 0.5

    show dust_wave_purify_burst at ui_vine_effect_center, ui_dust_wave_expand(570, 0.72, 1.35)
    pause 0.2

    show ui_vine after at ui_vine_position, ui_dust_idle with Dissolve(0.5)
    pause 0.3

    hide dust_wave_purify_ring
    hide dust_wave_purify_burst

    window auto

    return