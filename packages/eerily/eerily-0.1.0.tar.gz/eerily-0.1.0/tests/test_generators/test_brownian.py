import numpy as np
import pandas as pd
import pytest

from eerily.generators.brownian import BrownianMotionParams, BrownianMotionStepper
from eerily.generators.utils.noises import GaussianNoise


@pytest.fixture
def gaussian_force(seed):
    return GaussianNoise(mu=0, std=1, seed=seed)


@pytest.fixture
def brownian_motion_params(gaussian_force):

    model_params = BrownianMotionParams(
        gamma=0,
        delta_t=0.1,
        force_densities=gaussian_force,
        initial_state=np.array([0]),
        variable_names=["v"],
    )

    return model_params


@pytest.fixture
def brownian_motion_stepper(brownian_motion_params):
    return BrownianMotionStepper(model_params=brownian_motion_params)


def test_brownian_motion_stepper(brownian_motion_stepper, length):

    container = np.array([])
    for _ in range(length):
        container = np.append(container, next(brownian_motion_stepper))

    container_truth = np.array(
        [
            0.030471707975443137,
            -0.07352670264860642,
            0.001518416932039315,
            0.09557488857116071,
            -0.09952863029422294,
            -0.2297465809804547,
            -0.21696254066372622,
            -0.24858679989808444,
            -0.25026691564851333,
            -0.3355713084058713,
        ]
    )

    np.testing.assert_allclose(container, container_truth)
