from __future__ import annotations

# TODO: make videos page paginated


#  Deferred translations!
def _(message):
    return message


VIDEO_TAGS = {
    "Howto": _("Howto"),
    "Introduction": _("Introduction"),
    "Opening": _("Opening"),
    "Middlegame": _("Middlegame"),
    "Endgame": _("Endgame"),
    "Fundamentals": _("Fundamentals")
}

VIDEO_TARGETS = {
    "beginner": _("beginner"),
    "intermediate": _("intermediate"),
    "advanced": _("advanced"),
}

del _

VIDEOS = [
]
