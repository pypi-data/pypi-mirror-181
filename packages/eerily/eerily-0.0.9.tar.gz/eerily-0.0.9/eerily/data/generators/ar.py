import copy
from dataclasses import dataclass
from typing import Dict, Iterator, List

import numpy as np

from eerily.data.generators.stepper import BaseStepper, StepperModelParams


@dataclass(frozen=True)
class ARModelParams(StepperModelParams):
    """Parameters of our AR model,

    $$s(t+1) = \phi_0 + \phi_1 s(t) + \epsilon.$$

    :param delta_t: step size of time in each iteration
    :param phi0: pho_0 in the AR model
    :param phi1: pho_1 in the AR model
    :param epsilon: noise iterator, e.g., Gaussian noise
    :param initial_state: a dictionary of the initial state, e.g., `np.array([1])`
    :param variable_name: variable names
    """

    delta_t: float
    phi0: float
    phi1: float
    epsilon: Iterator


class AR1Stepper(BaseStepper):
    """Stepper that calculates the next step in time in an AR model

    :param model_params: parameters for the AR model
    """

    def __next__(self):
        epsilon = next(self.model_params.epsilon)

        next_s = self.model_params.phi0 + self.model_params.phi1 * self.current_state + epsilon
        self.current_state = next_s

        return copy.deepcopy(self.current_state)
