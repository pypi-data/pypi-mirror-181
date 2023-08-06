import pytest

from eerily.generators.utils.events import PoissonEvent


@pytest.mark.parametrize(
    "rate, expected",
    [
        (0.5, [0, 1, 0, 0, 1, 0, 0, 0, 1, 1]),
        (0.1, [0, 0, 0, 0, 1, 0, 0, 0, 0, 0]),
        (0.9, [1, 1, 1, 1, 1, 0, 1, 1, 1, 1]),
    ],
)
def test_poisson_events(rate, expected):
    seed = 42
    pe = PoissonEvent(rate=rate, seed=seed)

    length = 10
    events = [next(pe) for _ in range(length)]

    assert events == expected
