
from typing import Iterator

class GenerationRange(object):
    """
    A range-like object to be used when generating generations.
    Say that three times :P
    """
    CURRENT_GENERATION = 7

    def __init__(self, start, end):
        self._start = start
        self._end = end

    def __iter__(self) -> Iterator[int]:
        yield from range(self._start, self._end + 1)
