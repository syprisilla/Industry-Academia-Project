define intro_recording_sentence = "사자가 숲속에서 사과를 찾았어요."


label start:

    $ renpy.stop_skipping()
    $ play_scene_music(scene_field_music)

    $ player_name = renpy.input("Enter your name.").strip() or player_name
    $ remember_player_name(player_name)

    call progress_autosave from intro_name_autosaved

    jump intro


# --------------------------------------------------
# Character definitions
# Reuse n and mc from scripts/chapter.rpy.
# --------------------------------------------------
define ghost = Character("Little Ghost", color="#B4DFFF")


label intro:

    # Only the dialogue flow can be checked before the features are connected.
    # Dialogue that depends on results is preserved in comments at each TODO.

    # ==========================================
    # SCENE 1. An unfamiliar apartment building
    # ==========================================

    $ play_scene_music(scene_field_music)
    scene apartment field with fade

    n "A cold wind brushes my cheeks. I open my eyes in the middle of a field I've never seen before."
    mc "Where am I...?"
    n "I look around, but there's nobody in sight."
    n "In the distance, the lights are on in an apartment building."
    mc "Maybe someone's in there."
    show apartment exterior with fade
    n "I follow the lights and step inside."

    $ play_scene_music(scene_entrance_music)
    show apartment entrance with fade

    n "Just then, the front door shuts behind me."
    mc "Huh? The door won't open!"

    show ui_ghost intro_idle at ui_ghost_position, ghost_float with dissolve
    # Fade in Little Ghost at the specified size and position.

    n "A little ghost appears in front of me."
    show ui_ghost intro_worried with Dissolve(0.2)
    ghost "You're trapped here too! Monsters have cursed this building."
    mc "How do we get out?"
    show ui_ghost intro_explain with Dissolve(0.2)
    ghost "We have to break the curse on the top floor. But it takes a special power to beat the monsters!"
    mc "A special power? Do I have one?"
    show ui_ghost intro_idea with Dissolve(0.2)
    ghost "Of course! It's hidden in your voice!"

    # ==========================================
    # SCENE 2. Mic check and comparison recording
    # ==========================================

    show apartment lobby behind ui_ghost with dissolve
    show ui_ghost intro_talk_closed with Dissolve(0.2)
    ghost "In this building, your voice has magic. Let's find out what it can do!"
    show ui_ghost intro_talk with Dissolve(0.2)
    ghost "Start by reading this sentence out loud."
    show ui_ghost intro_idle with Dissolve(0.2)
    ghost "Take your time. Read it the way you normally would."

    window hide

    $ intro_recording_sentence = pick_sentence()["text"]
    $ persistent.intro_sentence = intro_recording_sentence   
    $ renpy.music.set_pause(True, channel="music")
    call screen ui_sentence(intro_recording_sentence)
    $ ui_compare_intro = ui_compare_capture_intro(intro_recording_sentence)

    $ renpy.music.set_pause(False, channel="music")
    $ play_scene_music(scene_entrance_music)
    window auto
    # Temporary example for checking the screen.

    # --------------------------------------------------
    # TODO Check the mic and record the initial comparison sentence.
    # Check for a working mic, input volume, and background noise.
    # Show and record the same sentence that will be used for the Final Boss.
    # Store the recording and acoustic analysis results in the database.
    # --------------------------------------------------

    # ==========================================
    # SCENE 3. Initial pronunciation assessment
    # ==========================================

    show ui_ghost intro_happy with Dissolve(0.2)
    ghost "Great! Now let's find out which sounds will help you beat the monsters!"
    show ui_ghost intro_explain with Dissolve(0.2)
    ghost "Say each sound as it appears on the screen!"
    mc "Okay! I'll take it slow."

    window hide

    $ renpy.music.set_pause(True, channel="music")
    call screen ui_s_assessment()
    $ renpy.music.set_pause(False, channel="music")

    $ play_scene_music(scene_entrance_music)
    window auto
    # Show 시, 세, 사, 서, 소, 수, and 스 in order. Finish resumes the word selection dialogue.

    # --------------------------------------------------
    # TODO Assess ㅅ pronunciation.
    # Record 시, 세, 사, 서, 소, 수, and 스 and analyze ㅅ in each one.
    # Group the sounds into clear sounds and sounds that need practice.
    # --------------------------------------------------

    # ==========================================
    # SCENE 4. Choose a key word for paired-stimulus practice
    # ==========================================

    show ui_ghost intro_happy with Dissolve(0.2)
    ghost "We're almost ready to take on the monsters!"
    show ui_ghost intro_curious with Dissolve(0.2)
    ghost "Can you read the words on the screen this time?"

    window hide

    # Key words start with the clearest syllable from the assessment.
    call screen ui_word_selection(
        "Choose a Core Word",
        ui_core_words()
    )

    $ ui_selected_core_word = persistent.ui_core_word = _return

    window auto
    # Done saves the chosen key word in ui_selected_core_word.

    # --------------------------------------------------
    # TODO Choose the key word and practice word.
    # Pick a key word with a clear ㅅ and a practice word with a harder ㅅ.
    # Show separate guidance if no key word can be selected.
    # --------------------------------------------------

    # ==========================================
    # SCENE 5. The elevator powers on
    # ==========================================

    # Once connected, enter this scene only after a key word is selected.

    $ play_scene_sound(scene_elevator_sound)
    show apartment elevator_on behind ui_ghost
    show ui_ghost intro_relief
    with dissolve

    n "When we get our word, the elevator lights up."
    mc "The elevator lit up!"
    show ui_ghost intro_move with Dissolve(0.2)
    ghost "Now we can go upstairs."
    mc "Okay. Let's go together!"

    # --------------------------------------------------
    # TODO Connect to Chapter 1.
    # Go to Chapter 1 after choosing a key word.
    # --------------------------------------------------

    call show_chapter_end("images/chapter_end/intro.png") from intro_end_card_done

    menu:
        "Start Chapter 1":
            jump chapter1

        "Start Chapter 2 (Test)":
            jump chapter2

        "Start Chapter 3 (Test)":
            jump chapter3
