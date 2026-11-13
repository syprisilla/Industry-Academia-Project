init python:
    import subprocess, json, os

    def run_voice_engine(word, seconds=3):
        """voice_engine.exe 로 녹음·분석 후 word.json 을 읽어 결과 dict 반환.
        반환: {"result": "success"/"fail"/"unrecognized", "feedback": str, "gauges": {feature: path}}
        """
        gamedir = renpy.config.gamedir
        exe = os.path.join(gamedir, "python", "voice_engine", "voice_engine.exe")
        word_json = os.path.join(gamedir, "data", "word.json")

        fail = {"result": "unrecognized", "feedback": "소리를 잘 듣지 못했어요. 다시 말해 볼까요?", "gauges": {}}

        try:
            subprocess.run([exe, "try", word, str(seconds)],
                           check=True, capture_output=True,
                           creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0))
        except Exception as e:
            renpy.log("voice_engine 실행 실패: %r" % e)
            return fail

        try:
            with open(word_json, encoding="utf-8") as f:
                data = json.load(f)
        except Exception as e:
            renpy.log("word.json 읽기 실패: %r" % e)
            return fail

        if data.get("status") != "ok":
            return fail

        result = "success" if data.get("success") else "fail"
        # out 폴더의 게이지 PNG 절대경로 (고정 파일명)
        out_dir = os.path.join(gamedir, "data", "out")
        gauges = {
            "cog_hz": os.path.join(out_dir, "gauge_cog_hz.png").replace("\\", "/"),
            "sd_hz": os.path.join(out_dir, "gauge_sd_hz.png").replace("\\", "/"),
        }
        # 캐시 우회: 바뀐 PNG 를 다시 읽도록 이미지 캐시 비우기
        renpy.free_memory()
        return {"result": result, "feedback": data.get("feedback", ""), "gauges": gauges,
                "segment_estimated": data.get("segment_estimated", False)}

    def do_record(word):
        """녹음 실행 후 screen 변수(ui_voice, ui_record_state)를 설정한다."""
        result = run_voice_engine(word)
        renpy.set_screen_variable("ui_voice", result)
        renpy.set_screen_variable("ui_record_state", "result")
        renpy.restart_interaction()   # 화면 갱신


    def do_syll_record(syllable, order, seconds=3):
        """음절 하나 녹음·분석 → syllable_data.json 누적. 성공 여부를 screen 변수로."""
        gamedir = renpy.config.gamedir
        exe = os.path.join(gamedir, "python", "voice_engine", "voice_engine.exe")
        try:
            subprocess.run([exe, "syll-record", syllable, str(order), str(seconds)],
                           check=True, capture_output=True,
                           creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0))
            renpy.set_screen_variable("syll_state", "done")
        except Exception as e:
            renpy.log("syll-record 실패: %r" % e)
            renpy.set_screen_variable("syll_state", "done")   # 실패해도 넘어가게(해당 글자는 선정서 제외됨)
        renpy.restart_interaction()

    def do_syll_select():
        """7개에서 최고 선정 → syllable_result.json 읽어 screen 변수에 저장."""
        gamedir = renpy.config.gamedir
        exe = os.path.join(gamedir, "python", "voice_engine", "voice_engine.exe")
        result_json = os.path.join(gamedir, "data", "syllable_result.json")
        fail = {"status": "no_candidate", "selected": None, "image": ""}
        try:
            subprocess.run([exe, "syll-select"],
                           check=True, capture_output=True,
                           creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0))
        except Exception as e:
            renpy.log("syll-select 실패: %r" % e)
            renpy.set_screen_variable("syll_result", fail)
            renpy.restart_interaction()
            return
        try:
            with open(result_json, encoding="utf-8") as f:
                data = json.load(f)
            if "image" in data:
                data["image"] = data["image"].replace("\\", "/")
            renpy.set_screen_variable("syll_result", data)
        except Exception as e:
            renpy.log("syllable_result.json 읽기 실패: %r" % e)
            renpy.set_screen_variable("syll_result", fail)
        renpy.free_memory()   # 선정 글자 이미지 캐시 우회
        renpy.restart_interaction()