# ==================================================
# Chapter 3
# ==================================================

label chapter3:

    $ current_chapter = 3

    $ play_scene_music(scene_ch3_corridor_music, volume=scene_corridor_volume)

    scene apartment elevator_on_3
    show ui_ghost intro_idle at ui_ghost_corridor, ghost_float
    with fade

    $ play_scene_sound(scene_elevator_sound)

    n "The elevator stops on the third floor."

    # 엘리베이터에서 나와 복도로 이동
    show apartment corridor_2 behind ui_ghost with fade

    show ui_letter_scattered at ui_letter_scattered_position with dissolve

    n "The doors open to reveal old letters scattered across the floor."

    mc "This must be the top floor."

    # 흩어진 편지가 모이며 괴물 등장
    window hide

    show ui_letter_scattered at ui_letter_scattered_position, ui_letter_gather
    show ui_letter before at ui_letter_position, ui_dust_emerge

    pause 0.7

    hide ui_letter_scattered

    window auto

    show ui_ghost intro_surprised with Dissolve(0.2)

    n "Suddenly, the letters move on their own and turn into a monster."

    jump ch3_m1_start


# ==================================================
# MONSTER 1. Letter Monster
# ==================================================

label ch3_m1_start:

    $ play_scene_music(scene_battle_music, volume=scene_battle_volume)

    show ui_letter angry at ui_letter_position, ui_dust_threaten with Dissolve(0.16)

    ch3_letter "Liar! You said you'd come back! Go away, all of you!"

    show ui_letter before at ui_letter_position, ui_dust_idle with Dissolve(0.16)

    mc "Who said they'd come back?"

    show ui_ghost intro_worried with Dissolve(0.2)
    ghost "Watch out! The curse is making it lash out at us."

    mc "Then let's break the curse first!"

    show ui_ghost intro_explain with Dissolve(0.2)
    ghost "Warm up with a familiar word, then say the practice word."

    mc "Okay! I'll give it a try!"

    # 기존 공통 전투로 이동
    jump ch3_m1_battle


label ch3_m1_prompt:

    show ui_ghost intro_talk with Dissolve(0.2)
    ghost "Say the word on the screen slowly!"

    return


# ==================================================
# 편지 괴물 정화 완료
# ==================================================

label ch3_m1_clear:

    n "The darkness fades from the Letter Monster's body."

    call ui_letter_purification from ch3_m1_letter_purification_done

    show ui_letter after_sad at ui_letter_position, ui_dust_idle with Dissolve(0.2)
    show ui_ghost intro_relief with Dissolve(0.2)

    ch3_letter "I wrote letters every day while I waited for Mom to come home."
    ch3_letter "She promised she'd come back... but no matter how long I waited, she never came."

    show ui_ghost intro_sad with Dissolve(0.2)
    mc "That's why you couldn't let go of these letters..."

    show ui_letter after at ui_letter_position, ui_dust_idle with Dissolve(0.3)

    ch3_letter "Yes... I'll leave this last letter behind and go now. Thank you."
    show ui_ghost intro_idle with Dissolve(0.2)
    show ui_letter_last at ui_letter_last_position with Dissolve(0.3)

    hide ui_letter_scattered
    hide screen ui_letter_hp

    n "The Letter Monster turns into a tiny light and disappears."

    # 위 내레이션을 넘기면 바로 화면에서 제거
    hide ui_letter
    hide ui_letter_last
    with Dissolve(0.3)

    $ play_scene_music(scene_ch3_corridor_music, volume=scene_corridor_volume)

    n "Farther down the hall, we hear something start to grow."

    show ui_ghost intro_talk_closed with Dissolve(0.2)
    ghost "Let's keep going!"

    $ cleared_monsters.add((3, 1))
    call progress_autosave from ch3_m1_autosaved

    jump ch3_m2_start


# ==================================================
# MONSTER 2. Thorny Vine Monster
# ==================================================

label ch3_m2_start:

    # 이전 장면의 편지 이미지 정리
    hide ui_letter
    hide ui_letter_last
    hide ui_letter_scattered
    hide screen ui_letter_hp

    show apartment corridor_3 behind ui_ghost with fade

    $ play_scene_music(scene_battle_music, volume=scene_battle_volume)

    show ui_vine before at ui_vine_position, ui_dust_emerge

    n "Thorny vines block the middle of the hallway."
    n "A little flower peeks out between the vines."

    mc "Whoa! Those thorns came out of nowhere!"

    show ui_vine angry at ui_vine_position, ui_dust_threaten with Dissolve(0.16)
    ch3_vine "No! Stay back!"

    show ui_vine before at ui_vine_position, ui_dust_idle with Dissolve(0.16)
    show ui_ghost intro_worried with Dissolve(0.2)

    ghost "Watch out! The curse is making those thorns grow like crazy."
    mc "That looks dangerous! Let's break the curse, quick!"

    jump ch3_m2_battle


label ch3_m2_prompt:

    show ui_ghost intro_talk with Dissolve(0.2)
    ghost "When you're ready, say the word on the screen!"

    return


label ch3_m2_clear:

    n "The thorns disappear and the vines slowly unwind."

    call ui_vine_purification from ch3_m2_vine_purification_done

    n "Behind the vines, the floor is cracked, with a deep hole in it."

    show ui_ghost intro_relief with Dissolve(0.2)

    ch3_vine "A kid came to pick a flower here once and almost fell in."
    mc "Is that why you blocked the way?"
    ch3_vine "Yes... but the curse made me start attacking people."

    show ui_ghost intro_explain with Dissolve(0.2)
    ghost "You were trying to keep everyone safe!"

    ch3_vine "The one who started all this is at the end of that hall."
    mc "The one who started it?"

    show ui_vine after_worried at ui_vine_position, ui_dust_idle with Dissolve(0.2)

    ch3_vine "The Final Boss. He put a curse on every monster you've met."
    ch3_vine "He's much stronger than the other monsters. Be careful!"

    n "The Thorny Vine Monster turns into a tiny light and disappears."

    hide ui_vine with Dissolve(0.5)
    hide screen ui_vine_hp

    $ play_scene_music(scene_ch3_corridor_music, volume=scene_corridor_volume)

    mc "A monster that strong? I'm a little scared."

    show ui_ghost intro_encourage with Dissolve(0.2)
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

    # 덩굴이 열어 준 길 끝의 큰 문
    show apartment boss_door behind ui_ghost with fade
    show ui_ghost intro_idle with Dissolve(0.2)

    n "We follow the path the vines opened to the end of the hall."
    n "Dark magic seeps out of a huge door."

    mc "The Final Boss is behind that door, right?"
    show ui_ghost intro_worried with Dissolve(0.2)
    ghost "Yes... this feels different from anything we've faced."

    n "Just then, the door swings open by itself and a dark shadow appears."

    # 문이 열리고 보스 등장
    $ play_scene_music(scene_boss_music, volume=scene_battle_volume)
    window hide
    show apartment boss_room behind ui_ghost with fade
    show ui_boss before at ui_boss_position, ui_boss_emerge
    show ui_ghost intro_surprised with Dissolve(0.2)
    pause 0.9
    window auto

    show ui_boss laugh at ui_boss_position, ui_dust_idle with Dissolve(0.16)
    ch3_boss "Mwahaha! So you've made it this far!"
    mc "Y-you're the one who cursed all the monsters?"

    show ui_boss talk at ui_boss_position, ui_dust_idle with Dissolve(0.16)
    ch3_boss "Yes! That was all my doing!"
    ch3_boss "Their sadness and fear made me stronger!"

    mc "Do you know how much you hurt them?!"
    show ui_boss angry at ui_boss_position, ui_boss_threaten with Dissolve(0.16)
    ch3_boss "Hmph! Why should I care?"

    show ui_ghost intro_determined with Dissolve(0.2)
    ghost "We can't let you hurt any more monsters!"
    mc "That's right! We're going to break your curse!"

    show ui_boss laugh at ui_boss_position, ui_dust_idle with Dissolve(0.16)
    ch3_boss "Ha ha ha! Come and try!"

    # ==========================================
    # SCENE 9. Prepare for the Final Boss battle
    # ==========================================

    # 검은 구슬을 들자 방이 어두워짐
    show ui_boss orb at ui_boss_orb_position, ui_boss_threaten with Dissolve(0.2)
    show ui_boss_darkness behind ui_ghost, ui_boss at ui_boss_darkness_fade

    n "The Final Boss holds up a black orb, and the room grows dark."

    show ui_ghost intro_worried with Dissolve(0.2)
    ghost "I can feel a powerful curse coming from that orb!"
    show ui_ghost intro_explain with Dissolve(0.2)
    ghost "Use the power of your voice, just like we practiced!"

    mc "Okay! I can do this!"

    show ui_boss laugh at ui_boss_position, ui_dust_idle with Dissolve(0.16)
    ch3_boss "You think your tiny power can beat me?"

    show ui_ghost intro_idle with Dissolve(0.2)

    # 기존 공통 전투로 이동
    jump ch3_m3_battle


label ch3_m3_failure_ending:

    window hide

    # 어떤 경로로 들어와도 보스 장면이 보이도록 다시 세움
    show apartment boss_room behind ui_ghost
    show ui_boss_darkness behind ui_ghost
    show ui_ghost intro_worried at ui_ghost_corridor, ghost_float
    show ui_boss laugh at ui_boss_position, ui_boss_threaten
    with Dissolve(0.3)

    window auto
    n "The light from your voice slowly fades away."
    ch3_boss "Ha ha ha! My curse is still too strong!"
    show ui_ghost intro_sad with Dissolve(0.2)
    mc "Oh no... I couldn't break the curse."
    show ui_ghost intro_encourage with Dissolve(0.2)
    ghost "It's okay! You've come so far. We can always try again!"
    n "The curse remains... but the adventure isn't over yet."

    call show_chapter_end("images/chapter_end/final_boss_defeat.png") from ch3_m3_defeat_card_done
    # 이번 훈련 결과 보여 주기
    window hide
    call screen ui_results_screen()
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

    # 구슬이 깨지고 보스가 검은 연기처럼 사라짐
    call ui_boss_purification from ch3_m3_boss_purification_done

    n "The one who cast the curse vanishes in a puff of black smoke."
    $ play_scene_music(scene_ending_music)

    # 건물 전체의 어둠이 걷힘
    hide ui_boss_darkness with Dissolve(1.0)

    n "At the same moment, the darkness lifts from the whole building."

    show ui_ghost intro_happy with Dissolve(0.2)
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

    # 따뜻한 빛이 퍼지며 방이 밝아짐
    call ui_ending_light from ch3_ending_light_done

    n "With the Final Boss gone, a warm light spreads through the whole building."

    show ui_ghost intro_surprised with Dissolve(0.2)
    n "Just then, familiar voices ring out."

    # 정화된 괴물들이 한 마리씩 나타남
    $ ui_ending_show("dust")
    dust "Wow! All the curses are finally broken!"

    $ ui_ending_show("echo")
    echo "Thank you so much! You did it!"

    $ ui_ending_show("shadow")
    shadow "You saved us all."

    $ ui_ending_show("whisper")
    whisper "I'm not scared anymore either! Thank you so much!"

    show ui_ghost intro_happy with Dissolve(0.2)
    mc "Hey! You're the monsters we helped!"

    $ ui_ending_show("toy")
    ch2_toy "Thanks to you, I can play with my friends again!"

    $ ui_ending_show("clock")
    ch2_clock "And I can get time moving again!"

    $ ui_ending_show("letter")
    ch3_letter "I think I'm ready to say goodbye now."

    $ ui_ending_show("vine")
    ch3_vine "I'm so glad everyone's safe!"

    show ui_ghost intro_react with Dissolve(0.2)
    ghost "Wow! All the friends we helped are here!"

    # 다 같이 기뻐하기
    call ui_ending_cheer from ch3_ending_cheer_done
    n "The monsters beam at our hero."

    mc "I'm so glad you're all okay!"

    show ui_ghost intro_encourage with Dissolve(0.2)
    ghost "The power of your voice saved everyone!"
    mc "I couldn't have done it alone. You helped me!"

    show ui_ghost intro_happy with Dissolve(0.2)
    ghost "Hee hee! We made a great team, didn't we?"

    # 다 같이 손 흔들며 인사
    call ui_ending_goodbye from ch3_ending_goodbye_done
    n "The monsters wave goodbye to our hero."

    # 한 마리씩 빛이 되어 사라짐
    call ui_ending_farewell from ch3_ending_farewell_done
    n "One by one, the monsters disappear in a warm glow."

    show ui_ghost intro_relief with Dissolve(0.2)
    mc "Bye, everyone! I hope you'll be happy!"

    show ui_ghost intro_talk with Dissolve(0.2)
    ghost "Let's head back too!"

    n "And so ends the adventure of our hero and Little Ghost."

    $ completed_chapters.add(3)
    $ unlock_chapter(3)
    call progress_autosave from ch3_completion_autosaved
    call show_chapter_end("images/chapter_end/final_boss_cleared.png") from ch3_end_card_done
    # 이번 훈련 결과 보여 주기
    window hide
    call screen ui_results_screen()
    $ renpy.full_restart(config.game_main_transition, save=False)