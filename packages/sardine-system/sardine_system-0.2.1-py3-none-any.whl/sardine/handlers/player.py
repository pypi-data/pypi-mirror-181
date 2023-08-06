from dataclasses import dataclass
from typing import Any, Callable, Optional, ParamSpec, TypeVar

from ..base import BaseHandler
from ..handlers.sender import Number, NumericElement, Sender
from ..scheduler import AsyncRunner
from ..utils import alias_param, get_snap_deadline, lerp

__all__ = ("Player",)

P = ParamSpec("P")
T = TypeVar("T")


@dataclass
class PatternInformation:
    sender: Sender
    send_method: Callable[P, T]
    args: tuple[Any]
    kwargs: dict[str, Any]
    period: NumericElement
    iterator: Optional[Number]
    divisor: NumericElement
    rate: NumericElement
    snap: Number
    timespan: Optional[float]


class Player(BaseHandler):

    """
    Players are holders used to support one-line specialised swimming functions. Many
    instances of 'Player' are injected in globals() at boot time as a way to provide a
    quick interface for the user to output musical and data patterns. Players are han-
    dling the whole lifetime of a pattern, from its initial entry in the scheduler to
    its death when the silence() or panic() method is called.
    """

    def __init__(self, name: str):
        super().__init__()
        self._name = name
        self.runner = AsyncRunner(name=name)
        self.iterator: Number = 0
        self._iteration_span: Number = 1
        self._period: int | float = 1.0

    def fit_period_to_timespan(self, period: NumericElement, timespan: float):
        """
        Fit a given period to a certain timestamp (forcing a pattern to have a fixed
        duration. This feature can be useful for preventing users from creating loops
        that will phase out too easily.
        """

        if isinstance(period, (int, float)):
            return lerp(period, 0, period, 0, timespan)

        period = self.env.parser.parse(period)
        period = list(map(lambda x: lerp(x, 0, sum(period), 0, timespan), period))
        return period

    @staticmethod
    @alias_param(name="period", alias="p")
    @alias_param(name="iterator", alias="i")
    @alias_param(name="divisor", alias="d")
    @alias_param(name="rate", alias="r")
    @alias_param(name="timespan", alias="span")
    def play(
        sender: Sender,
        send_method: Callable[P, T],
        *args: P.args,
        timespan: Optional[float] = None,
        period: NumericElement = 1,
        iterator: Optional[Number] = None,
        divisor: NumericElement = 1,
        rate: NumericElement = 1,
        snap: Number = 0,
        **kwargs: P.kwargs,
    ):
        """Entry point of a pattern into the Player"""

        return PatternInformation(
            sender,
            send_method,
            args,
            kwargs,
            period,
            iterator,
            divisor,
            rate,
            snap,
            timespan,
        )

    def __rshift__(self, pattern: Optional[PatternInformation]) -> None:
        """
        This method acts as a cosmetic disguise for feeding PatternInformation into a
        given player. Its syntax is inspired by FoxDot (Ryan Kirkbride), another very
        popular live coding library.
        """
        if pattern is not None and pattern.timespan is not None:
            pattern.period = self.fit_period_to_timespan(
                pattern.period, pattern.timespan
            )
        self.push(pattern)

    def get_new_period(self, pattern: PatternInformation) -> Number:
        """Get period value for the current cycle"""
        for message in pattern.sender.pattern_reduce(
            {"period": pattern.period},
            self.iterator,
            pattern.divisor,
            pattern.rate,
            use_divisor_to_skip=False,
        ):
            return message["period"]
        return 1

    def func(
        self,
        pattern: PatternInformation,
        p: NumericElement = 1,  # pylint: disable=invalid-name,unused-argument
    ) -> None:
        """Central swimming function defined by the player"""
        if pattern.iterator is not None:
            self.iterator = pattern.iterator
            pattern.iterator = None

        pattern.send_method(
            *pattern.args,
            **pattern.kwargs,
            iterator=self.iterator,
            divisor=pattern.divisor,
            rate=pattern.rate,
        )

        self.iterator += self._iteration_span
        period = self.get_new_period(pattern)
        self.again(pattern=pattern, p=period)

    def push(self, pattern: Optional[PatternInformation]):
        """
        Managing lifetime of the pattern, similar to managing a swimming function
        manually. If PatternInformation is hot-swapped by None, the Player will stop
        scheduling its internal function, defined in self.func.
        """
        # This is a local equivalent to the silence() function.
        if pattern is None:
            return self.env.scheduler.stop_runner(self.runner)
        elif not self.runner.is_running():
            # Assume we are queuing the first state
            self.iterator = 0

        # Forcibly reset the interval shift back to 0 to make sure
        # the new pattern can be synchronized
        self.runner.interval_shift = 0.0

        period = self.get_new_period(pattern)

        deadline = get_snap_deadline(self.env.clock, pattern.snap)
        self.runner.push_deferred(deadline, self.func, pattern=pattern, p=period)

        self.env.scheduler.start_runner(self.runner)
        self.runner.reload()

    def again(self, *args, **kwargs):
        self.runner.update_state(*args, **kwargs)
        self.runner.swim()
