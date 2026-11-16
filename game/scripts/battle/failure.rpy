label ch1_m1_fail(reason="unknown"):

    n "The power of your voice fades before it reaches the monster."

    dust "Ha ha! Nothing happened that time!"

    show ui_ghost intro_worried with Dissolve(0.2)
    if reason == "substitution":
        ghost "The first sound came out a little differently this time."
        ghost "Let's focus on the first sound and try again!"

    elif reason == "omission":
        ghost "I think the first sound got left out this time."
        ghost "Let's try again slowly, starting with that first sound."

    else:
        ghost "I think the magic in your voice faded on the way."
        ghost "That's okay! You can try again."

    show ui_ghost intro_idle with Dissolve(0.2)
    mc "Okay! I'll give it another try."

    return