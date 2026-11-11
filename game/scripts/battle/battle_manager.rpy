label ch1_m1_battle:

    $ success_count = 0

    while success_count < 3:

        # TODO 실제 음성 분석 결과 연결
        $ result = renpy.call_screen("test_pronunciation")

        if result == "success":

            $ success_count += 1

            if success_count == 1:
                call ch1_m1_success_1

            elif success_count == 2:
                call ch1_m1_success_2

            elif success_count == 3:
                call ch1_m1_success_3

        elif result == "fail":

            # TODO 분석 담당자가 실제 오류 원인 전달
            $ reason = "unknown"

            call ch1_m1_fail(reason)

        elif result == "unrecognized":

            call ch1_m1_unrecognized

    jump ch1_m1_clear