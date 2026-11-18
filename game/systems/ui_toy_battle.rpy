# ========================================
# 장난감 괴물 이미지
# ========================================

image ui_toy before = "images/characters/toy_before.png"
image ui_toy talk = "images/characters/toy_talk.png"
image ui_toy angry = "images/characters/toy_angry.png"

image ui_toy hit1 = "images/characters/toy_surprised.png"
image ui_toy hit2 = "images/characters/toy_hit2.png"
image ui_toy hit3 = "images/characters/toy_hit3.png"

image ui_toy after = "images/characters/toy_after.png"

image ui_toy_box closed = "images/characters/toy_box_closed.png"
image ui_toy_box open = "images/characters/toy_box_open.png"

image ui_toy_ball rolling = "images/characters/toy_rolling_ball.png"
image ui_toy_ball still = "images/characters/toy_ball.png"


# ========================================
# 크기와 위치
# 공격 효과가 도착하는 위치에 맞춤
# ========================================

transform ui_toy_effect_center:
    anchor (0.5, 0.5)
    pos (1435, 630)

transform ui_toy_position:
    xysize (560, 560)
    fit "contain"
    anchor (0.5, 0.5)
    pos (1435, 630)

    zoom 1.0
    alpha 1.0
    xoffset 0
    yoffset 0


# after 이미지 안에 작은 곰과 상자가 함께 있으므로
# 이미지 전체 크기는 유지
transform ui_toy_after_position:
    xysize (620, 620)
    fit "contain"
    anchor (0.5, 0.5)
    pos (1435, 536)

    zoom 1.0
    alpha 1.0
    xoffset 0
    yoffset 0


transform ui_toy_box_position:
    xysize (520, 520)
    fit "contain"
    anchor (0.5, 1.0)
    pos (1435, 830)

    alpha 1.0
    xoffset 0
    yoffset 0


# 공이 복도 안쪽에서 앞으로 굴러오는 연출
transform ui_toy_ball_roll:
    subpixel True
    xysize (150, 150)
    fit "contain"
    anchor (0.5, 0.5)

    pos (1000, 650)
    zoom 0.45
    rotate 0

    easeout 1.6 pos (1200, 780) zoom 1.0 rotate 360


transform ui_toy_ball_stop:
    xysize (150, 150)
    fit "contain"
    anchor (0.5, 0.5)
    pos (1200, 780)

    zoom 1.0
    rotate 0
    alpha 1.0


transform ui_toy_box_shake:
    subpixel True

    block:
        linear 0.07 xoffset -10
        linear 0.07 xoffset 10
        repeat 4

    linear 0.07 xoffset 0


# ========================================
# HP 패널
# 공통 전투의 success_count 사용
# ========================================

screen ui_toy_hp():
    use ui_dust_hp("Toy Monster")


# ========================================
# 장난감 괴물 전투
# 단어 선택·녹음·발음 판정은 공통 로직 사용
# ========================================

label ch2_m2_battle:

    call pronunciation_battle(
        "ch2_m2",
        "Toy Monster",
        scene_battle_music,
        "toy",
        ui_toy_position
    ) from ch2_m2_pronunciation_battle_done

    jump ch2_m2_clear


# ========================================
# 공격 성공 연출
# 공통 전투에서 호출
# ========================================

label ui_toy_light_attack:

    window hide

    $ play_scene_sound(scene_wave_sound)

    show dust_wave_launch at ui_dust_wave_launch
    pause 0.12

    show dust_wave_flight at ui_dust_wave_flight
    show dust_wave_sparkles at ui_dust_wave_glint
    pause 0.7

    hide dust_wave_launch
    hide dust_wave_flight
    hide dust_wave_sparkles

    # 성공 횟수는 여기에서 한 번만 증가
    $ success_count += 1

    if success_count == 1:
        show ui_toy hit1 at ui_toy_position, ui_dust_hit
    elif success_count == 2:
        show ui_toy hit2 at ui_toy_position, ui_dust_hit
    else:
        show ui_toy hit3 at ui_toy_position, ui_dust_hit

    show dust_wave_impact at ui_dust_wave_center, ui_dust_wave_expand(460, 0.42, 1.22)
    show dust_wave_sparkles at ui_dust_wave_center, ui_dust_wave_expand(500, 0.44, 1.25)

    pause 0.3

    if success_count == 1:
        show ui_toy hit1 at ui_toy_position, ui_dust_idle
    elif success_count == 2:
        show ui_toy hit2 at ui_toy_position, ui_dust_idle
    else:
        show ui_toy hit3 at ui_toy_position, ui_dust_idle

    pause 0.4

    hide dust_wave_impact
    hide dust_wave_sparkles

    return


# ========================================
# 정화 연출
# ========================================

label ui_toy_purify:

    window hide

    # 이전 코드에서 표시됐을 수 있는 잘못된 이미지 제거
    hide dust_purify_ring
    hide dust_purify_burst

    show ui_toy hit3 at ui_toy_position, ui_dust_idle

    # 다른 괴물과 같은 정화 효과
    show dust_wave_purify_ring at ui_toy_effect_center, ui_dust_wave_expand(600, 0.85, 1.28, 1.0, 30)
    pause 0.5

    show dust_wave_purify_burst at ui_toy_effect_center, ui_dust_wave_expand(630, 0.72, 1.35)
    pause 0.2

    # 작은 곰과 열린 상자로 변경
    show ui_toy after at ui_toy_after_position, ui_dust_idle with Dissolve(0.5)

    pause 0.3

    hide dust_wave_purify_ring
    hide dust_wave_purify_burst

    window auto

    return