import copy
from dataclasses import dataclass
from typing import Iterator

import numpy as np

from eerily.generators.utils.stepper import BaseStepper, StepperModelParams


@dataclass(frozen=True)
class ARModelParams(StepperModelParams):
    """Parameters of our AR model,

    $$s(t+1) = \phi_0 + \phi_1 s(t) + \epsilon.$$

    :param delta_t: step size of time in each iteration
    :param phi0: pho_0 in the AR model
    :param phi1: pho_1 in the AR model
    :param epsilon: noise iterator, e.g., Gaussian noise
    :param initial_state: a dictionary of the initial state,
        e.g., `np.array([1])`
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


@dataclass(frozen=True)
class VAR1ModelParams(StepperModelParams):
    r"""Parameters of our VAR model,

    $$
    \begin{equation}
    \begin{pmatrix}s^{(1)}(t+1) \\ s^{(2)}(t+1) \end{pmatrix} =
    \begin{pmatrix} \phi^{(1)}_0 \\ \phi^{(2)}_0 \end{pmatrix} +
    \begin{pmatrix}\phi_{1, 11} & \phi_{1, 12}\\ \phi_{1, 21} & \phi_{1, 22} \end{pmatrix}
    \begin{pmatrix}s^{(1)}(t) \\ s^{(2)}(t) \end{pmatrix} +
    \begin{pmatrix}\epsilon^{(1)} \\ \epsilon^{(2)} \end{pmatrix}.
    \end{equation}
    $$

    :param delta_t: step size of time in each iteration
    :param phi0: pho_0 in the AR model
    :param phi1: pho_1 in the AR model
    :param epsilon: noise iterator, e.g., Gaussian noise
    :param initial_state: an array of the initial state, e.g., `{"s": 1}`
    """

    delta_t: float
    phi0: np.ndarray
    phi1: np.ndarray
    epsilon: Iterator


class VAR1Stepper(BaseStepper):
    """Calculate the next values using VAR(1) model.

    :param model_params: the parameters of the VAR(1) model, e.g.,
        [`VAR1ModelParams`][eerily.generators.var.VAR1ModelParams]
    """

    def __next__(self):

        epsilon = next(self.model_params.epsilon)
        phi0 = self.model_params.phi0
        phi1 = self.model_params.phi1

        self.current_state = phi0 + np.matmul(phi1, self.current_state) + epsilon

        return copy.deepcopy(self.current_state)
