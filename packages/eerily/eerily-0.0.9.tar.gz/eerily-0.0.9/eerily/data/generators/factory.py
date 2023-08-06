from typing import Iterator


class Factory:
    """An experimental factor that generates a history based on a stepper and the given length."""

    def __init__(self):
        pass

    def __call__(self, stepper: Iterator, length: int):
        i = 0
        while i < length:
            yield next(stepper)
            i += 1
