label ch1_m1_unrecognized:

    show ui_ghost intro_curious with Dissolve(0.2)
    ghost "어? 방금 목소리를 잘 듣지 못했어."
    mc "내 목소리가 안 들렸어?"
    ghost "응. 이번에는 발음을 확인하기 어려웠어."
    show ui_ghost intro_idle with Dissolve(0.2)
    ghost "준비되면 다시 말해 줄래?"

    # 안내 화면에서는 유령이 떠다니지 않게 멈췄다가, 돌아오면 다시 띄운다.
    show ui_ghost intro_idle at ui_ghost_corridor
    window hide None
    call screen ui_unrecognized(ui_unrec_kind)
    window auto
    show ui_ghost intro_idle at ui_ghost_corridor, ui_ghost_idle

    return