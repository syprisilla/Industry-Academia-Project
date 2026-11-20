default ui_compare_intro = None
default persistent.ui_compare_pair = None
default persistent.ui_compare_latest_intro = None

init python:
    def ui_compare_capture(filename, sentence):
        # Use the same single-segment analysis for both recordings.
        gamedir = renpy.config.gamedir
        executable = os.path.join(gamedir, "python", "voice_engine", "voice_engine.exe")
        recording = os.path.join(gamedir, "data", "recordings", filename)
        try:
            process = subprocess.run(
                [executable, "judge", recording], check=True, capture_output=True,
                creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0),
            )
            data = json.loads(process.stdout)
            if data.get("status") != "ok" or data.get("segment_estimated"):
                return None
            features = data["judge"]["per_feature"]
            gauges = {feature: features[feature]["gauge"] for feature, label in ui_feedback_cards}
            return {"sentence": sentence, "success": data["success"], "gauges": gauges}
        except (OSError, subprocess.SubprocessError, ValueError, KeyError) as error:
            renpy.log("Could not capture pronunciation comparison: %r" % error)
            return None

    def ui_compare_capture_intro(sentence):
        sample = ui_compare_capture("sentence.wav", sentence)
        if sample:
            persistent.ui_compare_latest_intro = sample
            renpy.save_persistent()
        return sample

    def ui_compare_capture_boss(sentence, voice):
        if (not ui_compare_intro or ui_compare_intro["sentence"] != sentence
                or voice["result"] not in ("success", "fail") or voice.get("segment_estimated")):
            return
        sample = ui_compare_capture("rec.wav", sentence)
        if sample:
            persistent.ui_compare_pair = (ui_compare_intro, sample)
            renpy.save_persistent()


screen ui_pronunciation_compare():
    modal True
    zorder 100
    key "game_menu" action Hide("ui_pronunciation_compare")

    $ intro_sample, boss_sample = persistent.ui_compare_pair or (persistent.ui_compare_latest_intro, None)

    add "apartment corridor_1"
    add Solid("#10152F88")

    vbox:
        xalign 0.5
        ypos 105
        spacing 32

        fixed:
            xysize (930, 108)
            xalign 0.5
            add intro_ch1_ui + "panel_assessment.png" xysize (930, 108) fit "fill"
            text "Compare Pronunciation" style "intro_ch1_text" size 58 bold True align (0.5, 0.5)

        if intro_sample:
            text intro_sample["sentence"] style "intro_ch1_caption" xalign 0.5 size 38

        hbox:
            spacing 22
            use ui_compare_result("Intro", intro_sample)
            use ui_compare_result("Final Boss (Round 3)", boss_sample)

        fixed:
            xysize (240, 68)
            xalign 0.5
            use intro_ch1_button("Back", "continue", Hide("ui_pronunciation_compare"), width=240, height=68)


screen ui_compare_result(title, sample):
    fixed:
        xysize (836, 500)
        add intro_ch1_ui + "panel_assessment.png" xysize (836, 500) fit "fill" alpha 0.92
        text title style "intro_ch1_text" size 38 bold True xalign 0.5 ypos 34

        if sample:
            text ("You did it!" if sample["success"] else "Let's practice once more"):
                style "intro_ch1_text"
                size 40
                bold True
                color ("#C8F2DC" if sample["success"] else "#FFF2C7")
                xalign 0.5
                ypos 103

            hbox:
                xalign 0.5
                ypos 189
                spacing 16
                for feature, label in ui_feedback_cards:
                    use ui_compare_gauge(label, sample["gauges"][feature])
        else:
            text "No recording available yet." style "intro_ch1_caption" align (0.5, 0.5)


screen ui_compare_gauge(label, gauge):
    $ start = 30 + int(320 * gauge["range_low_pos"])
    $ end = 30 + int(320 * gauge["range_high_pos"])
    $ marker = 30 + int(320 * gauge["value_pos"])

    fixed:
        xysize (380, 240)
        add intro_ch1_ui + "panel_hint.png" xysize (380, 240) fit "fill"
        text label style "intro_ch1_text" size 27 bold True xalign 0.5 ypos 33
        add Solid("#E7E6E1") pos (30, 114) xysize (320, 23)
        add Solid("#9FD3B8") pos (start, 114) xysize (end - start, 23)
        add Solid("#D8A13A") pos (marker - 2, 94) xysize (5, 55)
        text "●" style "intro_ch1_text" color "#D8A13A" size 23 xpos marker xanchor 0.5 ypos 77
        text "Your sound" style "intro_ch1_text" color "#F4C96B" size 22 xpos max(83, min(marker, 297)) xanchor 0.5 ypos 154
        text "Target range" style "intro_ch1_text" color "#9FD3B8" size 22 xpos ((start + end) // 2) xanchor 0.5 ypos 185
