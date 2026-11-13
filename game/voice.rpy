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
        return {"result": result, "feedback": data.get("feedback", ""), "gauges": gauges}

    def do_record(word):
        """녹음 실행 후 screen 변수(ui_voice, ui_record_state)를 설정한다."""
        result = run_voice_engine(word)
        renpy.set_screen_variable("ui_voice", result)
        renpy.set_screen_variable("ui_record_state", "result")
        renpy.restart_interaction()   # 화면 갱신