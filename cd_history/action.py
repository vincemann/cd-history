from enum import Enum


# action applied to the result dirs
class Action(Enum):
    # just print the dirs (no selection)
    SHOW = "show"
    # let user select dir and only print that
    SELECT = "select"
