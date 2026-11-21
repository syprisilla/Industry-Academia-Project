init python:
    import subprocess, json, os

    def run_voice_engine(word, seconds=3):
        """Record and analyze with voice_engine.exe, then read word.json.
        Returns {"result": "success"/"fail"/"unrecognized", "feedback": str, "gauges": {feature: path}}.
        """
        gamedir = renpy.config.gamedir
        exe = os.path.join(gamedir, "python", "voice_engine", "voice_engine.exe")
        word_json = os.path.join(gamedir, "data", "word.json")

        fail = {"result": "unrecognized", "feedback": "We couldn't hear you clearly. Want to try again?", "gauges": {}}

        try:
            subprocess.run([exe, "try", word, str(seconds)],
                           check=True, capture_output=True,
                           creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0))
        except Exception as e:
            renpy.log("Could not run voice_engine: %r" % e)
            return fail

        try:
            with open(word_json, encoding="utf-8") as f:
                data = json.load(f)
        except Exception as e:
            renpy.log("Could not read word.json: %r" % e)
            return fail

        if data.get("status") != "ok":
            # Pass the cause (too_quiet/clipping/no_device) to the mic help screen.
            ui_unrec_set_kind(data.get("reason") or data.get("status"))
            return fail

        result = "success" if data.get("success") else "fail"
        # Absolute paths to the fixed gauge filenames in the out folder.
        out_dir = os.path.join(gamedir, "data", "out")
        gauges = {
            "cog_hz": os.path.join(out_dir, "gauge_cog_hz.png").replace("\\", "/"),
            "sd_hz": os.path.join(out_dir, "gauge_sd_hz.png").replace("\\", "/"),
        }
        # Clear cached images so the updated PNGs are loaded.
        renpy.free_memory()
        return {"result": result, "feedback": data.get("feedback", ""), "gauges": gauges,
                "segment_estimated": data.get("segment_estimated", False)}

    def do_record(word):
        """Legacy recording handler that sets ui_voice and ui_record_state."""
        result = run_voice_engine(word)
        renpy.set_screen_variable("ui_voice", result)
        renpy.set_screen_variable("ui_record_state", "result")
        renpy.restart_interaction()   # Refresh the screen.




    def do_syll_record(syllable, order, seconds=3):
        """Record and analyze one sound, append to syllable_data.json, and set the screen state."""
        gamedir = renpy.config.gamedir
        exe = os.path.join(gamedir, "python", "voice_engine", "voice_engine.exe")
        try:
            subprocess.run([exe, "syll-record", syllable, str(order), str(seconds)],
                           check=True, capture_output=True,
                           creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0))
            renpy.set_screen_variable("ui_record_state", "done")
        except Exception as e:
            renpy.log("syll-record failed: %r" % e)
            renpy.set_screen_variable("ui_record_state", "done")   # Continue and exclude this sound from selection.
        renpy.restart_interaction()

    def do_syll_select():
        """Pick the best of seven sounds and load syllable_result.json into the screen state."""
        gamedir = renpy.config.gamedir
        exe = os.path.join(gamedir, "python", "voice_engine", "voice_engine.exe")
        result_json = os.path.join(gamedir, "data", "syllable_result.json")
        fail = {"status": "no_candidate", "selected": None, "image": ""}
        try:
            subprocess.run([exe, "syll-select"],
                           check=True, capture_output=True,
                           creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0))
        except Exception as e:
            renpy.log("syll-select failed: %r" % e)
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
            renpy.log("Could not read syllable_result.json: %r" % e)
            renpy.set_screen_variable("syll_result", fail)
        renpy.free_memory()   # Reload the selected sound image from disk.
        renpy.restart_interaction()



    def pick_sentence():
        """random sentence"""
        import random
        gamedir = renpy.config.gamedir
        p = os.path.join(gamedir, "data", "sentences.json")
        try:
            with open(p, encoding="utf-8") as f:
                data = json.load(f)
            return random.choice(data["sentences"])
        except Exception as e:
            renpy.log("sentences.json reading fail: %r" % e)
            return {"id": "fallback", "text": "사자가 숲속에서 사과를 찾았어요", "target_count": 2}

    def do_sentence(sentence, seconds=8):
        """Record and analyze the sentence, then read sentence_result.json into screen variables.
        ok -> ui_record_state='done' / otherwise -> 'ready' (re-record)."""
        gamedir = renpy.config.gamedir
        exe = os.path.join(gamedir, "python", "voice_engine", "voice_engine.exe")
        result_json = os.path.join(gamedir, "data", "sentence_result.json")
        data = {"status": "unmeasurable", "expected_count": 0, "detected_count": 0}
        try:
            subprocess.run([exe, "sentence", sentence, str(seconds)],
                           check=True, capture_output=True,
                           creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0))
            with open(result_json, encoding="utf-8") as f:
                data = json.load(f)
        except Exception as e:
            renpy.log("sentence run/read failed: %r" % e)
        renpy.set_screen_variable("ui_sentence_result", data)
        renpy.set_screen_variable("ui_record_state",
                                  "done" if data.get("status") == "ok" else "ready")
        renpy.restart_interaction()


    def _save_sentence_result_copy(dest_name):
        """sentence_result.json을 고정 이름으로 복사해 인트로/보스가 서로 덮어쓰지 않게 한다."""
        import shutil
        gamedir = renpy.config.gamedir
        src = os.path.join(gamedir, "data", "sentence_result.json")
        dst = os.path.join(gamedir, "data", dest_name)
        try:
            shutil.copyfile(src, dst)
            return True
        except Exception as e:
            renpy.log("Could not copy sentence result to %s: %r" % (dest_name, e))
            return False

    def run_voice_engine_sentence(sentence, seconds=8):
        gamedir = renpy.config.gamedir
        exe = os.path.join(gamedir, "python", "voice_engine", "voice_engine.exe")
        result_json = os.path.join(gamedir, "data", "sentence_result.json")
        try:
            subprocess.run([exe, "sentence", sentence, str(seconds)],
                           check=True, capture_output=True,
                           creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0))
            with open(result_json, encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            renpy.log("sentence run/read failed: %r" % e)
            return None

    def do_record_sentence_boss(sentence):
        """보스 3라운드: 문장(다중 /ㅅ/) 녹음 → 보스 복사본 저장 → 전투 화면용 ui_voice 설정.
        타깃 전부 success일 때만 성공."""
        data = run_voice_engine_sentence(sentence)
        targets = []                                   # ← 미리 초기화 (실패 분기 대비)
        if not data or data.get("status") != "ok":
            if data is not None:
                ui_unrec_set_kind(data.get("reason") or data.get("status"))
            result = {"result": "unrecognized",
                      "feedback": "We couldn't hear you clearly. Want to try again?",
                      "gauges": {}, "segment_estimated": False, "targets": targets}
        else:
            _save_sentence_result_copy("sentence_boss.json")
            targets = data.get("targets", [])
            all_ok = bool(targets) and all(t.get("success") for t in targets)
            result = {"result": "success" if all_ok else "fail",
                      "feedback": "", "gauges": {}, "segment_estimated": False,
                      "targets": targets}
        renpy.set_screen_variable("ui_voice", result)
        renpy.set_screen_variable("ui_record_state", "result")
        renpy.restart_interaction()