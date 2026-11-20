# ==================================================
# 엔딩: 정화된 괴물들이 모여 인사하고 빛 속으로 사라짐
# chapter3.rpy 의 ch3_finish 에서 사용
# ==================================================


# --------------------------------------------------
# 정화 후 이미지 (빈 여백을 잘라서 크기를 맞춤)
# --------------------------------------------------

image ending_dust = Transform("images/characters/dust_after.png", crop=(127, 88, 393, 345))
image ending_echo = Transform("images/characters/echo_after.png", crop=(66, 136, 1403, 730))
image ending_shadow = Transform("images/characters/shadow_after.png", crop=(242, 0, 1108, 859))
image ending_whisper = Transform("images/characters/whisper_after.png", crop=(63, 142, 1122, 1021))
image ending_toy = Transform("images/characters/toy_after.png", crop=(189, 576, 942, 598))
image ending_clock = Transform("images/characters/clock_after.png", crop=(148, 64, 939, 1174))
image ending_letter = Transform("images/characters/letter_after.png", crop=(63, 82, 1124, 1138))
image ending_vine = Transform("images/characters/thorny_vine_after.png", crop=(174, 112, 943, 1071))


# 저주가 풀려 밝아진 보스방
init python:

    def ui_ending_background():
        path = "images/backgrounds/apartment_boss_room.png"
        if not renpy.loadable(path):
            path = "images/backgrounds/apartment_corridor_4.png"
        return Transform(
            path,
            matrixcolor=BrightnessMatrix(0.1) * TintMatrix("#FFE9CC"),
        )

image apartment boss_room_bright = apartment_background(ui_ending_background())

# 건물 전체에 퍼지는 따뜻한 빛
image ui_ending_glow = Solid("#FFD49A")


# --------------------------------------------------
# 괴물 자리 (x, 발 위치 y, 크기)
#   뒷줄: 먼지 / 메아리 / 그림자 / 속삭임
#   앞줄: 장난감 / 시계 / 편지 / 가시덩굴
# 크기나 위치가 어색하면 여기 숫자만 바꾸면 됨
# --------------------------------------------------

define ui_ending_slots = {
    "dust":    (760, 560, 190),
    "echo":    (1040, 560, 230),
    "shadow":  (1320, 560, 220),
    "whisper": (1600, 560, 220),
    "toy":     (900, 790, 250),
    "clock":   (1180, 790, 240),
    "letter":  (1460, 790, 240),
    "vine":    (1740, 790, 240),
}

# 사라지는 순서
define ui_ending_order = ["dust", "echo", "shadow", "whisper", "toy", "clock", "letter", "vine"]


transform ui_ending_slot(x, y, size):
    xysize (size, size)
    fit "contain"
    anchor (0.5, 1.0)
    pos (x, y)


# 둥실둥실 떠 있기
transform ui_ending_idle:
    subpixel True
    block:
        ease 1.3 yoffset -10
        ease 1.3 yoffset 0
        repeat


# 한 마리씩 톡 나타남
transform ui_ending_pop:
    subpixel True
    alpha 0.0
    zoom 0.6
    yoffset 30
    easeout 0.45 alpha 1.0 zoom 1.0 yoffset 0
    ui_ending_idle


# 다 같이 기뻐서 폴짝
transform ui_ending_hop:
    subpixel True
    alpha 1.0
    zoom 1.0
    easeout 0.16 yoffset -34
    easein 0.22 yoffset 0
    easeout 0.16 yoffset -22
    easein 0.2 yoffset 0
    ui_ending_idle


# 손 흔들듯 좌우로 흔들기
transform ui_ending_wave:
    subpixel True
    alpha 1.0
    zoom 1.0
    yoffset 0
    block:
        ease 0.35 rotate -6
        ease 0.35 rotate 6
        repeat 3
    ease 0.3 rotate 0
    ui_ending_idle


# 위로 떠오르며 빛 속으로 사라짐
transform ui_ending_vanish:
    subpixel True
    rotate 0
    parallel:
        easein 0.8 alpha 0.0
    parallel:
        easein 0.8 yoffset -80 zoom 1.12


# 사라지는 자리에 반짝이
transform ui_ending_sparkle(x, y):
    subpixel True
    anchor (0.5, 0.5)
    pos (x, y)
    xysize (260, 260)
    fit "contain"
    alpha 0.0
    zoom 0.6
    easeout 0.25 alpha 1.0 zoom 1.0
    easein 0.6 alpha 0.0 zoom 1.35


transform ui_ending_glow_fade:
    alpha 0.0
    linear 1.2 alpha 0.14
    block:
        ease 2.0 alpha 0.18
        ease 2.0 alpha 0.12
        repeat


init python:

    def ui_ending_show(name, motion=None):
        """괴물 한 마리를 자기 자리에 보여 준다. 처음이면 톡 나타나는 연출."""
        x, y, size = ui_ending_slots[name]
        renpy.show(
            "ending_" + name,
            at_list=[ui_ending_slot(x, y, size), motion or ui_ending_pop],
        )


# --------------------------------------------------
# 엔딩 시작: 따뜻한 빛이 퍼지며 방이 밝아짐
# --------------------------------------------------

label ui_ending_light:

    window hide

    show apartment boss_room_bright behind ui_ghost with Dissolve(1.2)
    show ui_ending_glow behind ui_ghost at ui_ending_glow_fade

    pause 0.6

    window auto

    return


# --------------------------------------------------
# 다 같이 기뻐하기
# --------------------------------------------------

label ui_ending_cheer:

    python:
        for name in ui_ending_order:
            ui_ending_show(name, ui_ending_hop)

    return


# --------------------------------------------------
# 다 같이 손 흔들기
# --------------------------------------------------

label ui_ending_goodbye:

    python:
        for name in ui_ending_order:
            ui_ending_show(name, ui_ending_wave)

    return


# --------------------------------------------------
# 한 마리씩 빛이 되어 사라짐
# --------------------------------------------------

label ui_ending_farewell:

    window hide

    python:
        for name in ui_ending_order:
            x, y, size = ui_ending_slots[name]
            ui_ending_show(name, ui_ending_vanish)
            renpy.show(
                "ending_sparkle_" + name,
                what=renpy.displayable("dust_wave_sparkles"),
                at_list=[ui_ending_sparkle(x, y - size // 2)],
            )
            renpy.pause(0.35, hard=True)

    pause 0.9

    python:
        for name in ui_ending_order:
            renpy.hide("ending_" + name)
            renpy.hide("ending_sparkle_" + name)

    window auto

    return
