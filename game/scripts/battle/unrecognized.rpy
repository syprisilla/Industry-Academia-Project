label ch1_m1_unrecognized:

    show ui_ghost intro_curious with Dissolve(0.2)
    ghost "Huh? I couldn't hear you very well that time."
    mc "You couldn't hear me?"
    ghost "Yeah. It was hard to tell how the word sounded."
    show ui_ghost intro_idle with Dissolve(0.2)
    ghost "Can you say it again when you're ready?"

    # Pause Little Ghost's floating animation on the help screen and resume it on return.
    show ui_ghost intro_idle at ui_ghost_corridor
    window hide None
    call screen ui_unrecognized(ui_unrec_kind)
    window auto
    show ui_ghost intro_idle at ui_ghost_corridor, ui_ghost_idle

    return