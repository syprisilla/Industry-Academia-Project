image ui_ghost = "images/characters/ghost.png"  #길잡이 유령

# 인트로 표정. 같은 태그로 기존 유령 스프라이트를 교체한다.
image ui_ghost intro_idle = "images/characters/ghost_intro/ghost_idle.png"
image ui_ghost intro_talk = "images/characters/ghost_intro/ghost_talk.png"
image ui_ghost intro_talk_closed = "images/characters/ghost_intro/ghost_talk_closed.png"
image ui_ghost intro_talk_o = "images/characters/ghost_intro/ghost_talk_o.png"
image ui_ghost intro_explain = "images/characters/ghost_intro/ghost_explain.png"
image ui_ghost intro_worried = "images/characters/ghost_intro/ghost_worried.png"
image ui_ghost intro_surprised = "images/characters/ghost_intro/ghost_surprised.png"
image ui_ghost intro_happy = "images/characters/ghost_intro/ghost_happy.png"
image ui_ghost intro_encourage = "images/characters/ghost_intro/ghost_encourage.png"
image ui_ghost intro_idea = "images/characters/ghost_intro/ghost_idea.png"
image ui_ghost intro_curious = "images/characters/ghost_intro/ghost_curious.png"
image ui_ghost intro_confident = "images/characters/ghost_intro/ghost_confident.png"
image ui_ghost intro_determined = "images/characters/ghost_intro/ghost_determined.png"
image ui_ghost intro_relief = "images/characters/ghost_intro/ghost_relief.png"
image ui_ghost intro_sad = "images/characters/ghost_intro/ghost_sad.png"
image ui_ghost intro_move = "images/characters/ghost_intro/ghost_move.png"
image ui_ghost intro_react = "images/characters/ghost_intro/ghost_react.png"

image ui_dust before = "images/characters/dust_before.png"  #먼지 괴물 정화 전
image ui_dust talk = "images/characters/dust_talk.png"
image ui_dust angry = "images/characters/dust_angry.png"
image ui_dust hit3 = "images/characters/dust_hit3.png"
image ui_dust hit1 = "images/characters/dust_surprised.png"  #먼지 괴물 피격 성공 1번
image ui_dust hit2 = "images/characters/dust_hit2.png"  #먼지 괴물 피격 성공 2번
image ui_dust after = "images/characters/dust_after.png"    #먼지 괴물 정화 후

#시작에서 유령 위치
transform ui_ghost_position:
    xysize (500, 600)
    fit "contain"
    xalign 0.85
    yalign 0.55

#시작 배경
image ui_castle = Transform(
    "images/backgrounds/castle.png",
    xysize=(1920, 1080),
    fit="cover"
)

#엘레베이터 불 '꺼진' 성 내부 배경
image ui_castle_inside = Transform(
    "images/backgrounds/castle_inside_ver1.png",
    xysize=(1920, 1080),
    fit="cover"
)

#엘레베이터 불 '켜진' 성 내부 배경
image ui_castle_inside_on = Transform(
    "images/backgrounds/castle_inside_ver2.png",
    xysize=(1920, 1080),
    fit="cover"
)

# 복도 배경
image ui_corridor = Transform(
    "images/backgrounds/corridor.png",
    xysize=(1920, 1080),
    fit="cover"
)

# 복도에서 유령 위치
transform ui_ghost_corridor:
    xysize (450, 540)
    fit "contain"
    xalign 0.10
    ypos 0.73
    yanchor 1.0

#복도에서 먼지 괴물 위치
transform ui_dust_corridor:
    xysize (600, 600)
    fit "contain"
    xalign 0.86
    ypos 0.78
    yanchor 1.0

# 정화 후 캐릭터 크기와 위치
transform ui_dust_after_position:
    xysize (300, 300)
    fit "contain"

    xalign 0.68
    ypos 0.73
    yanchor 1.0

    xoffset 0
    yoffset 0
    alpha 1.0


# 위치 트랜스폼 뒤에 붙여 사용하는 캐릭터 동작.
transform ui_ghost_idle:
    subpixel True
    block:
        ease 1.25 yoffset -14
        ease 1.25 yoffset 0
        repeat


# 같은 이미지 태그에서 표정이 바뀌어도 떠 있는 주기를 유지한다.
transform ghost_float:
    animation
    ui_ghost_idle


transform ui_ghost_react:
    subpixel True
    easeout 0.16 xoffset -16 yoffset -34
    easein 0.34 xoffset 0 yoffset -8
    ui_ghost_idle


transform ui_ghost_settle:
    subpixel True
    ease 0.3 xoffset 0 yoffset 0


transform ui_dust_idle:
    subpixel True
    block:
        ease 1.25 xoffset 0 yoffset -12
        ease 1.25 yoffset 0
        repeat


transform ui_dust_emerge:
    subpixel True
    alpha 0.0
    zoom 0.82
    yoffset 24
    easeout 0.55 alpha 1.0 zoom 1.0 yoffset 0
    ui_dust_idle


transform ui_dust_threaten:
    subpixel True
    easeout 0.22 alpha 1.0 zoom 1.07 xoffset -16 yoffset -6
    easein 0.34 zoom 1.0 xoffset 0 yoffset 0
    ui_dust_idle


transform ui_dust_purified:
    subpixel True
    alpha 1.0
    xoffset 0
    easeout 0.4 zoom 1.0 yoffset 0
    ui_dust_idle
