"""
Spinner implementation on top of prompt_toolkit.

::

    with GromSpin(...) as pb:
        for item in pb(data):
            ...
"""
import datetime
import functools
import os
import signal
import threading
import traceback
from asyncio import new_event_loop, set_event_loop
from typing import Callable, Generic, Iterable, List, Optional, Sequence, TextIO, TypeVar

from prompt_toolkit.application import Application
from prompt_toolkit.application.current import get_app_session
from prompt_toolkit.filters import Condition, is_done, renderer_height_is_known
from prompt_toolkit.formatted_text import AnyFormattedText, StyleAndTextTuples, to_formatted_text
from prompt_toolkit.input import Input
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.key_binding.key_processor import KeyPressEvent
from prompt_toolkit.layout import ConditionalContainer, FormattedTextControl, HSplit, Layout, VSplit, Window
from prompt_toolkit.layout.controls import UIContent, UIControl
from prompt_toolkit.layout.dimension import AnyDimension, D
from prompt_toolkit.output import ColorDepth, Output
from prompt_toolkit.styles import BaseStyle

from .formatters import SpinFormatter, create_default_spin_formatters
from grom.theme import GromThemer

try:
    import contextvars
except ImportError:
    from prompt_toolkit.eventloop import dummy_contextvars

    contextvars = dummy_contextvars  # type: ignore


__all__ = ["GromSpin"]

E = KeyPressEvent

_SIGWINCH = getattr(signal, "SIGWINCH", None)


def create_key_bindings(cancel_callback: Optional[Callable[[], None]]) -> KeyBindings:
    """
    Key bindings handled by the spinner.
    (The main thread is not supposed to handle any key bindings.)
    """
    kb = KeyBindings()

    @kb.add("c-l")
    def _clear(event: E) -> None:
        event.app.renderer.clear()

    if cancel_callback is not None:

        @kb.add("c-c")
        def _interrupt(_: E) -> None:
            "Kill the 'body' of the spinner, but only if we run from the main thread."
            assert cancel_callback is not None
            cancel_callback()

    return kb


_T = TypeVar("_T")


class GromSpin:
    """
    GromSpin context manager.

    Usage ::

        with GromSpin(...) as pb:
            for item in pb(data):
                ...

    :param title: Text to be displayed above the spinners. This can be a
        callable or formatted text as well.
    :param formatters: List of :class:`.Formatter` instances.
    :param bottom_toolbar: Text to be displayed in the bottom toolbar. This
        can be a callable or formatted text.
    :param style: :class:`prompt_toolkit.styles.BaseStyle` instance.
    :param key_bindings: :class:`.KeyBindings` instance.
    :param cancel_callback: Callback function that's called when control-c is
        pressed by the user. This can be used for instance to start "proper"
        cancellation if the wrapped code supports it.
    :param file: The file object used for rendering, by default `sys.stderr` is used.

    :param color_depth: `prompt_toolkit` `ColorDepth` instance.
    :param output: :class:`~prompt_toolkit.output.Output` instance.
    :param input: :class:`~prompt_toolkit.input.Input` instance.
    """

    def __init__(
        self,
        title: AnyFormattedText = None,
        formatters: Optional[Sequence[SpinFormatter]] = None,
        bottom_toolbar: AnyFormattedText = None,
        style: Optional[BaseStyle] = None,
        key_bindings: Optional[KeyBindings] = None,
        cancel_callback: Optional[Callable[[], None]] = None,
        _: Optional[TextIO] = None,
        color_depth: Optional[ColorDepth] = None,
        output: Optional[Output] = None,
        input: Optional[Input] = None,  # pylint: disable=redefined-builtin
    ) -> None:

        self.title = title
        self.formatters = formatters or create_default_spin_formatters()
        self.bottom_toolbar = bottom_toolbar
        self.spinners: List[Spinner[object]] = []
        self.style = GromThemer().get_style() if style is None else style
        self.key_bindings = key_bindings
        self.cancel_callback = cancel_callback

        # If no `cancel_callback` was given, and we're creating the spinner
        # from the main thread. Cancel by sending a `KeyboardInterrupt` to
        # the main thread.
        if (
            self.cancel_callback is None and
            threading.currentThread() == threading.main_thread()  # pylint: disable=deprecated-method
        ):

            def keyboard_interrupt_to_main_thread() -> None:
                os.kill(os.getpid(), signal.SIGINT)

            self.cancel_callback = keyboard_interrupt_to_main_thread

        # Note that we use __stderr__ as default error output, because that
        # works best with `patch_stdout`.
        self.color_depth = color_depth
        self.output = output or get_app_session().output
        self.input = input or get_app_session().input

        self._thread: Optional[threading.Thread] = None

        self._app_loop = new_event_loop()
        self._has_sigwinch = False
        self._app_started = threading.Event()

    def __enter__(self) -> "GromSpin":
        # Create UI Application.
        title_toolbar = ConditionalContainer(
            Window(
                FormattedTextControl(lambda: self.title),
                height=1,
                style="class:spinner,title",
            ),
            filter=Condition(lambda: self.title is not None),
        )

        bottom_toolbar = ConditionalContainer(
            Window(
                FormattedTextControl(
                    lambda: self.bottom_toolbar, style="class:bottom-toolbar.text"
                ),
                style="class:bottom-toolbar",
                height=1,
            ),
            filter=~is_done &  # pylint: disable=E1130
            renderer_height_is_known &
            Condition(lambda: self.bottom_toolbar is not None),
        )

        def width_for_formatter(formatter: SpinFormatter) -> AnyDimension:
            # Needs to be passed as callable (partial) to the 'width'
            # parameter, because we want to call it on every resize.
            return formatter.get_width(spin=self)

        spinner_controls = [
            Window(
                content=_SpinnerControl(self, f, self.cancel_callback),
                width=functools.partial(width_for_formatter, f),
            )
            for f in self.formatters
        ]

        self.app: Application[None] = Application(  # pylint: disable=attribute-defined-outside-init
            min_redraw_interval=0.05,
            layout=Layout(
                HSplit(
                    [
                        title_toolbar,
                        VSplit(
                            spinner_controls,
                            height=lambda: D(
                                preferred=len(self.spinners), max=len(self.spinners)
                            ),
                        ),
                        Window(),
                        bottom_toolbar,
                    ]
                )
            ),
            style=self.style,
            key_bindings=self.key_bindings,
            refresh_interval=0.3,
            color_depth=self.color_depth,
            output=self.output,
            input=self.input,
        )

        # Run application in different thread.
        def run() -> None:
            set_event_loop(self._app_loop)
            try:
                self.app.run(pre_run=self._app_started.set)
            except BaseException as e:  # pylint: disable=broad-except
                traceback.print_exc()
                print(e)

        ctx: contextvars.Context = contextvars.copy_context()

        self._thread = threading.Thread(target=ctx.run, args=(run,))
        self._thread.start()

        return self

    def __exit__(self, *a: object) -> None:
        # Wait for the app to be started. Make sure we don't quit earlier,
        # otherwise `self.app.exit` won't terminate the app because
        # `self.app.future` has not yet been set.
        self._app_started.wait()

        # Quit UI application.
        if self.app.is_running:
            self._app_loop.call_soon_threadsafe(self.app.exit)

        if self._thread is not None:
            self._thread.join()
        self._app_loop.close()

    def __call__(
        self,
        data: Optional[Iterable[_T]] = None,
        label: AnyFormattedText = "",
        remove_when_done: bool = False,
        total: Optional[int] = None,
    ) -> "Spinner[_T]":
        """
        Start a new spinner.

        :param label: Title text or description for this spinner. (This can be
            formatted text as well).
        :param remove_when_done: When `True`, hide this spinner.
        :param total: Specify the maximum value if it can't be calculated by
            calling ``len``.
        """
        spinner = Spinner(self, label=label, remove_when_done=remove_when_done)
        self.spinners.append(spinner)
        return spinner

    def invalidate(self) -> None:
        """Invalidate"""
        self.app.invalidate()


class _SpinnerControl(UIControl):
    """
    User control for the spinner.
    """

    def __init__(
        self,
        spinner: GromSpin,
        formatter: SpinFormatter,
        cancel_callback: Optional[Callable[[], None]],
    ) -> None:
        self.spinner = spinner
        self.formatter = formatter
        self._key_bindings = create_key_bindings(cancel_callback)

    def create_content(self, width: int, height: int) -> UIContent:
        items: List[StyleAndTextTuples] = []

        for pr in self.spinner.spinners:
            try:
                text = self.formatter.format(self.spinner, pr, width)
            except BaseException:  # pylint: disable=broad-except
                traceback.print_exc()
                text = "ERROR"

            items.append(to_formatted_text(text))

        def get_line(i: int) -> StyleAndTextTuples:
            return items[i]

        return UIContent(get_line=get_line, line_count=len(items), show_cursor=False)

    def is_focusable(self) -> bool:
        return True  # Make sure that the key bindings work.

    def get_key_bindings(self) -> KeyBindings:
        return self._key_bindings


_SpinnerItem_co = TypeVar("_SpinnerItem_co", covariant=True)


class Spinner(Generic[_SpinnerItem_co]):
    """
    An individual spinner (A Spin can have multiple spinners).
    """

    def __init__(
        self,
        spinner: GromSpin,
        label: AnyFormattedText = "",
        remove_when_done: bool = False,
    ) -> None:
        self.start_time = datetime.datetime.now()
        self.stop_time: Optional[datetime.datetime] = None
        self.spinner = spinner
        self._label = label
        self.remove_when_done = remove_when_done
        self._done = False

    def __enter__(self) -> "Spinner[_T]":
        return self

    def __exit__(self, *a: object) -> None:
        pass

    @property
    def label(self) -> AnyFormattedText:
        """
        Set spinner label
        """
        return self._label

    def set_label(self, value: AnyFormattedText) -> None:
        if value:
            self._label = value

    @property
    def done(self) -> bool:
        """Whether a spinner are done.

        Done spinner have been stopped (see stopped) and removed depending on
        remove_when_done value.

        Contrast this with stopped. A stopped spinner may have failed, while done spinner has reached completion.
        Grom comes with more spesialized spinner implementations, like SuccessFailureSpin.
        """
        return self._done

    def set_done(self, done: bool, label: AnyFormattedText = None) -> None:
        self._done = done
        self.set_stopped(done)

        if label:
            self._label = label

        if done and self.remove_when_done:
            self.spinner.spinners.remove(self)

    @property
    def stopped(self) -> bool:
        """Whether a spinner has been stopped.

        Stopped spinners no longer have increasing time_elapsed.

        A stopped spinner (but not done) can be used to signal that a given spinner has
        encountered an error but allows other spinners to continue
        (e.g. download X of Y failed). Given how only done spinners are removed
        (see remove_when_done) this can help aggregate failures from a large number of
        successes.

        Contrast this with done. A done spinner has reached completion.
        A stopped spinner may be terminated before completion.
        """
        return self.stop_time is not None

    def set_stopped(self, stopped: bool, label: AnyFormattedText = None) -> None:
        if label:
            self._label = label
        if stopped:
            # This spinner has not already been stopped.
            if not self.stop_time:
                self.stop_time = datetime.datetime.now()
        else:
            # Clearing any previously set stop_time.
            self.stop_time = None

    @property
    def time_elapsed(self) -> datetime.timedelta:
        """
        Return how much time has been elapsed since the start.
        """
        if self.stop_time is None:
            return datetime.datetime.now() - self.start_time
        return self.stop_time - self.start_time
