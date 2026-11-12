image ui_ghost = "images/characters/ghost.png"  #길잡이 유령
image ui_dust before = "images/characters/dust_before.png"  #먼지 괴물 정화 전
image ui_dust hit1 = "images/characters/dust_hit1.png"  #먼지 괴물 피격 성공 1번
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