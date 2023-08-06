import copy
from dataclasses import dataclass
from typing import Any, Dict, Iterator, List, Optional, Sequence, Union

import numpy as np

from eerily.data.generators.events import PoissonEvents
from eerily.data.generators.stepper import BaseStepper, StepperModelParams


@dataclass(frozen=True)
class SpikingEventParams(StepperModelParams):
    """
    Parameters for spiking events.

    :param spike: the spiking process, e.g., Poisson process.
    :param spike_level: the level of spikes, e.g. [`GaussianNoise`][eerily.data.generators.noise.GaussianNoise] with some positve mean. This parameter determines the height of the spikes.
    :param background: the stochastic noise level, e.g. [`GaussianNoise`][eerily.data.generators.noise.GaussianNoise].
    """

    spike: Iterator
    spike_level: Iterator
    background: Iterator


class SpikingEventStepper(BaseStepper):
    """Calculates the next step in a spiking event.

    :param model_params: a dataclass that contains the necessary parameters for the model.
        e.g., [`SpikingEventParams`][eerily.data.generators.spiking.SpikingEventParams]
    """

    def __next__(self) -> Dict[str, float]:

        background = next(self.model_params.background)
        spike = next(self.model_params.spike)
        spike_level = next(self.model_params.spike_level)

        v_next = background + spike * spike_level

        self.current_state = v_next

        return copy.deepcopy(self.current_state)
