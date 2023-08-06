import copy
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List

import numpy as np


@dataclass(frozen=True)
class StepperModelParams:
    """Base Parameters for Stepper

    :param initial_state: the initial state, e.g., `np.array([1])`
    :param variable_name: variable names
    """

    initial_state: np.ndarray
    variable_names: List[str]


class BaseStepper(ABC):
    """A framework to evolve a DGP to the next step"""

    def __init__(self, model_params) -> None:
        self.model_params = model_params
        self.current_state = copy.deepcopy(self.model_params.initial_state)

    def __iter__(self):
        return self

    @abstractmethod
    def __next__(self):
        pass

    def get_iterator(self):
        return self.__iter__()

    def __str__(self) -> str:
        return f"Model Parameters: {self.model_params}"
