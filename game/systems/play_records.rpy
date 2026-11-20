default persistent.play_completed_chapters = set()
default persistent.play_cleared_monsters = set()
default persistent.play_events = {}

init python:
    from time import localtime, strftime, time
    from uuid import uuid4

    def merge_play_progress(old, new, current):
        return (old or set()) | (new or set()) | (current or set())

    def merge_play_events(old, new, current):
        merged = dict(old or {})
        merged.update(new or {})
        merged.update(current or {})
        return merged

    renpy.register_persistent("play_completed_chapters", merge_play_progress)
    renpy.register_persistent("play_cleared_monsters", merge_play_progress)
    renpy.register_persistent("play_events", merge_play_events)

    def remember_play_progress():
        chapters = persistent.play_completed_chapters | completed_chapters
        monsters = persistent.play_cleared_monsters | cleared_monsters
        if chapters != persistent.play_completed_chapters or monsters != persistent.play_cleared_monsters:
            persistent.play_completed_chapters = chapters
            persistent.play_cleared_monsters = monsters
            renpy.save_persistent()

    config.after_load_callbacks.append(remember_play_progress)

    def record_play_event(monster_name, result, word=None, is_test=False, attempt_id=None):
        if monster_name and not _in_replay:
            persistent.play_events[uuid4().hex] = (time(), monster_name, result, word, is_test, attempt_id)
            renpy.save_persistent()

    def play_result_actions(monster_name, word, result, is_test=False, attempt_id=None):
        # Log fresh screen actions. Ren'Py can roll forward a Return value without
        # running the action again.
        return [
            Function(record_play_event, monster_name, result, word, is_test, attempt_id, _update_screens=False),
            Return(result),
        ]

    def format_play_event(event):
        timestamp, monster_name, result, word, is_test = event[:5]
        result_labels = {
            "success": _("Success"),
            "fail": _("Failed"),
            "unrecognized": _("No Reading"),
            "retry": _("Battle Restarted"),
        }
        entry = _("{} | {} | {}").format(strftime("%Y-%m-%d %H:%M", localtime(timestamp)), monster_name, result_labels.get(result, result))
        if word:
            entry += _(" | Word: {}").format(word)
        if is_test:
            entry += _(" | Test")
        return entry


screen play_records():
    tag menu

    default events = sorted(persistent.play_events.values(), key=lambda event: event[0], reverse=True)
    default page = 0
    $ page_size = 12
    $ page_count = max(1, (len(events) + page_size - 1) // page_size)

    use game_menu(_("Play Records"), scroll="viewport", spacing=16):
        label _("Progress")
        for chapter in range(1, 4):
            $ cleared = sum(1 for item in persistent.play_cleared_monsters if item[0] == chapter)
            $ status = _("Cleared") if chapter in persistent.play_completed_chapters else _("Unlocked") if chapter == 1 or chapter in persistent.unlocked_chapters else _("Locked")
            text _("Chapter {} | {} | Monsters cleared: {} / 3").format(chapter, status, cleared)

        label _("Pronunciation and Battle History")
        if events:
            hbox:
                spacing 24
                textbutton _("Previous") action SetScreenVariable("page", page - 1) sensitive (page > 0)
                text _("{}/{}").format(page + 1, page_count) yalign 0.5
                textbutton _("Next") action SetScreenVariable("page", page + 1) sensitive (page + 1 < page_count)

            for event in events[page * page_size:(page + 1) * page_size]:
                text format_play_event(event) substitute False
        else:
            text _("No play records yet.")
