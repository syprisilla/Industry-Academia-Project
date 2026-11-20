# ==================================================
# 설정 화면 + UI 설정 저장/불러오기
#
# 저장되는 값
#   - 볼륨, 글자 속도, 자동 넘김, 화면 모드: Ren'Py 기본 설정 (자동 저장)
#   - 대사 글자 크기: gui.preference("ui_dialogue_size")  (자동 저장)
#   - 대화창 투명도: persistent.ui_textbox_alpha        (자동 저장)
# 게임을 껐다 켜도 마지막 설정이 그대로 불러와진다.
#
# screens.rpy 의 screen preferences() 는 이 파일의 ui_settings_content 를 사용
# ==================================================


# --------------------------------------------------
# 저장되는 UI 설정 기본값
# --------------------------------------------------

default persistent.ui_textbox_alpha = 1.0

# 대사 글자 크기 (기본 33). 바꾸면 Ren'Py가 자동으로 저장하고 다음 실행 때 불러온다.
define gui.ui_dialogue_size = gui.preference("ui_dialogue_size", 33)

# 글자 크기 선택지: (버튼 이름, 크기)
define ui_dialogue_sizes = [("Normal", 33), ("Large", 40), ("Extra Large", 46)]


init python:

    def ui_textbox_frame(alpha=None):
        """대화창 배경: 전투 UI와 같은 패널을 늘려서 사용"""
        return Transform(
            Frame(intro_ch1_ui + "panel_hint.png", 60, 62, 60, 30),
            alpha=persistent.ui_textbox_alpha if alpha is None else alpha,
        )

    def ui_textbox_background(st, at):
        """저장된 투명도를 매번 적용"""
        return ui_textbox_frame(), None

    def ui_settings_reset():
        """모든 설정을 처음 상태로 되돌림"""
        persistent.ui_textbox_alpha = 1.0

        try:
            _preferences.set_volume("music", config.default_music_volume)
            _preferences.set_volume("sfx", config.default_sfx_volume)
            _preferences.set_mute("music", False)
            _preferences.set_mute("sfx", False)
            _preferences.set_mute("voice", False)
            _preferences.text_cps = config.default_text_cps
            _preferences.afm_time = config.default_afm_time
        except Exception as e:
            renpy.log("Settings reset failed: %r" % e)

        # 글자 크기는 GUI를 다시 그려야 해서 마지막에 적용
        gui.SetPreference("ui_dialogue_size", 33)()


# --------------------------------------------------
# 대화창 디자인 (전투 UI 패널과 같은 스타일)
# 대화창 크기·위치를 바꾸려면 여기 숫자만 수정
# --------------------------------------------------

style window:
    xalign 0.5
    xfill False
    xsize 1640
    yalign 1.0
    yoffset -48
    ysize 232
    background DynamicDisplayable(ui_textbox_background)

# 이름 칸: 대화창 왼쪽 위에 살짝 걸치게
style namebox:
    xpos 70
    xanchor 0.0
    ypos -31
    xminimum 240
    ysize 62
    background Frame(intro_ch1_ui + "panel_hint.png", 30, 24, 30, 24)
    padding (34, 6, 34, 6)

style say_label:
    size 34
    xalign 0.5
    yalign 0.5

style say_dialogue:
    xpos 100
    ypos 72
    # 조음 안내·피드백 화면 오른쪽 아래 버튼과 겹치지 않는 너비
    xsize 1240
    size gui.ui_dialogue_size

# 이름 입력 화면에도 같은 글자 크기 적용
style input_prompt:
    size gui.ui_dialogue_size

style input:
    size gui.ui_dialogue_size


# --------------------------------------------------
# 스타일
# --------------------------------------------------

style ui_settings_bar is slider:
    xsize 582

style ui_settings_title is intro_ch1_text:
    size 40
    bold True
    text_align 0.0

style ui_settings_label is intro_ch1_caption:
    size 28
    text_align 0.0


# --------------------------------------------------
# 카드 (패널 배경 + 제목 + 내용)
# --------------------------------------------------

screen ui_settings_card(title, w=670, h=400):
    fixed:
        xysize (w, h)

        add intro_ch1_ui + "panel_assessment.png" xysize (w, h) fit "fill" alpha 0.92

        text title style "ui_settings_title" xpos 60 ypos 30

        vbox:
            xpos 44
            ypos 100
            spacing 12

            transclude


# --------------------------------------------------
# 설정 화면 내용
# --------------------------------------------------

screen ui_settings_content():

    $ muted = Preference("all mute", "toggle").get_selected()
    $ fullscreen = Preference("display", "fullscreen").get_selected()
    $ current_size = gui.preference("ui_dialogue_size", 33)

    vbox:
        spacing 30

        # ---------- 1줄: 소리 / 글자 ----------
        hbox:
            spacing 30

            use ui_settings_card("Sound"):

                if config.has_music:
                    text "Music" style "ui_settings_label"
                    bar value Preference("music volume") style "ui_settings_bar"

                if config.has_sound:
                    text "Sound Effects" style "ui_settings_label"
                    bar value Preference("sound volume") style "ui_settings_bar"

                null height 6

                use intro_ch1_button(
                    ("Sound Off" if muted else "Mute All"),
                    ("fail" if muted else "next"),
                    Preference("all mute", "toggle"),
                    width=280, height=64,
                )

            use ui_settings_card("Text"):

                text "Text Speed" style "ui_settings_label"
                bar value Preference("text speed") style "ui_settings_bar"

                text "Auto-Forward Time" style "ui_settings_label"
                bar value Preference("auto-forward time") style "ui_settings_bar"

                text "Text Size" style "ui_settings_label"

                hbox:
                    spacing 12
                    for size_name, size_value in ui_dialogue_sizes:
                        use intro_ch1_button(
                            size_name,
                            ("success" if current_size == size_value else "next"),
                            gui.SetPreference("ui_dialogue_size", size_value),
                            width=186, height=64,
                        )

        # ---------- 2줄: 화면 / 미리보기 ----------
        hbox:
            spacing 30

            use ui_settings_card("Display", h=360):

                if renpy.variant("pc") or renpy.variant("web"):

                    text "Screen" style "ui_settings_label"

                    hbox:
                        spacing 12
                        use intro_ch1_button(
                            "Windowed",
                            ("next" if fullscreen else "success"),
                            Preference("display", "window"),
                            width=285, height=64,
                        )
                        use intro_ch1_button(
                            "Full Screen",
                            ("success" if fullscreen else "next"),
                            Preference("display", "fullscreen"),
                            width=285, height=64,
                        )

                    null height 6

                text "Dialogue Box" style "ui_settings_label"
                bar value FieldValue(persistent, "ui_textbox_alpha", range=0.7, offset=0.3) style "ui_settings_bar"

            use ui_settings_card("Preview", h=360):

                # 지금 설정으로 대사가 어떻게 보이는지 미리보기
                fixed:
                    xysize (582, 130)

                    add ui_textbox_frame() xysize (582, 130)

                    text "Let's say the word together!":
                        xpos 28
                        yalign 0.5
                        xmaximum 530
                        size current_size
                        color "#FFFFFF"

                null height 6

                use intro_ch1_button(
                    "Reset to Default",
                    "continue",
                    Confirm("Reset all settings to default?", Function(ui_settings_reset)),
                    width=320, height=64,
                )
