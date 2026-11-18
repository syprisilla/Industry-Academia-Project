default success_count = 0
default failure_count = 0
default ui_battle_targets = None
default ui_boss_words = None


label ch1_m1_battle:
    call pronunciation_battle("ch1_m1", "Dust Monster", scene_battle_music, "dust", ui_dust_corridor) from ch1_m1_pronunciation_battle_done
    jump ch1_m1_clear


label pronunciation_battle(monster, monster_name, battle_music, sprite=None, sprite_position=None, core_word=None, target_word=None):
    $ ui_battle_core_word = core_word if core_word is not None else (ui_selected_core_word or ui_saved_core_word())
    $ ui_battle_targets = ui_target_words()
    if monster == "ch3_m3":
        $ ui_boss_words = ui_final_boss_words(ui_battle_targets)
        $ initial_target_word = ui_boss_words[0]
    elif target_word in ui_battle_targets.get(monster, []):
        $ initial_target_word = target_word
    else:
        $ initial_target_word = ui_target_word(monster, ui_battle_targets)
    $ hp_screen = "ui_{}_hp".format(sprite) if sprite else "ui_dust_hp"

label .restart:
    $ success_count = 0
    $ failure_count = 0
    $ ui_battle_training_word = initial_target_word

    if sprite:
        $ renpy.show("ui_{} before".format(sprite), at_list=[sprite_position, ui_dust_idle])

    if hp_screen == "ui_dust_hp":
        show screen ui_dust_hp(monster_name)
    else:
        $ renpy.show_screen(hp_screen)

    while success_count < 3:
        if monster == "ch3_m3":
            if ui_boss_words is None:
                $ ui_boss_words = ui_final_boss_words(ui_target_words())
            $ ui_battle_training_word = ui_boss_words[success_count]

        window hide
        $ play_scene_music(battle_music, volume=scene_battle_volume)
        call screen ui_dust_word(ui_battle_core_word)

        # A recording we couldn't measure is repeated within the same attempt.
        $ ui_battle_result = "unrecognized"
        while ui_battle_result == "unrecognized":
            window hide
            call screen ui_dust_word(ui_battle_training_word, training=True, battle_music=battle_music, monster_name=monster_name, sentence=(monster == "ch3_m3" and success_count == 2))
            $ ui_battle_result = _return
            $ play_scene_music(battle_music, volume=scene_battle_volume)
            if ui_battle_result == "unrecognized":
                window auto
                if sprite and sprite != "dust":
                    call pronunciation_battle_monster_unrecognized from pronunciation_battle_monster_record_again
                else:
                    call ch1_m1_unrecognized from pronunciation_battle_record_again

        if ui_battle_result == "success":
            if sprite:
                # The attack animation counts the hit when the wave lands.
                call expression "ui_{}_light_attack".format(sprite) from pronunciation_battle_monster_hit
            else:
                $ success_count += 1

            window auto
            call expression "{}_success_{}".format(monster, success_count) from pronunciation_battle_success_feedback

        elif ui_battle_result == "fail":
            $ failure_count += 1
            window auto
            if sprite and sprite != "dust":
                call pronunciation_battle_monster_fail from pronunciation_battle_monster_failure_feedback
            else:
                call ch1_m1_fail("unknown", monster) from pronunciation_battle_failure_feedback

            if monster == "ch3_m3":
                if failure_count >= 3:
                    $ renpy.hide_screen(hp_screen)
                    window hide
                    call screen ui_pronunciation_battle_over(True, monster_name=monster_name)
                    if _return is False:
                        jump ch3_m3_failure_ending
                    jump .restart
            elif failure_count >= 3:
                window hide
                call screen ui_pronunciation_battle_over(monster_name=monster_name)
                $ retry_words = ui_retry_target_words(monster, ui_battle_training_word, ui_battle_targets)
                $ ui_battle_training_word = renpy.random.choice(retry_words)
                $ failure_count = 0

    $ renpy.hide_screen(hp_screen)
    window auto
    return
