
label chapter3:

    $ current_chapter = 3
    $ play_scene_music(scene_ch3_corridor_music, volume=scene_corridor_volume)

    # ==========================================
    # SCENE 1. Third floor
    # ==========================================

    $ play_scene_sound(scene_elevator_sound)
    n "The elevator stops on the third floor."
    n "The doors open to reveal old letters scattered across the floor."

    show apartment elevator_on_3 behind ui_ghost with fade

    mc "This must be the top floor."

    n "Suddenly, the letters move on their own and turn into a monster."

    jump ch3_m1_start


# ==================================================
# MONSTER 1. Letter Monster
# ==================================================

label ch3_m1_start:

    # ==========================================
    # SCENE 2. The first monster appears
    # ==========================================

    $ play_scene_music(scene_battle_music, volume=scene_battle_volume)
    ch3_letter "Liar! You said you'd come back! Go away, all of you!"
    mc "Who said they'd come back?"

    ghost "Watch out! The curse is making it lash out at us."
    mc "Then let's break the curse first!"

    # ==========================================
    # SCENE 3. Prepare for the first battle
    # ==========================================

    ghost "Warm up with a familiar word, then say the practice word."
    mc "Okay! I'll give it a try!"

    # --------------------------------------------------
    # TODO Start the first monster battle
    # Show the key word, then the practice word, and analyze the recording
    # Successful hits 0/3, monster HP 3
    # Success -> ch3_m1_success_1 ~ ch3_m1_success_3
    # Failure -> ch3_m1_fail
    # Unrecognized -> ch3_m1_unrecognized
    # --------------------------------------------------

    # [Temporary test] Play three success scenes
    call ch3_m1_success_1
    call ch3_m1_success_2
    call ch3_m1_success_3

    jump ch3_m1_clear


label ch3_m1_prompt:

    ghost "Say the word on the screen slowly!"
    # TODO Record and analyze pronunciation

    return


label ch3_m1_clear:

    # ==========================================
    # SCENE 4. Break the first monster's curse
    # ==========================================

    n "The darkness fades from the Letter Monster's body."

    ch3_letter "I wrote letters every day while I waited for Mom to come home."
    ch3_letter "She promised she'd come back... but no matter how long I waited, she never came."
    mc "That's why you couldn't let go of these letters..."
    ch3_letter "Yes... I'll leave this last letter behind and go now. Thank you."

    n "The Letter Monster turns into a tiny light and disappears."
    $ play_scene_music(scene_ch3_corridor_music, volume=scene_corridor_volume)
    n "Farther down the hall, we hear something start to grow."

    ghost "Let's keep going!"

    $ cleared_monsters.add((3, 1))
    call progress_autosave from ch3_m1_autosaved
    jump ch3_m2_start


# ==================================================
# MONSTER 2. Thorny Vine Monster
# ==================================================

label ch3_m2_start:

    # ==========================================
    # SCENE 5. The second monster appears
    # ==========================================

    $ play_scene_music(scene_battle_music, volume=scene_battle_volume)
    n "Thorny vines block the middle of the hallway."
    n "A little flower peeks out between the vines."

    mc "Whoa! Those thorns came out of nowhere!"
    ch3_vine "No! Stay back!"

    ghost "Watch out! The curse is making those thorns grow like crazy."
    mc "That looks dangerous! Let's break the curse, quick!"

    # --------------------------------------------------
    # TODO Start the second monster battle
    # Show the key word, then the practice word, and analyze the recording
    # Successful hits 0/3, monster HP 3
    # Success -> ch3_m2_success_1 ~ ch3_m2_success_3
    # Failure -> ch3_m2_fail
    # Unrecognized -> ch3_m2_unrecognized
    # --------------------------------------------------

    # [Temporary test] Play three success scenes
    call ch3_m2_success_1
    call ch3_m2_success_2
    call ch3_m2_success_3

    jump ch3_m2_clear


label ch3_m2_prompt:

    ghost "When you're ready, say the word on the screen!"
    # TODO Record and analyze pronunciation

    return


label ch3_m2_clear:

    # ==========================================
    # SCENE 7. Break the second monster's curse
    # ==========================================

    n "The thorns disappear and the vines slowly unwind."
    n "Behind the vines, the floor is cracked, with a deep hole in it."

    ch3_vine "A kid came to pick a flower here once and almost fell in."
    mc "Is that why you blocked the way?"
    ch3_vine "Yes... but the curse made me start attacking people."
    ghost "You were trying to keep everyone safe!"

    ch3_vine "The one who started all this is at the end of that hall."
    mc "The one who started it?"
    ch3_vine "The Final Boss. He put a curse on every monster you've met."
    ch3_vine "He's much stronger than the other monsters. Be careful!"
    n "The Thorny Vine Monster turns into a tiny light and disappears."
    $ play_scene_music(scene_ch3_corridor_music, volume=scene_corridor_volume)

    mc "A monster that strong? I'm a little scared."
    ghost "You've done great so far! We'll face him together."
    mc "You're right! I'm going to break that curse!"

    $ cleared_monsters.add((3, 2))
    call progress_autosave from ch3_m2_autosaved
    jump ch3_m3_start



# ==================================================
# MONSTER 3. Final Boss
# ==================================================

label ch3_m3_start:

    # ==========================================
    # SCENE 8. The Final Boss appears
    # ==========================================

    n "We follow the path the vines opened to the end of the hall."
    n "Dark magic seeps out of a huge door."

    mc "The Final Boss is behind that door, right?"
    ghost "Yes... this feels different from anything we've faced."

    n "Just then, the door swings open by itself and a dark shadow appears."

    $ play_scene_music(scene_boss_music, volume=scene_battle_volume)
    ch3_boss "Mwahaha! So you've made it this far!"
    mc "Y-you're the one who cursed all the monsters?"

    ch3_boss "Yes! That was all my doing!"
    ch3_boss "Their sadness and fear made me stronger!"

    mc "Do you know how much you hurt them?!"
    ch3_boss "Hmph! Why should I care?"

    ghost "We can't let you hurt any more monsters!"
    mc "That's right! We're going to break your curse!"

    ch3_boss "Ha ha ha! Come and try!"

    # ==========================================
    # SCENE 9. Prepare for the Final Boss battle
    # ==========================================

    n "The Final Boss holds up a black orb, and the room grows dark."

    ghost "I can feel a powerful curse coming from that orb!"
    ghost "Use the power of your voice, just like we practiced!"

    mc "Okay! I can do this!"

    ch3_boss "You think your tiny power can beat me?"

    call pronunciation_battle("ch3_m3", "Final Boss", scene_boss_music) from ch3_m3_pronunciation_battle_done
    jump ch3_m3_clear


label ch3_m3_failure_ending:

    window auto
    n "The light from your voice slowly fades away."
    ch3_boss "Ha ha ha! My curse is still too strong!"
    mc "Oh no... I couldn't break the curse."
    ghost "It's okay! You've come so far. We can always try again!"
    n "The curse remains... but the adventure isn't over yet."

    call show_chapter_end("images/chapter_end/final_boss_defeat.png") from ch3_m3_defeat_card_done
    $ renpy.full_restart(config.game_main_transition, save=False)


# --------------------------------------------------
# Final Boss Prompt the player to speak
# --------------------------------------------------

label ch3_m3_prompt:

    ghost "This is the last battle! Say the word on the screen!"

    # TODO Practice saying the key word, then the practice word

    return


# --------------------------------------------------
# Final Boss Battle complete
# --------------------------------------------------

label ch3_m3_clear:

    # ==========================================
    # SCENE 10. The Final Boss disappears
    # ==========================================

    n "The black orb shatters, and the darkness vanishes."

    ch3_boss "Impossible... you broke my curse!"
    mc "You can't hurt the monsters anymore!"

    ch3_boss "Aaaah! My power is fading!"

    n "The one who cast the curse vanishes in a puff of black smoke."
    $ play_scene_music(scene_ending_music)
    n "At the same moment, the darkness lifts from the whole building."

    ghost "We did it! Every curse is finally broken!"
    mc "Really? Is everyone okay now?"

    $ cleared_monsters.add((3, 3))
    call progress_autosave from ch3_m3_autosaved
    jump ch3_finish


# ==================================================
# CHAPTER 3. Final victory ending
# ==================================================

label ch3_finish:

    # ==========================================
    # SCENE 11. The truth about the voice
    # ==========================================

    n "With the Final Boss gone, a warm light spreads through the whole building."
    n "Just then, familiar voices ring out."

    dust "Wow! All the curses are finally broken!"
    echo "Thank you so much! You did it!"
    shadow "You saved us all."
    whisper "I'm not scared anymore either! Thank you so much!"

    mc "Hey! You're the monsters we helped!"

    ch2_toy "Thanks to you, I can play with my friends again!"
    ch2_clock "And I can get time moving again!"

    ch3_letter "I think I'm ready to say goodbye now."
    ch3_vine "I'm so glad everyone's safe!"

    ghost "Wow! All the friends we helped are here!"

    n "The monsters beam at our hero."

    mc "I'm so glad you're all okay!"

    ghost "The power of your voice saved everyone!"
    mc "I couldn't have done it alone. You helped me!"

    ghost "Hee hee! We made a great team, didn't we?"

    n "The monsters wave goodbye to our hero."
    n "One by one, the monsters disappear in a warm glow."

    mc "Bye, everyone! I hope you'll be happy!"
    ghost "Let's head back too!"

    n "And so ends the adventure of our hero and Little Ghost."

    $ completed_chapters.add(3)
    $ unlock_chapter(3)
    call progress_autosave from ch3_completion_autosaved
    call show_chapter_end("images/chapter_end/final_boss_cleared.png") from ch3_end_card_done
    $ renpy.full_restart(config.game_main_transition, save=False)
