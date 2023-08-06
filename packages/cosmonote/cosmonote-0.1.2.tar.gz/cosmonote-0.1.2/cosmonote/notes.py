import re
from typing import cast

NOTE_PROG = re.compile(r"([^\n]+)(?:\n\n(.*))?\n?", re.S)
TITLE_PROG = re.compile(r"^\s*(\S+.*?)\s*$")


class InvalidNoteError(Exception):
    pass


def parse_note(note: str) -> tuple[str, str]:
    m = NOTE_PROG.match(note)
    if not m:
        raise InvalidNoteError()
    title_line, content = m.groups()
    m = TITLE_PROG.match(title_line)
    if not m:
        raise InvalidNoteError()
    title = m.groups()[0]
    return cast(str, title), content
