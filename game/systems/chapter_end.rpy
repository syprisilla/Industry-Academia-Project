transform chapter_end_fade_out:
    alpha 1.0
    linear 0.4 alpha 0.0

screen chapter_end_card(image_path):
    modal True
    zorder 200
    default leaving = False

    add Solid("#000")

    if leaving:
        add image_path at chapter_end_fade_out:
            xysize (config.screen_width, config.screen_height)
            fit "cover"
        timer 0.4 action Return()
    else:
        button:
            style "empty"
            xfill True
            yfill True
            action SetScreenVariable("leaving", True)

            add image_path:
                xysize (config.screen_width, config.screen_height)
                fit "cover"

        key "dismiss" action SetScreenVariable("leaving", True)

label show_chapter_end(image_path):
    window hide None
    call screen chapter_end_card(image_path) with Dissolve(0.4)
    window auto
    return
