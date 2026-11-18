# ==================================================
# 시계 괴물 이미지
# ==================================================

image ui_clock normal = "images/characters/clock.png"
image ui_clock before = "images/characters/clock_before.png"
image ui_clock talk = "images/characters/clock_talk.png"
image ui_clock angry = "images/characters/clock_angry.png"

image ui_clock hit1 = "images/characters/clock_surprised.png"
image ui_clock hit2 = "images/characters/clock_hit2.png"
image ui_clock hit3 = "images/characters/clock_hit3.png"

image ui_clock after = "images/characters/clock_after.png"


# ==================================================
# 새 배경 등록
# 기존 apartment 배경과 같은 태그 사용
# ==================================================

image apartment corridor_clock = apartment_background(
    "images/backgrounds/apartment_corridor_clock.png"
)

image apartment elevator_on_3 = apartment_background(
    "images/backgrounds/apartment_elevator_on_3.png"
)


# ==================================================
# 변신 전: 문에 붙어 있는 시계
# 떠다니는 동작을 적용하지 않음
# ==================================================

transform ui_clock_wall_position:
    xysize (440, 520)
    fit "contain"
    anchor (0.5, 0.5)
    pos (1380, 340)

    zoom 1.0
    alpha 1.0
    xoffset 0
    yoffset 0


# ==================================================
# 전투 위치
# 위쪽 단어 패널에 가리지 않도록 배치
# 정화 후에도 같은 크기 유지
# ==================================================

transform ui_clock_position:
    xysize (500, 500)
    fit "contain"
    anchor (0.5, 0.5)
    pos (1435, 610)

    zoom 1.0
    alpha 1.0
    xoffset 0
    yoffset 0


# 문에서 앞으로 나오며 괴물로 변신
transform ui_clock_transform:
    subpixel True

    xysize (440, 520)
    fit "contain"
    anchor (0.5, 0.5)
    pos (1380, 420)

    alpha 0.0
    zoom 0.9
    xoffset 0
    yoffset 0

    easeout 0.65 alpha 1.0 xysize (500, 500) pos (1435, 610) zoom 1.0

    ui_dust_idle


# 정화 후 옆으로 비켜주기
transform ui_clock_move_aside:
    subpixel True

    ease 0.6 xpos 1615

    block:
        ease 1.25 yoffset -12
        ease 1.25 yoffset 0
        repeat


# ==================================================
# 시계 위치에 맞춘 공격 효과
# ==================================================

transform ui_clock_effect_center:
    subpixel True
    anchor (0.5, 0.5)
    pos (1435, 610)


transform ui_clock_wave_flight:
    subpixel True
    anchor (0.5, 0.5)
    pos (0.25, 0.50)

    xysize (380, 220)
    fit "contain"
    alpha 0.0

    parallel:
        linear 0.08 alpha 1.0

    parallel:
        easein 0.7 pos (1435, 610)


transform ui_clock_wave_glint:
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
        easein 0.7 pos (1350, 575)


# ==================================================
# HP
# 기존 공통 HP 화면 재사용
# ==================================================

screen ui_clock_hp():
    use ui_dust_hp("Clock Monster")


# ==================================================
# 시계 괴물 전투
# 단어 선택·녹음·발음 판정은 기존 공통 전투 사용
# ==================================================

label ch2_m3_battle:

    call pronunciation_battle(
        "ch2_m3",
        "Clock Monster",
        scene_battle_music,
        "clock",
        ui_clock_position
    ) from ch2_m3_pronunciation_battle_done

    jump ch2_m3_clear


# ==================================================
# 공격 성공
# ==================================================

label ui_clock_light_attack:

    window hide

    $ play_scene_sound(scene_wave_sound)

    show dust_wave_launch at ui_dust_wave_launch
    pause 0.12

    show dust_wave_flight at ui_clock_wave_flight
    show dust_wave_sparkles at ui_clock_wave_glint
    pause 0.7

    hide dust_wave_launch
    hide dust_wave_flight
    hide dust_wave_sparkles

    # 명중했을 때 한 번만 증가
    $ success_count += 1

    if success_count == 1:
        show ui_clock hit1 at ui_clock_position, ui_dust_hit

    elif success_count == 2:
        show ui_clock hit2 at ui_clock_position, ui_dust_hit

    else:
        show ui_clock hit3 at ui_clock_position, ui_dust_hit

    show dust_wave_impact at ui_clock_effect_center, ui_dust_wave_expand(460, 0.42, 1.22)
    show dust_wave_sparkles at ui_clock_effect_center, ui_dust_wave_expand(500, 0.44, 1.25)

    pause 0.3

    if success_count == 1:
        show ui_clock hit1 at ui_clock_position, ui_dust_idle

    elif success_count == 2:
        show ui_clock hit2 at ui_clock_position, ui_dust_idle

    else:
        show ui_clock hit3 at ui_clock_position, ui_dust_idle

    pause 0.25

    hide dust_wave_impact
    hide dust_wave_sparkles

    return


# ==================================================
# 정화
# 다른 괴물과 동일한 정화 효과 사용
# ==================================================

label ui_clock_purification:

    window hide

    show ui_clock hit3 at ui_clock_position, ui_dust_idle

    show dust_wave_purify_ring at ui_clock_effect_center, ui_dust_wave_expand(560, 0.85, 1.28, 1.0, 30)
    pause 0.5

    show dust_wave_purify_burst at ui_clock_effect_center, ui_dust_wave_expand(590, 0.72, 1.35)
    pause 0.2

    show ui_clock after at ui_clock_position, ui_dust_idle with Dissolve(0.5)

    pause 0.3

    hide dust_wave_purify_ring
    hide dust_wave_purify_burst

    window auto

    return