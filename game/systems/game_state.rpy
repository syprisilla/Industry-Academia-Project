default current_chapter = 0
default completed_chapters = set()
default cleared_monsters = set()

define config.has_autosave = False

init python:
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
    # Retain checkpoint statements for existing saves. Autosaving is disabled.
    $ renpy.block_rollback()
    $ renpy.force_autosave(take_screenshot=True, block=True)
    return
