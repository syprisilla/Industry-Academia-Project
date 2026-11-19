# ==================================================
# 결과 화면: 발음 훈련 기록 요약
#
# 데이터: persistent.play_events (play_records.rpy 에서 저장)
#   (시간, 괴물 이름, 결과, 단어, 테스트 여부)
#   결과 = "success" / "fail" / "unrecognized" / "retry"
#
# 사용
#   - 엔딩 후:  call screen ui_results_screen()
#   - 단독:     ShowMenu("ui_results_menu")
# ==================================================


# 괴물 표시 순서
define ui_results_monsters = [
    "Dust Monster", "Echo Monster", "Shadow Monster",
    "Whisper Monster", "Toy Monster", "Clock Monster",
    "Letter Monster", "Thorny Vine Monster", "Final Boss",
]


init python:

    import time as _ui_time

    def ui_results_events(scope="today", include_test=False):
        """조건에 맞는 기록을 시간 순서대로 반환"""
        events = sorted((persistent.play_events or {}).values(), key=lambda e: e[0])

        if not include_test:
            events = [e for e in events if not e[4]]

        if scope == "today":
            now = _ui_time.localtime()
            midnight = _ui_time.mktime((now.tm_year, now.tm_mon, now.tm_mday, 0, 0, 0, 0, 0, -1))
            events = [e for e in events if e[0] >= midnight]

        return events

    def ui_results_stats(scope="today", include_test=False):
        """화면에 보여 줄 숫자 계산"""
        events = ui_results_events(scope, include_test)

        success = fail = no_reading = first_try = 0
        words = {}
        monsters = {}

        # 첫 시도 성공: 새 세트의 첫 시도에서 바로 성공한 경우
        # (전투 시작, 재도전, 직전 성공 후에 시작되는 시도가 새 세트)
        fresh = {}

        for timestamp, monster, result, word, is_test in events:

            m = monsters.setdefault(monster, {"success": 0, "fail": 0})

            if result == "retry":
                fresh[monster] = True
                continue

            if result == "unrecognized":
                no_reading += 1
                continue

            if result == "success":
                success += 1
                m["success"] += 1
                if fresh.get(monster, True):
                    first_try += 1
                fresh[monster] = True

            elif result == "fail":
                fail += 1
                m["fail"] += 1
                fresh[monster] = False

            else:
                continue

            if word:
                w = words.setdefault(word, {"success": 0, "total": 0})
                w["total"] += 1
                if result == "success":
                    w["success"] += 1

        attempts = success + fail

        word_rows = sorted(words.items(), key=lambda item: (-item[1]["total"], item[0]))

        return {
            "attempts": attempts,
            "success": success,
            "fail": fail,
            "no_reading": no_reading,
            "success_rate": (100.0 * success / attempts) if attempts else None,
            "first_try_rate": (100.0 * first_try / success) if success else None,
            "avg_retries": (1.0 * fail / success) if success else None,
            "purified": len(persistent.play_cleared_monsters or ()),
            "words": word_rows,
            "monsters": monsters,
        }

    def ui_results_short(word, limit=6):
        """긴 문장(최종 보스)은 앞부분만 표시"""
        return word if len(word) <= limit else word[:limit] + "..."

    def ui_results_percent(value):
        return "-" if value is None else "{:.0f}%".format(value)

    def ui_results_number(value):
        return "-" if value is None else "{:.1f}".format(value)


# --------------------------------------------------
# 스타일
# --------------------------------------------------

style ui_results_big is intro_ch1_text:
    size 64
    bold True
    color "#FFF2C7"

style ui_results_small is intro_ch1_caption:
    size 26
    text_align 0.0


# --------------------------------------------------
# 숫자 카드 하나
# --------------------------------------------------

screen ui_results_tile(title, value, note=""):
    fixed:
        xysize (318, 190)

        add intro_ch1_ui + "panel_hp.png" xysize (318, 190) fit "fill" alpha 0.92

        vbox:
            align (0.5, 0.5)
            spacing 2

            text title style "intro_ch1_caption" size 26 xalign 0.5
            text value style "ui_results_big" xalign 0.5
            if note:
                text note style "intro_ch1_caption" size 20 xalign 0.5 color "#BDB1CD"


# --------------------------------------------------
# 가로 막대 (성공률 표시)
# --------------------------------------------------

screen ui_results_bar(rate, width=300):
    fixed:
        xysize (width, 22)
        add Solid("#2A2A4A") xysize (width, 22)
        if rate:
            add Solid("#7FD8B3") xysize (max(4, int(width * rate / 100.0)), 22)


# --------------------------------------------------
# 결과 내용 (엔딩 화면과 메뉴 화면이 함께 사용)
# --------------------------------------------------

# 이 화면은 다른 화면 안에 use 로 들어가므로 SetLocalVariable 을 사용
screen ui_results_content():

    default scope = "today"
    default include_test = False

    $ stats = ui_results_stats(scope, include_test)

    vbox:
        spacing 26

        # 보기 범위 선택
        hbox:
            spacing 14
            use intro_ch1_button("Today", ("success" if scope == "today" else "next"),
                SetLocalVariable("scope", "today"), width=200, height=60)
            use intro_ch1_button("All Time", ("success" if scope == "all" else "next"),
                SetLocalVariable("scope", "all"), width=200, height=60)
            null width 40
            use intro_ch1_button(("Test Plays: On" if include_test else "Test Plays: Off"),
                ("unrecognized" if include_test else "next"),
                SetLocalVariable("include_test", not include_test), width=270, height=60)

        if stats["attempts"] == 0:

            fixed:
                xysize (1370, 560)
                add intro_ch1_ui + "panel_assessment.png" xysize (1370, 560) fit "fill" alpha 0.92
                vbox:
                    align (0.5, 0.5)
                    spacing 16
                    text "No practice records yet." style "intro_ch1_text" size 44 xalign 0.5
                    text "Records appear here after you practice words in battle." style "intro_ch1_caption" xalign 0.5

        else:

            # 숫자 카드 4개
            hbox:
                spacing 32
                use ui_results_tile("Success Rate", ui_results_percent(stats["success_rate"]),
                    "{} of {} tries".format(stats["success"], stats["attempts"]))
                use ui_results_tile("First-Try Success", ui_results_percent(stats["first_try_rate"]),
                    "succeeded on the first try")
                use ui_results_tile("Avg. Retries", ui_results_number(stats["avg_retries"]),
                    "tries before each success")
                use ui_results_tile("Monsters Purified", "{} / 9".format(min(stats["purified"], 9)),
                    "all-time progress")

            hbox:
                spacing 30

                # 단어별 성공률
                use ui_settings_card("By Word", w=670, h=520):

                    if stats["words"]:
                        for word, w in stats["words"][:6]:
                            $ rate = 100.0 * w["success"] / w["total"]
                            hbox:
                                spacing 18
                                text ui_results_short(word) style "intro_ch1_text" size 30 xsize 150 text_align 0.0 yalign 0.5
                                use ui_results_bar(rate, 260)
                                text "{:.0f}% ({}/{})".format(rate, w["success"], w["total"]):
                                    style "ui_results_small"
                                    yalign 0.5
                    else:
                        text "No word records." style "ui_results_small"

                # 괴물별 결과
                use ui_settings_card("By Monster", w=670, h=520):

                    $ rows = [m for m in ui_results_monsters if m in stats["monsters"]]

                    for monster in rows[:9]:
                        $ m = stats["monsters"][monster]
                        hbox:
                            spacing 18
                            text monster style "ui_results_small" xsize 290 yalign 0.5
                            text "Success {}".format(m["success"]) style "ui_results_small" color "#7FD8B3" xsize 150
                            text "Failed {}".format(m["fail"]) style "ui_results_small" color "#F4A7B9"


# --------------------------------------------------
# 엔딩 후 보여 주는 결과 화면 (전체 화면)
# --------------------------------------------------

screen ui_results_screen():

    modal True

    add "apartment boss_room_bright"
    add Solid("#0B0618AA")

    text "My Training Results" style "intro_ch1_text":
        xpos 275
        ypos 40
        size 64
        bold True
        outlines [(3, "#0C1530", 0, 2)]

    fixed:
        xpos 275
        ypos 145
        xysize (1370, 830)
        use ui_results_content

    fixed:
        xysize (260, 72)
        pos (1385, 990)
        use intro_ch1_button("Continue", "continue", Return(), width=260, height=72)


# --------------------------------------------------
# 메뉴에서 여는 결과 화면 (Play Records 처럼 게임 메뉴 안에 표시)
# --------------------------------------------------

screen ui_results_menu():

    tag menu

    use game_menu(_("My Results")):
        use ui_results_content
