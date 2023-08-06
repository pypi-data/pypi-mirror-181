import pytest

from eerily.data.generators.events import PoissonEvents


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
    pe = PoissonEvents(rate=rate, seed=seed)

    length = 10
    events = [next(pe) for _ in range(length)]

    assert events == expected
