from enum import Enum, EnumMeta


class EnumContainsItemMeta(EnumMeta):
    def __contains__(cls, item: str) -> bool:  # type: ignore
        return item in cls.__members__.values()


class Section(str, Enum, metaclass=EnumContainsItemMeta):
    # DAYS
    monday = "MONDAY"
    tuesday = "TUESDAY"
    wednesday = "WEDNESDAY"
    thursday = "THURSDAY"
    friday = "FRIDAY"
    # you should not work at these days ;)
    saturday = "SATURDAY"
    sunday = "SUNDAY"

    # OTHERS
    todo = "TODO"


class CommandEnum(str, Enum, metaclass=EnumContainsItemMeta):
    ls = "ls"
    todo = "td"
    done = "dn"
    reset = "rst"
    quit = "q"
    edit = "e"
    move = "mv"
