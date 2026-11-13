define scene_menu_music = "audio/메인 화면.flac"
define scene_field_music = "audio/낯선 벌판·아파트 외관.ogg"
define scene_entrance_music = "audio/아파트 입구·유령 첫 등장.ogg"
# PCM16 copies of Chapter 1 복도 탐험.wav and 전투장면.wav.
define scene_corridor_music = "audio/chapter1_corridor.wav"
define scene_battle_music = "audio/chapter1_battle.wav"
define scene_elevator_sound = "audio/엘리베이터 도착.ogg"
define scene_wave_sound = "audio/음파 발사·명중.ogg"
define scene_corridor_volume = 0.85
define scene_battle_volume = 0.8

init python:
    def stop_scene_music():
        renpy.music.stop(channel="music", fadeout=0.6)

    def play_scene_music(filename, volume=0.35):
        if not renpy.loadable(filename):
            stop_scene_music()
            return

        renpy.music.play(
            filename,
            channel="music",
            loop=True,
            fadeout=0.6,
            fadein=0.6,
            if_changed=True,
            relative_volume=volume,
        )

    def play_scene_sound(filename, volume=0.65):
        if renpy.loadable(filename):
            renpy.music.play(
                filename,
                channel="sound",
                loop=False,
                fadeout=0.0,
                relative_volume=volume,
            )

label before_main_menu:
    $ play_scene_music(scene_menu_music, volume=0.4)
    return
