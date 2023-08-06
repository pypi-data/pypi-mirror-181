"""
A bias, nicely styled progress bar without a lot of the fuzz.

But yet you can customize it like a regular progress bar upon need.
"""
from typing import Callable, Optional, Sequence, TextIO

from prompt_toolkit.formatted_text import AnyFormattedText
from prompt_toolkit.input import Input
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.output import ColorDepth, Output
from prompt_toolkit.shortcuts import ProgressBar
from prompt_toolkit.shortcuts.progress_bar import Formatter, formatters
from prompt_toolkit.styles import BaseStyle

from grom.theme import GromSpinnerStyles, GromTheme, GromThemer
from .formatters import ProgressSpinningWheel


def create_default_progress_formatters() -> Optional[Sequence[Formatter]]:
    return [
        ProgressSpinningWheel(style=GromSpinnerStyles.DOT),
        formatters.Text(" "),
        formatters.Label(width=40),
        formatters.Text(" "),
        formatters.Bar(start="", end="", sym_a="░", sym_b="░", sym_c=" "),
        formatters.Text(" "),
        formatters.TimeElapsed(),
    ]


class GromProgressBar(ProgressBar):
    """
    Styled progress bar.
    """

    def __init__(
        self,
        title: AnyFormattedText = None,
        formatters: Optional[Sequence[Formatter]] = None,
        bottom_toolbar: AnyFormattedText = None,
        style: Optional[BaseStyle] = None,
        key_bindings: Optional[KeyBindings] = None,
        cancel_callback: Optional[Callable[[], None]] = None,
        file: Optional[TextIO] = None,
        color_depth: Optional[ColorDepth] = None,
        output: Optional[Output] = None,
        input: Optional[Input] = None,  # pylint: disable=redefined-builtin
    ) -> None:
        super().__init__(
            title=title,
            formatters=create_default_progress_formatters() if formatters is None else formatters,
            bottom_toolbar=bottom_toolbar,
            style=GromThemer(theme=GromTheme()).get_style() if style is None else style,
            key_bindings=key_bindings,
            cancel_callback=cancel_callback,
            file=file,
            color_depth=color_depth,
            output=output,
            input=input
        )
