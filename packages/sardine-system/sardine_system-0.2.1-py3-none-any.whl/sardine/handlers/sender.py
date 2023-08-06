import asyncio
from math import floor
from typing import Callable, Generator, ParamSpec, TypeVar, Union

from ..base import BaseHandler
from ..utils import maybe_coro

__all__ = ("Sender",)

P = ParamSpec("P")
T = TypeVar("T")

Number = Union[float, int]
ReducedElement = TypeVar("ReducedElement")
RecursiveElement = Union[ReducedElement, list]  # assume list is list[RecursiveElement]
ParsableElement = Union[RecursiveElement, str]

# Sub-types of ParsableElement
NumericElement = Union[Number, list, str]
StringElement = Union[str, list]  # assume list is list[StringElement]

Pattern = dict[str, list[ParsableElement]]
ReducedPattern = dict[str, ReducedElement]


def _maybe_index(val: RecursiveElement, i: int) -> RecursiveElement:
    if not isinstance(val, list):
        return val

    length = len(val)
    return val[i % length]


def _maybe_length(val: RecursiveElement) -> int:
    if isinstance(val, list):
        return len(val)
    return 0


class Sender(BaseHandler):

    """
    Handlers can inherit from 'Sender' if they are in charge of some output operation.
    Output operations in Sardine generally involve some amount of pattern parsing and
    monophonic/polyphonic message composition. This class implements most of the inter-
    nal behavior necessary for patterning. Each handler rely on these methods in the
    final 'send' method called by the user.

    pattern_element: return the right index number for the pattern.
    reduce_polyphonic_message: turn any dict pattern into a list of patterns.
    pattern_reduce: reduce a pattern to a dictionary of values corresponding to iterator
                    index.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._timed_tasks: set[asyncio.Task] = set()

    def call_timed(
        self,
        deadline: float,
        func: Callable[P, T],
        *args: P.args,
        **kwargs: P.kwargs,
    ) -> None:
        """Schedules the given (a)synchronous function to be called.

        Senders should always use this method to properly account for time shift.
        """

        async def scheduled_func():
            await self.env.sleeper.sleep_until(deadline)
            await maybe_coro(func, *args, **kwargs)

        task = asyncio.create_task(scheduled_func())
        self._timed_tasks.add(task)
        task.add_done_callback(self._timed_tasks.discard)

    @staticmethod
    def pattern_element(
        val: RecursiveElement,
        iterator: Number,
        divisor: Number,
        rate: Number,
    ) -> RecursiveElement:
        """Joseph Enguehard's algorithm for solving iteration speed"""
        # For simplicity, we're allowing non-sequences to be passed through
        if not isinstance(val, list):
            return val

        length = len(val)
        if length > 0:
            i = floor(iterator * rate / divisor) % length
            return val[i]
        raise ValueError(f"Cannot pattern an empty sequence: {val!r}")

    def pattern_reduce(
        self,
        pattern: Pattern,
        iterator: Number,
        divisor: NumericElement = 1,
        rate: NumericElement = 1,
        *,
        use_divisor_to_skip: bool = True,
    ) -> Generator[ReducedPattern, None, None]:
        """Reduces a pattern to an iterator yielding subpatterns.

        First, any string values are parsed using the fish bowl's parser.
        Afterwards, if the pattern is a dictionary where none of its values
        are lists, the pattern is wrapped in a list and returned, ignoring
        the iterator/divisor/rate parameters. For example::

            >>> pat = {"note": 60, "velocity": 100}
            >>> list(sender.pattern_reduce(pat, 0, 1, 1))
            [{'note': 60, 'velocity': 100}]

        If it is a monophonic pattern, i.e. a dictionary where one or more
        of its values are lists, the corresponding element of those lists
        are indexed using the `pattern_element()` method which implements
        Joseph Enguehard's algorithm::

            >>> pat = {"note": [60, 70, 80, 90], "velocity": 100}
            >>> for i in range(1, 4):
            ...     list(sender.pattern_reduce(pat, i, 2, 3))
            [{'note': 70, 'velocity': 100}]
            [{'note': 90, 'velocity': 100}]
            [{'note': 60, 'velocity': 100}]

        If it is a polyphonic pattern, i.e. a dictionary where one or more
        of the values indexed by the above algorithm are also lists, the
        elements of each list are paired together into several reduced patterns.
        The number of messages is determined by the length of the longest list.
        Any lists that are shorter than the longest list will repeat its
        elements from the start to match the length of the longest list.
        Any values that are not lists are simply repeated.

        When `use_divisor_to_skip` is True and the `divisor` is a number
        other than 1, patterns are only generated if the iterator is
        divisible by the divisor, and will otherwise yield zero messages.
        """
        # TODO: more examples for pattern_reduce()
        # TODO: document pattern_reduce() arguments
        def maybe_parse(val: ParsableElement) -> RecursiveElement:
            if isinstance(val, str):
                return self.env.parser.parse(val)
            return val

        if any(isinstance(n, (list, str)) for n in (divisor, rate)):
            divisor, rate = next(
                self.pattern_reduce({"divisor": divisor, "rate": rate}, iterator)
            ).values()

        if use_divisor_to_skip and iterator % divisor != 0:
            return

        pattern = {k: maybe_parse(v) for k, v in pattern.items()}

        for k, v in pattern.items():
            pattern[k] = self.pattern_element(v, iterator, divisor, rate)

        if not any(isinstance(v, list) for v in pattern.values()):
            # Base case where we have a monophonic message
            yield pattern

        # For polyphonic messages, recursively reduce them
        # to a list of monophonic messages
        max_length = max(_maybe_length(v) for v in pattern.values())
        for i in range(max_length):
            sub_pattern = {k: _maybe_index(v, i) for k, v in pattern.items()}
            yield from self.pattern_reduce(sub_pattern, iterator, divisor, rate)
