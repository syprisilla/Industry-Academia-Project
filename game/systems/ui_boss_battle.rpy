# ==================================================
# 최종 보스 이미지
# 그림 파일이 아직 없으면 대체 이미지가 자동으로 나온다.
#   1순위 파일 → 2순위 파일 → ... → 임시 상자
# 파일을 images/characters/ 에 넣기만 하면 바로 적용됨
# ==================================================

init python:

    def ui_boss_pic(*names):
        """앞에서부터 있는 파일을 사용하고, 하나도 없으면 임시 상자를 보여 준다."""
        for name in names:
            path = "images/characters/" + name
            if renpy.loadable(path):
                return path

        return Fixed(
            Solid("#2A2440CC"),
            Text(
                "Final Boss\n({})\nImage coming soon".format(names[0]),
                size=30,
                color="#F8F5FF",
                text_align=0.5,
                align=(0.5, 0.5),
            ),
            xysize=(540, 540),
        )

    def ui_boss_background(name, fallback):
        """보스 배경이 없으면 기존 복도 배경을 어둡게 해서 대신 사용"""
        path = "images/backgrounds/" + name
        if renpy.loadable(path):
            return path
        return Transform(
            "images/backgrounds/" + fallback,
            matrixcolor=BrightnessMatrix(-0.22) * SaturationMatrix(0.7),
        )


# 기본 / 대사
image ui_boss before = ui_boss_pic("boss_before.png")
image ui_boss talk = ui_boss_pic("boss_talk.png", "boss_before.png")
image ui_boss angry = ui_boss_pic("boss_angry.png", "boss_before.png")
image ui_boss laugh = ui_boss_pic("boss_laugh.png", "boss_talk.png", "boss_before.png")

# 검은 구슬을 들어 올린 모습
image ui_boss orb = ui_boss_pic("boss_orb.png", "boss_angry.png", "boss_before.png")

# 피격 1~3: 구슬에 금이 점점 커지는 모습
image ui_boss hit1 = ui_boss_pic("boss_surprised.png", "boss_before.png")
image ui_boss hit2 = ui_boss_pic("boss_hit2.png", "boss_surprised.png", "boss_before.png")
image ui_boss hit3 = ui_boss_pic("boss_hit3.png", "boss_hit2.png", "boss_before.png")

# 저주가 풀려 사라지기 직전
image ui_boss defeated = ui_boss_pic("boss_defeated.png", "boss_hit3.png", "boss_before.png")


# ==================================================
# 보스 배경 (apartment 태그를 같이 써서 다른 배경과 자연스럽게 교체)
# ==================================================

image apartment boss_door = apartment_background(
    ui_boss_background("apartment_boss_door.png", "apartment_corridor_4.png")
)

image apartment boss_room = apartment_background(
    ui_boss_background("apartment_boss_room.png", "apartment_corridor_4.png")
)

# 구슬을 들면 방이 어두워지는 효과
image ui_boss_darkness = Solid("#0B061870")


# ==================================================
# 크기와 위치
# 다른 괴물보다 크게, 단어 패널(위)과 겹치지 않는 높이
# ==================================================

transform ui_boss_position:
    xysize (540, 540)
    fit "contain"
    anchor (0.5, 0.5)
    pos (1435, 590)
    zoom 1.0
    alpha 1.0
    xoffset 0
    yoffset 0

# 구슬을 든 그림은 몸이 작게 그려져 있어서 1.25배 크게 표시 (발 위치는 같게)
transform ui_boss_orb_position:
    xysize (675, 675)
    fit "contain"
    anchor (0.5, 0.5)
    pos (1435, 527)
    zoom 1.0
    alpha 1.0
    xoffset 0
    yoffset 0    

# 문이 열리며 그림자 속에서 천천히 나타남
transform ui_boss_emerge:
    subpixel True
    alpha 0.0
    zoom 0.86
    yoffset 30
    easeout 0.9 alpha 1.0 zoom 1.0 yoffset 0
    ui_dust_idle


# 위협: 앞으로 크게 다가왔다가 돌아감
transform ui_boss_threaten:
    subpixel True
    easeout 0.22 zoom 1.1 xoffset -24 yoffset -8
    easein 0.36 zoom 1.0 xoffset 0 yoffset 0
    ui_dust_idle


# 검은 연기와 함께 사라짐
transform ui_boss_vanish:
    subpixel True
    alpha 1.0
    parallel:
        easein 1.1 alpha 0.0
    parallel:
        easein 1.1 zoom 0.72 yoffset -50


transform ui_boss_darkness_fade:
    alpha 0.0
    linear 0.6 alpha 1.0


# ==================================================
# 보스 위치에 맞춘 음파 효과
# ==================================================

transform ui_boss_effect_center:
    subpixel True
    anchor (0.5, 0.5)
    pos (1435, 590)


transform ui_boss_wave_flight:
    subpixel True
    anchor (0.5, 0.5)
    pos (0.25, 0.50)

    xysize (380, 220)
    fit "contain"
    alpha 0.0

    parallel:
        linear 0.08 alpha 1.0

    parallel:
        easein 0.7 pos (1435, 590)


transform ui_boss_wave_glint:
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
        easein 0.7 pos (1350, 555)


# ==================================================
# HP
# ==================================================

screen ui_boss_hp():
    use ui_dust_hp("Final Boss")


# ==================================================
# 공통 전투 연결
# ==================================================

label ch3_m3_battle:

    call pronunciation_battle(
        "ch3_m3",
        "Final Boss",
        scene_boss_music,
        "boss",
        ui_boss_position
    ) from ch3_m3_pronunciation_battle_done

    jump ch3_m3_clear


# ==================================================
# 공격 성공
# 보스는 맞을 때 화면도 함께 흔들림
# ==================================================

label ui_boss_light_attack:

    window hide

    $ play_scene_sound(scene_wave_sound)

    show dust_wave_launch at ui_dust_wave_launch
    pause 0.12

    show dust_wave_flight at ui_boss_wave_flight
    show dust_wave_sparkles at ui_boss_wave_glint
    pause 0.7

    hide dust_wave_launch
    hide dust_wave_flight
    hide dust_wave_sparkles

    # 성공 횟수는 명중 시 한 번만 증가
    $ success_count += 1

    if success_count == 1:
        show ui_boss hit1 at ui_boss_position, ui_dust_hit
    elif success_count == 2:
        show ui_boss hit2 at ui_boss_position, ui_dust_hit
    else:
        show ui_boss hit3 at ui_boss_position, ui_dust_hit

    show dust_wave_impact at ui_boss_effect_center, ui_dust_wave_expand(560, 0.42, 1.08 + 0.14 * success_count)
    show dust_wave_sparkles at ui_boss_effect_center, ui_dust_wave_expand(600, 0.44, 1.25, 0.45 + 0.17 * success_count)
    with vpunch

    pause 0.3

    if success_count == 1:
        show ui_boss hit1 at ui_boss_position, ui_dust_idle
    elif success_count == 2:
        show ui_boss hit2 at ui_boss_position, ui_dust_idle
    else:
        show ui_boss hit3 at ui_boss_position, ui_dust_idle

    pause 0.25

    hide dust_wave_impact
    hide dust_wave_sparkles

    return


# ==================================================
# 저주 해제: 구슬이 깨지고 보스가 검은 연기처럼 사라짐
# ==================================================

label ui_boss_purification:

    window hide

    show ui_boss hit3 at ui_boss_position, ui_dust_idle

    show dust_wave_purify_ring at ui_boss_effect_center, ui_dust_wave_expand(660, 0.85, 1.35, 1.0, 30)
    pause 0.5

    show dust_wave_purify_burst at ui_boss_effect_center, ui_dust_wave_expand(700, 0.72, 1.45)
    with vpunch
    pause 0.2

    show ui_boss defeated at ui_boss_position, ui_boss_vanish with Dissolve(0.3)
    pause 1.1

    hide ui_boss
    hide dust_wave_purify_ring
    hide dust_wave_purify_burst

    window auto

    return
