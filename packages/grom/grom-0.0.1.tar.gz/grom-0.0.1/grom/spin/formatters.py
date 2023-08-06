"""
GromSpinFormatter classes for the Grom spinner.
Each spinner consists of a list of these formatters.
"""
import datetime
import time
from abc import ABCMeta, abstractmethod
from enum import Enum
from typing import TYPE_CHECKING, List

from prompt_toolkit.formatted_text import (
    HTML,
    AnyFormattedText,
    StyleAndTextTuples,
    to_formatted_text,
)
from prompt_toolkit.formatted_text.utils import fragment_list_width
from prompt_toolkit.layout.dimension import AnyDimension, D
from prompt_toolkit.layout.utils import explode_text_fragments
from prompt_toolkit.utils import get_cwidth

from grom.theme import GromSpinnerStyles, GromSpinnerStyle

if TYPE_CHECKING:
    from .base import GromSpin, Spinner

__all__ = [
    "SpinFormatter",
    "SpinText",
    "SpinLabel",
    "SpinTimeElapsed",
    "SpinWheel",
    "create_default_spin_formatters",
]


class SpinFormatter(metaclass=ABCMeta):
    """
    Base class for any formatter.
    """

    @abstractmethod
    def format(
        self,
        spin: "GromSpin",
        spinner: "Spinner[object]",
        width: int,
    ) -> AnyFormattedText:
        pass

    def get_width(self, spin: "GromSpin") -> AnyDimension:  # pylint: disable=unused-argument
        return D()


class SpinText(SpinFormatter):
    """
    Display plain text.
    """

    def __init__(self, text: AnyFormattedText, style: str = "") -> None:
        self.text = to_formatted_text(text, style=style)

    def format(
        self,
        spin: "GromSpin",
        spinner: "Spinner[object]",
        width: int,
    ) -> AnyFormattedText:
        return self.text

    def get_width(self, spin: "GromSpin") -> AnyDimension:
        return fragment_list_width(self.text)


class SpinLabel(SpinFormatter):
    """
    Display the name of the current task.

    :param width: If a `width` is given, use this width. Scroll the text if it
        doesn't fit in this width.
    :param suffix: String suffix to be added after the task name, e.g. ': '.
        If no task name was given, no suffix will be added.
    """

    def __init__(self, width: AnyDimension = None, suffix: str = "") -> None:
        self.width = width
        self.suffix = suffix

    def _add_suffix(self, label: AnyFormattedText) -> StyleAndTextTuples:
        label = to_formatted_text(label, style="class:label")
        return label + [("", self.suffix)]

    def format(
        self,
        spin: "GromSpin",
        spinner: "Spinner[object]",
        width: int,
    ) -> AnyFormattedText:

        label = self._add_suffix(spinner.label)
        cwidth = fragment_list_width(label)

        if cwidth > width:
            # It doesn't fit -> scroll task name.
            label = explode_text_fragments(label)
            max_scroll = cwidth - width
            current_scroll = int(time.time() * 3 % max_scroll)
            label = label[current_scroll:]

        return label

    def get_width(self, spin: "GromSpin") -> AnyDimension:
        if self.width:
            return self.width

        all_labels = [self._add_suffix(c.label) for c in spin.spinners]
        if all_labels:
            max_widths = max(fragment_list_width(lbl) for lbl in all_labels)
            return D(preferred=max_widths, max=max_widths)
        return D()


def _format_timedelta(timedelta: datetime.timedelta) -> str:
    """
    Return hh:mm:ss, or mm:ss if the amount of hours is zero.
    """
    result = f"{timedelta}".split(".")[0]
    if result.startswith("0:"):
        result = result[2:]
    return result


class SpinTimeElapsed(SpinFormatter):
    """
    Display the elapsed time.
    """

    def format(
        self,
        spin: "GromSpin",
        spinner: "Spinner[object]",
        width: int,
    ) -> AnyFormattedText:

        text = _format_timedelta(spinner.time_elapsed).rjust(width)
        return HTML("<time-elapsed>{time_elapsed}</time-elapsed>").format(
            time_elapsed=text
        )

    def get_width(self, spin: "GromSpin") -> AnyDimension:
        all_values = [
            len(_format_timedelta(c.time_elapsed)) for c in spin.spinners
        ]
        if all_values:
            return max(all_values)
        return 0


class SpinWheel(SpinFormatter):
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

    # pylint: disable=unused-argument
    def format(
        self,
        spin: "GromSpin",
        spinner: "Spinner[object]",
        width: int,
    ) -> AnyFormattedText:
        index = int(time.time() * self.style.fps) % len(self.style.frames)
        output = self._completed if self._show_completed and spinner.stopped else self.style.frames[index]
        return HTML(f"<spinning-wheel>{output}{self._space}</spinning-wheel>")

    def get_width(self, spin: "GromSpin") -> AnyDimension:
        return D.exact(len(self.style.frames[0]) + len(self._space))


def create_default_spin_formatters() -> List[SpinFormatter]:
    """
    Return the list of default formatters.
    """
    return [
        SpinWheel(),
        SpinText(" "),
        SpinLabel(),
        SpinText(" "),
        SpinTimeElapsed(),
    ]
