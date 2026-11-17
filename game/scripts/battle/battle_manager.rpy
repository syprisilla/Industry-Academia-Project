label ch1_m1_battle:

    $ success_count = 0

    # Use the key word picked in the intro
    $ ui_battle_core_word = ui_selected_core_word or "사과"

    # Temporary practice word until worst-syllable target words are connected
    $ ui_battle_training_word = ui_selected_training_word or "수박"

    # Keep the two words distinct in the demo
    if ui_battle_training_word == ui_battle_core_word:
        $ ui_battle_core_word = "사자"

    show screen ui_dust_hp

    while success_count < 3:

        window hide

        # 1. Warm up with the key word
        $ play_scene_music(scene_battle_music, volume=scene_battle_volume)
        call screen ui_dust_word(ui_battle_core_word)

        # 2. Try attacking with the practice word
        call screen ui_dust_word(ui_battle_training_word, training=True)
        $ ui_battle_result = _return
        $ play_scene_music(scene_battle_music, volume=scene_battle_volume)

        if ui_battle_result == "success":

            # Update the hit pose and HP when the sound wave lands.
            call ui_dust_light_attack

            window auto

            if success_count == 1:
                call ch1_m1_success_1

            elif success_count == 2:
                call ch1_m1_success_2

            else:
                call ch1_m1_success_3

        elif ui_battle_result == "fail":

            window auto
            call ch1_m1_fail("unknown")

        else:

            window auto
            call ch1_m1_unrecognized

    hide screen ui_dust_hp

    window auto

    # Continue to the existing curse-breaking scene
    jump ch1_m1_clear
