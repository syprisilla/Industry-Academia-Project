
# ==================================================
# Chapter 1. The Power of Your Voice - First Floor Monsters
# ==================================================


label chapter1:

    $ current_chapter = 1

    # ==========================================
    # SCENE 1. First floor
    # ==========================================

    n "The elevator slowly starts to move."

    window hide

    $ play_scene_music(scene_corridor_music, volume=scene_corridor_volume)
    scene apartment corridor_1
    show ui_ghost intro_idle at ui_ghost_corridor, ui_ghost_idle
    with fade

    window auto
    #Switch to the first-floor hallway and move Little Ghost to the left.

    $ play_scene_sound(scene_elevator_sound)
    n "A moment later, the doors open onto a dark hallway."

    mc "Is this the first floor?"
    show ui_ghost intro_worried with Dissolve(0.2)
    ghost "Yep! This is where the monsters start to show up."
    mc "Do you really think I can beat them?"
    show ui_ghost intro_talk_closed with Dissolve(0.2)
    ghost "Of course! Remember, there's a special power in your voice."
    mc "But how do I use it?"
    ghost "Don't worry. I'll be right here to show you!"

    n "Just then, something rustles at the end of the hall."

    mc "Huh? What's that sound?"

    jump ch1_m1_start


# ==================================================
# MONSTER 1. Dust Monster
# ==================================================

label ch1_m1_start:

    $ play_scene_music(scene_corridor_music, volume=scene_corridor_volume)

    # ==========================================
    # SCENE 2. The first monster appears
    # ==========================================

    show apartment corridor_2 behind ui_ghost with fade
    n "A pile of dust in the corner starts to wiggle."

    $ play_scene_music(scene_battle_music, volume=scene_battle_volume)
    show ui_dust before at ui_dust_corridor, ui_dust_emerge
    show ui_ghost intro_surprised
    #The Dust Monster appears.

    n "The dust clumps together and turns into a huge monster."

    show ui_dust talk with Dissolve(0.16)
    dust "Mwahaha! This is my floor!"
    mc "Whoa! The dust can talk!"
    show ui_dust angry at ui_dust_corridor, ui_dust_threaten
    show ui_ghost intro_surprised at ui_ghost_corridor, ui_ghost_react
    dust "Nobody gets past me!"

    show ui_dust before
    show ui_ghost intro_worried with Dissolve(0.2)
    ghost "There's our first monster!"
    show ui_ghost intro_talk_closed with Dissolve(0.2)
    ghost "Time to use the power of your voice."

    mc "But how do I attack?"

    # ==========================================
    # SCENE 3. Explain how to battle
    # ==========================================

    show ui_ghost intro_explain with Dissolve(0.2)
    ghost "First, warm up your voice with a word that's easy for you."
    ghost "Then say the practice word that pops up on the screen!"
    mc "All I have to do is say the word?"
    show ui_ghost intro_talk_closed with Dissolve(0.2)
    ghost "Yep! Say it clearly, and your voice will send its power right at the monster."
    ghost "Land three hits and you'll break the monster's curse!"

    mc "Okay! I'll give it a try!"

    call ch1_articulation_guide from ch1_m1_articulation_guide_done

    # --------------------------------------------------
    # TODO Start the first monster battle
    # Show the key word, then the practice word
    # Record speech and analyze pronunciation
    # Successful hits 0/3, monster HP 3
    #
    # Success -> ch1_m1_success_1
    # Failure -> ch1_m1_fail
    # Unrecognized -> ch1_m1_unrecognized
    # --------------------------------------------------

    # [Temporary test] Play three success scenes before battle is implemented
    jump ch1_m1_battle


# --------------------------------------------------
# MONSTER 1. Prompt the player to speak
# --------------------------------------------------

label ch1_m1_prompt:

    show ui_ghost intro_talk with Dissolve(0.2)
    ghost "Ready? Say the word on the screen slowly!"

    # TODO Practice saying the key word, then the practice word
    # Play the dialogue for the practice word result

    return


# --------------------------------------------------
# MONSTER 1. Battle complete
# --------------------------------------------------

label ch1_m1_clear:

    # ==========================================
    # SCENE 4. Break the first monster's curse
    # ==========================================

    n "The darkness around the Dust Monster fades away."

    call ui_dust_purification from ch1_m1_purification_done
    #Break the Dust Monster's curse

    show ui_ghost intro_relief with Dissolve(0.2)
    dust "Huh...? I feel lighter!"
    dust "Thank you! A strange curse was making me do things I didn't want to do."

    mc "So the curse turned you into a monster?"
    ghost "That's right. The monsters in this building are under a curse."
    ghost "And your voice can break it!"

    mc "Then we should help the other monsters too!"
    show ui_ghost intro_happy with Dissolve(0.2)
    ghost "Exactly! Come on, let's keep going."


    hide ui_dust after with dissolve
    $ play_scene_music(scene_corridor_music, volume=scene_corridor_volume)
    n "With the monster gone, the way down the hall is clear."

    $ cleared_monsters.add((1, 1))
    call progress_autosave from ch1_m1_autosaved
    # Go to ch1_m2_start

    # [Temporary test] Move to the next monster after freeing the first
    jump ch1_m2_start


# ==================================================
# MONSTER 2. Echo Monster
# ==================================================

label ch1_m2_start:

    # ==========================================
    # SCENE 5. The second monster appears
    # ==========================================

    show apartment corridor_3 behind ui_ghost with fade
    n "Our hero and Little Ghost walk down the hallway."
    show ui_ghost intro_curious with Dissolve(0.2)
    n "Just then, a strange voice rings out."

    mc "I hear a weird sound..."

    echo "Sound... sound... sound..."

    mc "Huh? It's copying me!"

    echo "Copying me... copying me!"

    $ play_scene_music(scene_battle_music, volume=scene_battle_volume)
    n "A round monster drops down from the ceiling."

    mc "It's another monster!"
    show ui_ghost intro_worried with Dissolve(0.2)
    ghost "Look out! That's the Echo Monster."
    ghost "It steals people's voices and copies them perfectly!"

    echo "I'll take your voice too!"

    mc "You can't have my voice!"
    show ui_ghost intro_talk_closed with Dissolve(0.2)
    ghost "Don't worry! Just do what we practiced."

    # ==========================================
    # SCENE 6. Prepare for the second battle
    # ==========================================

    show ui_ghost intro_explain with Dissolve(0.2)
    ghost "Let's warm up with a familiar word again."
    ghost "Then say the practice word on the screen!"

    mc "Got it! I'll take it from here."

    echo "Hee hee! Let's see if you can beat my echoes!"

    # --------------------------------------------------
    # TODO Start the second monster battle
    # Show the key word, then the practice word
    # Record speech and analyze pronunciation
    # Successful hits 0/3, monster HP 3
    #
    # Success -> ch1_m2_success_1
    # Failure -> ch1_m2_fail
    # Unrecognized -> ch1_m2_unrecognized
    # --------------------------------------------------

    # [Temporary test] Play three success scenes before battle is implemented
    call ch1_m2_success_1
    call ch1_m2_success_2
    call ch1_m2_success_3

    jump ch1_m2_clear


# --------------------------------------------------
# MONSTER 2. Prompt the player to speak
# --------------------------------------------------

label ch1_m2_prompt:

    show ui_ghost intro_talk with Dissolve(0.2)
    ghost "Great! Let's say the word on the screen!"

    # TODO Practice saying the key word, then the practice word
    # Play the dialogue for the practice word result

    return

# --------------------------------------------------
# MONSTER 2. Battle complete
# --------------------------------------------------

label ch1_m2_clear:

    # ==========================================
    # SCENE 7. Break the second monster's curse
    # ==========================================

    n "The darkness around the Echo Monster melts away."
    n "Tiny lights float out of the monster one by one."

    echo "Huh...? The strange voices are gone!"
    echo "I finally have my own voice back!"

    mc "What a relief!"
    show ui_ghost intro_happy with Dissolve(0.2)
    ghost "Nice work! You broke the second monster's curse too."

    $ play_scene_music(scene_corridor_music, volume=scene_corridor_volume)
    n "The Echo Monster disappears in a flash of light."

    ghost "There's just one monster left on this floor!"
    mc "Okay! I'll see this through."

    $ cleared_monsters.add((1, 2))
    call progress_autosave from ch1_m2_autosaved
    # Go to ch1_m3_start

    # [Temporary test] Move to the next monster after freeing the second
    jump ch1_m3_start


# ==================================================
# MONSTER 3. Shadow Monster
# ==================================================

label ch1_m3_start:

    # ==========================================
    # SCENE 8. The third monster appears
    # ==========================================

    show apartment corridor_4 behind ui_ghost with fade
    n "A big door stands at the end of the hallway."
    n "Beyond it is an elevator that goes upstairs."

    mc "There it is! Now we can go up!"
    show ui_ghost intro_worried with Dissolve(0.2)
    ghost "Wait! Something feels wrong..."

    n "Just then, a shadow on the floor starts to move."
    $ play_scene_music(scene_battle_music, volume=scene_battle_volume)
    n "It grows bigger and bigger until it turns into a giant monster."

    shadow "Who goes there...? How dare you come this far!"
    show ui_ghost intro_surprised with Dissolve(0.2)
    mc "Whoa! This one's huge!"

    show ui_ghost intro_worried with Dissolve(0.2)
    ghost "That's the last monster on this floor!"
    mc "We have to beat it before we can go upstairs, right?"
    show ui_ghost intro_talk_closed with Dissolve(0.2)
    ghost "That's right! But don't worry."
    ghost "Just do what you've been doing all along."

    # ==========================================
    # SCENE 9. Prepare for the last battle
    # ==========================================

    show ui_ghost intro_explain with Dissolve(0.2)
    ghost "Start with a familiar word again."
    ghost "Then use the practice word to attack the monster!"

    mc "Yep! I know how to do it now!"

    shadow "Then show me what you've got!"

    # --------------------------------------------------
    # TODO Start the third monster battle
    # Show the key word, then the practice word
    # Record speech and analyze pronunciation
    # Successful hits 0/3, monster HP 3
    #
    # Success -> ch1_m3_success_1
    # Failure -> ch1_m3_fail
    # Unrecognized -> ch1_m3_unrecognized
    # --------------------------------------------------

    # [Temporary test] Play three success scenes before battle is implemented
    call ch1_m3_success_1
    call ch1_m3_success_2
    call ch1_m3_success_3

    jump ch1_m3_clear


# --------------------------------------------------
# MONSTER 3. Prompt the player to speak
# --------------------------------------------------

label ch1_m3_prompt:

    show ui_ghost intro_talk with Dissolve(0.2)
    ghost "This is the last monster! Say the word when you're ready!"

    # TODO Practice saying the key word, then the practice word
    # Play the dialogue for the practice word result

    return

# --------------------------------------------------
# MONSTER 3. Battle complete
# --------------------------------------------------

label ch1_m3_clear:

    # ==========================================
    # SCENE 10. Break the last monster's curse
    # ==========================================

    n "The darkness around the Shadow Monster disappears."
    n "The monster shrinks and turns into a soft light."

    shadow "At last... I'm free of the curse."
    mc "Are you okay now?"
    shadow "Yes. Thanks to your voice."

    show ui_ghost intro_happy with Dissolve(0.2)
    ghost "You did it! You helped every monster on this floor!"
    mc "Really? I beat all three?"
    ghost "Yep! Now you know what your voice can do!"

    mc "Yeah! I was scared at first, but now I feel braver!"

    shadow "There is still more to do."
    mc "Huh?"
    shadow "A deeper curse lies asleep on the floors above."
    shadow "You'll see for yourself when you get there..."

    $ play_scene_music(scene_corridor_music, volume=scene_corridor_volume)
    n "With those last words, the Shadow Monster fades into the light."
    n "At the same moment, the elevator doors slide open."

    $ cleared_monsters.add((1, 3))
    call progress_autosave from ch1_m3_autosaved
    # Chapter 1 completion
    # Go to ch1_finish

    # [Temporary test] Go to the Chapter 1 ending after freeing the third monster
    jump ch1_finish


# ==================================================
# CHAPTER 1. Complete
# ==================================================

label ch1_finish:

    # ==========================================
    # SCENE 11. On to the next floor
    # ==========================================

    show apartment elevator_on behind ui_ghost with dissolve
    show ui_ghost intro_talk with Dissolve(0.2)
    n "Our hero and Little Ghost step into the elevator together."
    n "The doors slowly close, and the elevator starts toward the next floor."

    # --------------------------------------------------
    $ completed_chapters.add(1)
    $ unlock_chapter(1)
    $ current_chapter = 2
    call progress_autosave from ch1_completion_autosaved
    # Continue to Chapter 2
    # Go to Chapter 2 after the battle
    # --------------------------------------------------

    call show_chapter_end("images/chapter_end/chapter1.png") from ch1_end_card_done
    hide ui_ghost
    show ui_ghost at ui_ghost_corridor, ui_ghost_settle
    $ stop_scene_music()
    stop sound
    jump chapter2
