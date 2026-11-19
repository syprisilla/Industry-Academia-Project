#chapter1
# ==================================================
# MONSTER 1. Dust Monster Success dialogue
# ==================================================

label ch1_m1_success_1:

    n "Sparkling light bursts from our hero's voice."
    n "The light flies straight into the Dust Monster."

    dust "Aah! What kind of power is that?!"
    mc "Wow! It really worked!"
    show ui_ghost intro_happy with Dissolve(0.2)
    ghost "Nice work! That's the power of your voice!"

    ghost "Just two more hits!"

    return


label ch1_m1_success_2:

    n "A second flash of light shoots toward the Dust Monster."
    n "The monster's angry face softens."

    dust "Ugh... I'm shrinking..."
    show ui_ghost intro_talk with Dissolve(0.2)
    ghost "Just one more hit!"

    return


label ch1_m1_success_3:

    n "Our hero's voice turns into one last flash of light."

    dust "Aaaah! My body...!"
    mc "I did it!"
    show ui_ghost intro_happy with Dissolve(0.2)
    ghost "That last hit worked too!"

    return


# ==================================================
# MONSTER 2. Echo Monster Success dialogue
# ==================================================

label ch1_m2_success_1:

    n "Our hero's voice turns to light and flies toward the Echo Monster."

    echo "Aah! My echoes are wavering!"
    mc "Yes! It worked again!"
    show ui_ghost intro_happy with Dissolve(0.2)
    ghost "Great job! The monster is getting weaker!"

    echo "Hmph! This isn't over yet!"

    ghost "Let's keep going too!"

    return


label ch1_m2_success_2:

    n "A second flash of light reaches the Echo Monster."
    n "The strange voices swirling around the monster grow quieter."

    echo "No! My voices are fading!"
    mc "I hit it again!"
    show ui_ghost intro_talk with Dissolve(0.2)
    ghost "Nice work! Just one more hit."

    mc "I'll give it my best right to the end!"

    return


label ch1_m2_success_3:

    n "The last flash of light flies toward the Echo Monster."
    n "The echoes around the monster stop all at once."

    echo "Aaaah! My echoes...!"
    mc "I did it!"
    show ui_ghost intro_happy with Dissolve(0.2)
    ghost "Great! It worked again!"

    return


# ==================================================
# MONSTER 3. Shadow Monster Success dialogue
# ==================================================

label ch1_m3_success_1:

    n "Our hero's voice turns into a bright light."
    n "The light shoots toward the Shadow Monster and hits it."

    shadow "Urgh! What is this light?"
    mc "It worked!"
    show ui_ghost intro_happy with Dissolve(0.2)
    ghost "Nice work! Your voice is weakening the curse!"

    shadow "You still can't get past me!"

    mc "Then I'll try again!"

    return


label ch1_m3_success_2:

    n "A second flash of light reaches the Shadow Monster."
    n "The dark shadow wrapped around the monster starts to crack."

    shadow "Impossible... My power is fading!"
    mc "Almost there!"
    show ui_ghost intro_talk with Dissolve(0.2)
    ghost "That's right! Just one more hit!"

    mc "One last attack!"

    return


label ch1_m3_success_3:

    n "Our hero's voice turns into a dazzling light."
    n "The light wraps around the Shadow Monster and drives the darkness away."

    shadow "Aaaah! The curse... is breaking!"
    mc "I did it! The last hit worked!"
    show ui_ghost intro_happy with Dissolve(0.2)
    ghost "You did great!"

    return

#chapter2
# ==================================================
# MONSTER 1. Whisper Monster Success dialogue
# ==================================================
label ch2_m1_success_1:

    n "Our hero's voice turns to light and flies toward the monster."

    whisper "Hey! What's that light?!"
    mc "Wow! The attack worked!"

    ghost "Nice work! The monster is a little weaker now."
    ghost "Just two more hits!"

    return

label ch2_m1_success_2:

    n "Another flash of light flies out and wraps around the monster."

    whisper "Aah! My whispers are fading!"
    mc "I think we're almost there!"

    ghost "That's right! Just one more hit!"
    ghost "Keep it up to the very end!"

    return

label ch2_m1_success_3:

    n "The last flash of light reaches the monster."

    whisper "Aaaah! The darkness is leaving my body!"

    mc "I did it!"
    ghost "Great! The curse is breaking!"

    return

# ==================================================
# MONSTER 2. Toy Monster Success dialogue
# ==================================================

label ch2_m2_success_1:
    n "The light from our hero's voice reaches the Toy Monster, and one of the toy box's locks pops open."
    ch2_toy "Oh! My box is opening!"
    mc "It worked!"
    ghost "Nice work! Let's do that two more times!"
    
    return

label ch2_m2_success_2:
    n "The second flash of light brightens the toy box."
    ch2_toy "Do I really have to keep my friends locked up...?"
    mc "The curse is breaking bit by bit!"
    ghost "Great! Just one more hit!"
    
    return

label ch2_m2_success_3:
    n "The last flash of light wraps around the Toy Monster, and the darkness fades."
    ch2_toy "Oh... Why was I so angry?"
    mc "I did it!"
    ghost "Nice work! The curse is breaking!"
   
    return

# ==================================================
# MONSTER 3. Clock Monster Success dialogue
# ==================================================

label ch2_m3_success_1:
    n "The light from our hero's voice reaches the Clock Monster, and the clock hands move a little."
    ch2_clock "No! Time has to stay still!"
    mc "Wow! The attack worked!"
    ghost "Nice work! Let's do that two more times!"
    
    return

label ch2_m3_success_2:
    n "A second flash of light reaches the clock, and the second hand begins to tick."
    ch2_clock "You mean I can't go back to that day...?"
    mc "I think we're almost there!"
    ghost "That's right! Just one more!"
    
    return

label ch2_m3_success_3:
    n "The last flash of light reaches the Clock Monster, and the darkness scatters."
    ch2_clock "Oh... It's time to move on."
    mc "I did it!"
    ghost "Great! The last curse is broken too!"
    
    return


#chapter3
# ==================================================
# MONSTER 1. Letter Monster Success dialogue
# ==================================================

# ==================================================
# MONSTER 1. Letter Monster Success dialogue
# ==================================================

label ch3_m1_success_1:

    n "Our hero's voice turns to light and flies toward the Letter Monster."
    n "The letters flying around the monster stop in midair."

    ch3_letter "Aah! What did you do to my letters?!"
    mc "Yes! The attack worked!"
    ghost "Nice work! Just two more hits!"

    return


label ch3_m1_success_2:

    n "A second flash of light reaches the Letter Monster."
    n "The darkness around the monster slowly fades."

    ch3_letter "No! I still have to wait...!"
    mc "Almost there!"
    ghost "Great! Just one more hit!"

    return


label ch3_m1_success_3:

    n "The last flash of light wraps around the Letter Monster."
    n "The darkness leaves the monster completely."

    ch3_letter "Huh...? What was I doing?"
    mc "I did it!"
    ghost "Nice work! The curse is broken!"

    return


# ==================================================
# MONSTER 2. Thorny Vine Monster Success dialogue
# ==================================================

label ch3_m2_success_1:

    n "Our hero's voice turns to light and flies toward the Thorny Vine Monster."
    n "The thorns covering the monster begin to shrink."

    ch3_vine "Aah! My thorns are disappearing!"
    mc "Wow! The attack worked!"
    ghost "Nice work! Just two more hits!"

    return


label ch3_m2_success_2:

    n "A second flash of light reaches the Thorny Vine Monster."
    n "The vines blocking the hallway begin to unwind."

    ch3_vine "No! It's dangerous over there!"
    mc "I think we're almost there!"
    ghost "That's right! Just one more hit!"

    return


label ch3_m2_success_3:

    n "The last flash of light wraps around the Thorny Vine Monster."
    n "The darkness surrounding the monster disappears."

    ch3_vine "Ugh... The curse is finally broken!"
    mc "I did it!"
    ghost "Great! It worked again!"

    return

# ==================================================
# MONSTER 3. Final Boss Success dialogue
# ==================================================

label ch3_m3_success_1:

    n "Our hero's voice turns into a bright light and shoots toward the Final Boss."
    n "A tiny crack appears in the black orb he's holding."

    ch3_boss "Urgh! How dare you crack my source of power!"
    mc "It worked!"
    ghost "Nice work! The curse is getting weaker!"

    ghost "Just two more hits!"

    return


label ch3_m3_success_2:

    n "A second flash of light strikes the black orb."
    n "The crack in the orb grows wider."

    ch3_boss "No! My curse is losing its power...!"
    mc "Yes! Almost there!"
    ghost "Just one last hit!"

    ch3_boss "I will never lose to you!"

    return


label ch3_m3_success_3:

    n "Our hero's voice turns into one last dazzling light."
    n "The light shoots through the black orb with a mighty blast."

    ch3_boss "Aaaah! My curse...!"
    mc "I did it! The last hit worked!"
    ghost "You did great! We won!"

    return
