import copy
from dataclasses import dataclass
from typing import Dict, Iterator

from eerily.generators.utils.stepper import BaseStepper, StepperModelParams


@dataclass(frozen=True)
class SpikingEventParams(StepperModelParams):
    """
    Parameters for spiking events.

    :param spike: the spiking process, e.g., Poisson process using
        [`PoissonEvents`][eerily.generators.utils.events.PoissonEvents].
    :param spike_level: the level of spikes, e.g.
        [`GaussianNoise`][eerily.generators.utils.noise.GaussianNoise]
        with some positve mean. This parameter determines the height of the spikes.
    :param background: the stochastic noise level, e.g.
        [`GaussianNoise`][eerily.generators.utils.noise.GaussianNoise].
    """

    spike: Iterator
    spike_level: Iterator
    background: Iterator

    def __post_init__(self):
        if self.initial_state is None:
            self.initial_state = 0
        if self.variable_names is None:
            self.variable_names = ["event"]


class SpikingEventStepper(BaseStepper):
    """Calculates the next step in a spiking event.

    :param model_params: a dataclass that contains the necessary parameters for the model.
        e.g., [`SpikingEventParams`][eerily.generators.spiking.SpikingEventParams]
    """

    def __next__(self) -> Dict[str, float]:

        background = next(self.model_params.background)
        spike = next(self.model_params.spike)
        spike_level = next(self.model_params.spike_level)

        v_next = background + spike * spike_level

        self.current_state = v_next

        return copy.deepcopy(self.current_state)
