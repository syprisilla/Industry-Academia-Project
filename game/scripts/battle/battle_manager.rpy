label ch1_m1_battle:

    $ success_count = 0

    # 임시 핵심단어: 이후 평가/단어 선정 기능과 연결
    $ ui_battle_core_word = "사과"

    # 인트로에서 선택한 훈련단어 사용
    $ ui_battle_training_word = ui_selected_training_word or "수박"

    # 데모에서는 두 단어가 겹치지 않도록 처리
    if ui_battle_training_word == ui_battle_core_word:
        $ ui_battle_core_word = "사자"

    show screen ui_dust_hp

    while success_count < 3:

        window hide

        # 1. 핵심단어로 준비
        call screen ui_dust_word(ui_battle_core_word)

        # 2. 훈련단어로 공격 시도
        call screen ui_dust_word(ui_battle_training_word, training=True)
        $ ui_battle_result = _return

        if ui_battle_result == "success":

            # 음파가 명중하면 피격 모습과 HP를 갱신한다.
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

    # 기존 정화 장면으로 이동
    jump ch1_m1_clear