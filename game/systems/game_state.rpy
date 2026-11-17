default current_chapter = 0
default completed_chapters = set()
default cleared_monsters = set()
default persistent.unlocked_chapters = set()

define config.has_autosave = False

init python:
    def unlock_chapter(chapter):
        if chapter not in persistent.unlocked_chapters:
            persistent.unlocked_chapters.add(chapter)
            renpy.save_persistent()

    renpy.register_persistent("unlocked_chapters", lambda old, new, current: (old or set()) | (new or set()) | (current or set()))

    def save_to_empty_slot():
        occupied = set(renpy.list_slots())
        slots_per_page = gui.file_slot_cols * gui.file_slot_rows
        index = 0
        while True:
            page, slot = divmod(index, slots_per_page)
            page, slot = page + 1, slot + 1
            filename = "{}-{}".format(page, slot)
            if filename not in occupied:
                break
            index += 1

        save_action = FileSave(
            filename, page=page, slot=True,
            action=MainMenu(confirm=False, save=False),
        )
        if save_action.get_sensitive():
            if not renpy.context()._menu:
                renpy.take_screenshot()
            save_action()

label progress_autosave:
    $ remember_play_progress()
    # Retain the checkpoint statements for existing saves.
    $ renpy.block_rollback()
    $ renpy.force_autosave(take_screenshot=True, block=True)
    return

label start_unlocked_chapter_1:
    scene apartment elevator_on
    show ui_ghost intro_move
    jump chapter1

label start_unlocked_chapter_2:
    scene apartment elevator_on
    show ui_ghost at ui_ghost_corridor, ui_ghost_settle
    jump chapter2

label start_unlocked_chapter_3:
    scene apartment elevator_on
    show ui_ghost at ui_ghost_corridor
    jump chapter3
