import numpy as np
import pytest

from eerily.generators.spiking import SpikingEventParams, SpikingEventStepper
from eerily.generators.utils.events import PoissonEvent
from eerily.generators.utils.noises import LogNormalNoise


@pytest.mark.parametrize(
    ("spike_rate," "spike_level_mu,spike_level_std," "background_mu,background_std," "expected"),
    [
        (
            0.5,
            1.7,
            0.05,
            1.5,
            0.1,
            [
                4.62035577,
                9.23559839,
                4.83095958,
                4.92368125,
                8.65248086,
                3.93449308,
                4.53935095,
                4.34217659,
                9.94351653,
                9.36061423,
            ],
        )
    ],
)
def test_spiking_event_stepper(spike_rate, spike_level_mu, spike_level_std, background_mu, background_std, expected):

    seed = 42

    spike = PoissonEvent(rate=spike_rate, seed=seed)
    spike_noise = LogNormalNoise(mu=spike_level_mu, std=spike_level_std, seed=seed)
    background = LogNormalNoise(mu=background_mu, std=background_std, seed=seed)

    sep = SpikingEventParams(
        initial_state=0,
        variable_names=["event"],
        spike=spike,
        spike_level=spike_noise,
        background=background,
    )

    se = SpikingEventStepper(model_params=sep)

    length = 10

    values = np.array([next(se) for _ in range(length)])
    expected = np.array(expected)

    np.testing.assert_allclose(values, expected)
