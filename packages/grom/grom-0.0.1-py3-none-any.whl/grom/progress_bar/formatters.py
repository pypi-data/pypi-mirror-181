"""
Stylish formatter classes for the Prompt toolkit progress bar.
"""
import time
from enum import Enum

from prompt_toolkit.formatted_text import HTML, AnyFormattedText
from prompt_toolkit.layout.dimension import AnyDimension, D
from prompt_toolkit.shortcuts import progress_bar
from prompt_toolkit.utils import get_cwidth

from grom.theme import GromSpinnerStyle, GromSpinnerStyles


class ProgressSpinningWheel(progress_bar.Formatter):
    """
    Display a spinning wheel.
    """

    def __init__(self, style: GromSpinnerStyle = GromSpinnerStyles.DOT, show_completed: bool = True) -> None:
        if issubclass(GromSpinnerStyles, Enum):
            self.style = style.value
        else:
            self.style = style
        self._show_completed = show_completed
        self._space = " " if get_cwidth(self.style.frames[0]) > len(self.style.frames[0]) else ""
        self._completed = self.style.done_frame

    def format(
        self,
        progress_bar: "progress_bar.ProgressBar",
        progress: "progress_bar.ProgressBarCounter[object]",
        width: int,
    ) -> AnyFormattedText:
        index = int(time.time() * self.style.fps) % len(self.style.frames)
        output = self._completed if self._show_completed and progress.stopped else self.style.frames[index]
        return HTML(f"<spinning-wheel>{output}{self._space}</spinning-wheel>")

    def get_width(self, progress_bar: "progress_bar.ProgressBar") -> AnyDimension:
        return D.exact(len(self.style.frames[0]) + len(self._space))
