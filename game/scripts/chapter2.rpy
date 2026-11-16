
# ==================================================
# Chapter 2. Stolen Voices - Second Floor Monsters
# ==================================================

# ==================================================
# MONSTER 1. Whisper Monster
# ==================================================

label chapter2:

    $ current_chapter = 2
    $ play_scene_music(scene_ch2_corridor_music, volume=scene_corridor_volume)

    # ==========================================
    # SCENE 2. The first monster appears
    # ==========================================

    $ play_scene_sound(scene_elevator_sound)
    n "Soft whispers begin to drift through the hall."

    $ play_scene_music(scene_battle_music, volume=scene_battle_volume)
    whisper "Hee hee! A new visitor!"
    mc "Whoa! Another monster!"

    ghost "Watch out! There's some strange magic coming from that monster."
    mc "Is that one cursed too?"
    ghost "I think so. Let's help with the power of our voices!"

    whisper "Think you can beat my whispers?"

    mc "I'll break this curse too!"

    # ==========================================
    # SCENE 3. Prepare for the first battle
    # ==========================================

    ghost "Okay! Let's warm up with a familiar word first."
    ghost "Then say the practice word on the screen!"

    mc "Got it! I'm ready!"

    # --------------------------------------------------
    # TODO Start the first monster battle
    # Show the key word, then the practice word
    # Record speech and analyze pronunciation
    # Successful hits 0/3, monster HP 3
    #
    # One hit -> ch2_m1_success_1
    # Two hits -> ch2_m1_success_2
    # Three hits -> ch2_m1_success_3
    # Failure -> ch2_m1_fail
    # Unrecognized -> ch2_m1_unrecognized
    # --------------------------------------------------

    # [Temporary test] Play three success scenes before battle is implemented
    call ch2_m1_success_1
    call ch2_m1_success_2
    call ch2_m1_success_3

    jump ch2_m1_clear


# --------------------------------------------------
# MONSTER 1. Prompt the player to speak
# --------------------------------------------------

label ch2_m1_prompt:

    ghost "Ready? Say the word on the screen slowly!"

    # TODO Practice saying the key word, then the practice word

    return



# --------------------------------------------------
# MONSTER 1. Battle complete
# --------------------------------------------------

label ch2_m1_clear:

    # ==========================================
    # SCENE 4. Break the first monster's curse
    # ==========================================

    n "The darkness around the Whisper Monster fades."
    n "The strange whispers that filled the hallway fall quiet."

    whisper "Huh...? I can hear my own voice!"
    mc "Really? Are you okay now?"

    whisper "Yes! Someone did this to me."
    whisper "The other monsters are in danger too!"
    whisper "Please help my friends!"

    mc "I will. Count on me!"

    n "The Whisper Monster turns into a tiny light and disappears."
    $ play_scene_music(scene_ch2_corridor_music, volume=scene_corridor_volume)
    n "Something comes rolling down the hall."

    mc "Huh? Is something rolling across the floor?"
    ghost "Let's go see!"

    $ cleared_monsters.add((2, 1))
    call progress_autosave from ch2_m1_autosaved
    # Go to ch2_m2_start

    # [Temporary test] Move to the next monster
    jump ch2_m2_start


# ==================================================
# MONSTER 2. Toy Monster
# ==================================================

label ch2_m2_start:

    # ==========================================
    # SCENE 5. The second monster appears
    # ==========================================

    n "Our hero and Little Ghost follow a little ball as it rolls away."
    n "The ball stops in front of an old toy box by the wall."

    mc "Hey, a toy box!"
    ghost "Something's moving inside it!"

    n "The lid flies open. An old teddy bear and a pile of toys bunch together."
    $ play_scene_music(scene_battle_music, volume=scene_battle_volume)
    n "The toys turn into a big monster that blocks our hero's way."

    mc "Whoa! The toys turned into a monster!"

    ch2_toy "Everyone left me behind! You'll leave too!"
    mc "We're here to help you!"

    ch2_toy "Liar! I don't trust anyone!"

    ghost "Let's break the curse together!"

    mc "Okay! I'll help you!"

    # ==========================================
    # SCENE 6. Prepare for the second battle
    # ==========================================

    ghost "First, warm up your voice with a familiar word."
    ghost "Then say the practice word slowly, just like before!"

    ch2_toy "Stay back! I'll never let you open my box!"

    mc "Don't worry! Your toys are safe with us."

    # --------------------------------------------------
    # TODO Start the second monster battle
    # Show the key word, then the practice word
    # Record speech and analyze pronunciation
    # Successful hits 0/3, monster HP 3
    #
    # One hit -> ch2_m2_success_1
    # Two hits -> ch2_m2_success_2
    # Three hits -> ch2_m2_success_3
    # Failure -> ch2_m2_fail
    # Unrecognized -> ch2_m2_unrecognized
    # --------------------------------------------------

    # [Temporary test] Play three success scenes before battle is implemented
    call ch2_m2_success_1
    call ch2_m2_success_2
    call ch2_m2_success_3

    jump ch2_m2_clear




# --------------------------------------------------
# MONSTER 2. Prompt the player to speak
# --------------------------------------------------

label ch2_m2_prompt:

    ghost "Okay! Say the word on the screen nice and clearly!"

    # TODO Practice saying the key word, then the practice word

    return


# --------------------------------------------------
# MONSTER 2. Battle complete
# --------------------------------------------------

label ch2_m2_clear:

    # ==========================================
    # SCENE 7. Break the second monster's curse
    # ==========================================

    n "The darkness around the Toy Monster drifts away."
    n "The tangled toys settle into place, and the box opens."

    mc "Are you okay now?"

    ch2_toy "Yes... I'm sorry. I've been here all alone for a long time."
    ch2_toy "I thought my owner had forgotten me. It made me so sad."
    ch2_toy "I was scared the other toys would leave too, so I locked them in the box."

    mc "It must have been lonely, being left all by yourself."

    ch2_toy "It was... I'll let my friends out now."
    ch2_toy "Thanks for listening to me!"

    n "The Toy Monster disappears in a warm glow."
    $ play_scene_music(scene_ch2_corridor_music, volume=scene_corridor_volume)
    n "A steady ticking starts at the end of the hall."

    $ cleared_monsters.add((2, 2))
    call progress_autosave from ch2_m2_autosaved
    # Go to ch2_m3_start

    # [Temporary test] Move to the next monster
    jump ch2_m3_start


# ==================================================
# MONSTER 3. Clock Monster
# ==================================================

label ch2_m3_start:

    # ==========================================
    # SCENE 8. The third monster appears
    # ==========================================

    n "Our hero and Little Ghost reach the end of the hallway."
    n "A door with a huge clock on it is shut tight."

    mc "There it is! But the hands aren't moving."
    ghost "You're right. The clock is stuck at the same time!"

    n "Just then, the clock rings with a loud chime."
    $ play_scene_music(scene_battle_music, volume=scene_battle_volume)
    n "The hands spin backward, and the clock turns into a giant monster."

    mc "Whoa! Even the clock turned into a monster!"

    ghost "That's the Clock Monster!"
    ghost "Let's break the curse and ask what happened!"

    mc "Okay! I'll help this one too!"

    # ==========================================
    # SCENE 9. Prepare for the third battle
    # ==========================================

    ghost "This is the last battle on this floor!"
    ghost "Let's warm up your voice with a familiar word."
    ghost "Then say the practice word nice and clearly!"

    mc "Yep! I can do this!"


    # --------------------------------------------------
    # TODO Start the third monster battle
    # Show the key word, then the practice word
    # Record speech and analyze pronunciation
    # Successful hits 0/3, monster HP 3
    #
    # One hit -> ch2_m3_success_1
    # Two hits -> ch2_m3_success_2
    # Three hits -> ch2_m3_success_3
    # Failure -> ch2_m3_fail
    # Unrecognized -> ch2_m3_unrecognized
    # --------------------------------------------------

    # [Temporary test] Play three success scenes before battle is implemented
    call ch2_m3_success_1
    call ch2_m3_success_2
    call ch2_m3_success_3

    jump ch2_m3_clear


# --------------------------------------------------
# MONSTER 3. Prompt the player to speak
# --------------------------------------------------

label ch2_m3_prompt:

    ghost "This is the last monster! Say the word when you're ready!"
    ghost "Take your time and say it clearly!"

    # TODO Practice saying the key word, then the practice word

    return


# --------------------------------------------------
# MONSTER 3. Battle complete
# --------------------------------------------------

label ch2_m3_clear:

    # ==========================================
    # SCENE 10. Break the last monster's curse
    # ==========================================

    n "The darkness around the Clock Monster disappears."
    n "The clock hands slowly start moving again."

    ch2_clock "Thank you. You've helped me come to my senses."

    ghost "You did it! You helped every monster on this floor!"
    mc "I'm so glad!"

    n "The Clock Monster moves aside, and the door swings open."

    ch2_clock "Go through that door and you'll be able to reach the next floor."
    ch2_clock "But be careful. The curse is much stronger up there."

    mc "Got it! I'll make sure to help the others too!"

    n "The Clock Monster says goodbye and disappears into a soft light."
    $ play_scene_music(scene_ch2_corridor_music, volume=scene_corridor_volume)

    ghost "Wow! The door opened!"
    mc "There's an elevator inside!"

    $ cleared_monsters.add((2, 3))
    call progress_autosave from ch2_m3_autosaved
    # Go to ch2_finish

    # [Temporary test] Go to the Chapter 2 ending
    jump ch2_finish


# ==================================================
# CHAPTER 2. Victory ending
# ==================================================

label ch2_finish:

    # ==========================================
    # SCENE 11. On to the next floor
    # ==========================================

    n "Our hero and Little Ghost step into the elevator."
    n "The elevator doors slowly begin to close."

    # --------------------------------------------------
    $ completed_chapters.add(2)
    $ unlock_chapter(2)
    $ current_chapter = 3
    call progress_autosave from ch2_completion_autosaved
    # Continue to Chapter 3
    # --------------------------------------------------

    call show_chapter_end("images/chapter_end/chapter2.png") from ch2_end_card_done
    jump chapter3

