# ==================================================
# 편지 괴물 이미지
# ==================================================

image ui_letter before = "images/characters/letter_before.png"
image ui_letter talk = "images/characters/letter_talk.png"
image ui_letter angry = "images/characters/letter_angry.png"

image ui_letter hit1 = "images/characters/letter_surprised.png"
image ui_letter hit2 = "images/characters/letter_hit2.png"
image ui_letter hit3 = "images/characters/letter_hit3.png"

image ui_letter after_sad = "images/characters/letter_after_sad.png"
image ui_letter after = "images/characters/letter_after.png"

image ui_letter_scattered = "images/characters/letter_scattered.png"

# 정화 완료 이미지 오른쪽 위의 봉투 한 장만 표시
# 별도의 이미지 파일을 만들 필요 없음
image ui_letter_last = Transform(
    "images/characters/letter_after.png",
    crop=(910, 180, 300, 210)
)


# ==================================================
# 크기와 위치
# 정화 전후 같은 크기 유지
# ==================================================

# 편지 괴물: 등장 / 전투 / 정화 후 공통 크기
transform ui_letter_position:
    xysize (360, 360)
    fit "contain"
    anchor (0.5, 0.5)
    pos (1435, 550)
    zoom 1.0
    alpha 1.0
    xoffset 0
    yoffset 0


# 흩어진 편지: 작게 줄이고 바닥에 배치
transform ui_letter_scattered_position:
    xysize (420, 210)
    fit "contain"
    anchor (0.5, 1.0)
    pos (1435, 920)
    zoom 1.0
    alpha 1.0
    xoffset 0
    yoffset 0
    yoffset 0


# 흩어진 편지가 위로 모이며 사라지는 연출
transform ui_letter_gather:
    subpixel True

    parallel:
        easeout 0.65 yoffset -150 zoom 0.65

    parallel:
        ease 0.65 alpha 0.0


# 마지막에 남기는 편지
transform ui_letter_last_position:
    xysize (110, 77)
    fit "contain"
    anchor (0.5, 1.0)
    pos (1435, 920)
    zoom 1.0
    alpha 1.0
    xoffset 0
    yoffset 0


# ==================================================
# 편지 괴물 위치에 맞춘 음파 효과
# ==================================================

transform ui_letter_effect_center:
    subpixel True
    anchor (0.5, 0.5)
    pos (1435, 550)


transform ui_letter_wave_flight:
    subpixel True
    anchor (0.5, 0.5)
    pos (0.25, 0.50)

    xysize (380, 220)
    fit "contain"
    alpha 0.0

    parallel:
        linear 0.08 alpha 1.0

    parallel:
        easein 0.7 pos (1435, 550)


transform ui_letter_wave_glint:
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
        easein 0.7 pos (1350, 515)


# ==================================================
# HP
# ==================================================

screen ui_letter_hp():
    use ui_dust_hp("Letter Monster")


# ==================================================
# 공통 전투 연결
# ==================================================

label ch3_m1_battle:

    call pronunciation_battle(
        "ch3_m1",
        "Letter Monster",
        scene_battle_music,
        "letter",
        ui_letter_position
    ) from ch3_m1_pronunciation_battle_done

    jump ch3_m1_clear


# ==================================================
# 공격 성공
# ==================================================

label ui_letter_light_attack:

    window hide

    $ play_scene_sound(scene_wave_sound)

    show dust_wave_launch at ui_dust_wave_launch
    pause 0.12

    show dust_wave_flight at ui_letter_wave_flight
    show dust_wave_sparkles at ui_letter_wave_glint
    pause 0.7

    hide dust_wave_launch
    hide dust_wave_flight
    hide dust_wave_sparkles

    # 성공 횟수는 명중 시 한 번만 증가
    $ success_count += 1

    if success_count == 1:
        show ui_letter hit1 at ui_letter_position, ui_dust_hit

    elif success_count == 2:
        show ui_letter hit2 at ui_letter_position, ui_dust_hit

    else:
        show ui_letter hit3 at ui_letter_position, ui_dust_hit

    show dust_wave_impact at ui_letter_effect_center, ui_dust_wave_expand(460, 0.42, 1.22)
    show dust_wave_sparkles at ui_letter_effect_center, ui_dust_wave_expand(500, 0.44, 1.25)

    pause 0.3

    if success_count == 1:
        show ui_letter hit1 at ui_letter_position, ui_dust_idle

    elif success_count == 2:
        show ui_letter hit2 at ui_letter_position, ui_dust_idle

    else:
        show ui_letter hit3 at ui_letter_position, ui_dust_idle

    pause 0.25

    hide dust_wave_impact
    hide dust_wave_sparkles

    return


# ==================================================
# 정화
# ==================================================

label ui_letter_purification:

    window hide

    show ui_letter hit3 at ui_letter_position, ui_dust_idle

    show dust_wave_purify_ring at ui_letter_effect_center, ui_dust_wave_expand(580, 0.85, 1.28, 1.0, 30)
    pause 0.5

    show dust_wave_purify_burst at ui_letter_effect_center, ui_dust_wave_expand(610, 0.72, 1.35)
    pause 0.2

    show ui_letter after_sad at ui_letter_position, ui_dust_idle with Dissolve(0.5)
    pause 0.3

    hide dust_wave_purify_ring
    hide dust_wave_purify_burst

    window auto

    return