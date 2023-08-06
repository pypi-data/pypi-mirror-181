"""
Grom theming
"""
from dataclasses import dataclass
from enum import Enum

from prompt_toolkit.styles import Style


@dataclass
class GromTheme:
    """
    Grom theme lets you customize default colors in use by Grom formatters and components.
    """
    fg_main: str = "#ffffff bold"
    bg_main: str = None
    fg_highlight = "#ff87d7"
    bg_highlight = None


@dataclass
class GromTerminalColorTheme(GromTheme):
    """
    Desert theme
    """
    fg_main = "white"
    fg_highlight = "yellow"


@dataclass
class GromDesertTheme(GromTheme):
    """
    Desert theme
    """
    fg_main = "white"
    fg_highlight = "#8E8E8E"


@dataclass
class GromForestTheme(GromTheme):
    """
    Desert theme
    """
    fg_main = "white"
    fg_highlight = "#04B575"


class Singleton(type):
    """
    Singleton used by Grom themer
    """
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class GromThemer(metaclass=Singleton):
    """
    Grom theme holder class
    """

    def __init__(self, theme: GromTheme = GromTheme()) -> None:
        self._init(theme)

    def _init(self, theme: GromTheme):
        self._theme = theme
        self._style = self._create_style()

    def get_theme(self):
        """
        Get the current set theme
        """
        return self._theme

    def set_theme(self, theme: GromTheme) -> None:
        """
        Set a new theme
        """
        self._init(theme)

    def get_style(self):
        """
        Get the current set style
        """
        return self._style

    def _create_style(self):
        return Style.from_dict({
            "progressbar title": f"{self._theme.fg_main} bold",
            "bar": f"{self._theme.fg_highlight}",
            "time-left": f"{self._theme.fg_highlight}",
            "spinning-wheel": f"{self._theme.fg_highlight}",
        })


@dataclass(frozen=True)
class GromSpinnerStyle:
    """_summary_
    """
    frames: list[str]
    done_frame: str
    stopped_frame: str
    fps: int


class GromSpinnerStyles(Enum):
    """_summary_

    Args:
        Enum (_type_): _description_
    """
    LINE = GromSpinnerStyle(["|", "/", "-", "\\"], "✓", "ⅹ", 2)
    DOT = GromSpinnerStyle(["⣾", "⣽", "⣻", "⢿", "⡿", "⣟", "⣯", "⣷"], "✓", "⚠", 3)
    MINIDOT = GromSpinnerStyle(["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"], "✓", "⚠", 3)
    JUMP = GromSpinnerStyle(["⢄", "⢂", "⢁", "⡁", "⡈", "⡐", "⡠"], "✓", "⚠", 3)
    PULSE = GromSpinnerStyle(["█", "▓", "▒", "░"], "✓", "⚠", 2)
    POINTS = GromSpinnerStyle(["∙∙∙", "●∙∙", "∙●∙", "∙∙●"], "✓", "⚠", 2)
    GLOBE = GromSpinnerStyle(["🌍", "🌎", "🌏"], "✓", "⚠", 2)
    MOON = GromSpinnerStyle(["🌑", "🌒", "🌓", "🌔", "🌕", "🌖", "🌗", "🌘"], "✓", "⚠", 3)
    MONKEY = GromSpinnerStyle(["🙈", "🙉", "🙊"], "✓", "⚠", 2)
    METER = GromSpinnerStyle(["▱▱▱", "▰▱▱", "▰▰▱", "▰▰▰", "▰▰▱", "▰▱▱", "▱▱▱"], "✓", "⚠", 2)
    HAMBURGER = GromSpinnerStyle(["☱", "☲", "☴", "☲"], "✓", "⚠", 3)


__out__ = ["GromThemer", "GromTheme", "GromTerminalColorTheme",
           "GromDesertTheme", "GromForestTheme", "GromSpinnerStyle", "GromSpinnerStyles"]
