import numpy as np
import pandas as pd
import pytest

from eerily.data.generators.elasticity import ElasticityStepper


@pytest.fixture
def seed():
    return 42


@pytest.fixture
def length():
    return 10


@pytest.fixture
def deterministic_elasticity_stepper(length):

    elasticity = [-3] * length
    prices = range(length)

    initial_condition = {"price": 0.5, "sale": 3}

    return ElasticityStepper(initial_condition=initial_condition, elasticity=elasticity, prices=prices)


def test_deterministic_elasticity_stepper(deterministic_elasticity_stepper, length):

    container = []
    for _ in range(length):
        container.append(next(deterministic_elasticity_stepper))

    container_truth = [
        {"price": 0, "sale": 4.5, "elasticity": -3},
        {"price": 1, "sale": 1.5, "elasticity": -3},
        {"price": 2, "sale": -1.5, "elasticity": -3},
        {"price": 3, "sale": -4.5, "elasticity": -3},
        {"price": 4, "sale": -7.5, "elasticity": -3},
        {"price": 5, "sale": -10.5, "elasticity": -3},
        {"price": 6, "sale": -13.5, "elasticity": -3},
        {"price": 7, "sale": -16.5, "elasticity": -3},
        {"price": 8, "sale": -19.5, "elasticity": -3},
        {"price": 9, "sale": -22.5, "elasticity": -3},
    ]

    assert container == container_truth


@pytest.fixture
def gaussian_elasticity(length, seed):

    rng = np.random.default_rng(seed=seed)
    elasticity_mean = -3
    elasticity_std = 0.5
    elasticity = rng.normal(elasticity_mean, elasticity_std, length)

    return elasticity


@pytest.fixture
def stochastic_elasticity_stepper(gaussian_elasticity, length):

    elasticity = gaussian_elasticity
    prices = range(length)

    initial_condition = {"price": 0.5, "sale": 3}

    return ElasticityStepper(initial_condition=initial_condition, elasticity=elasticity, prices=prices)


def test_stochastic_elasticity_stepper(stochastic_elasticity_stepper, length):

    container = []
    for _ in range(length):
        container.append(next(stochastic_elasticity_stepper))

    container_truth = [
        {"price": 0, "sale": 4.423820730061392, "elasticity": -2.847641460122784},
        {"price": 1, "sale": 0.9038286769411439, "elasticity": -3.519992053120248},
        {"price": 2, "sale": -1.7209457251556275, "elasticity": -2.6247744020967714},
        {"price": 3, "sale": -4.250663366960021, "elasticity": -2.529717641804393},
        {"price": 4, "sale": -8.22618096128694, "elasticity": -3.9755175943269183},
        {"price": 5, "sale": -11.877270714718097, "elasticity": -3.651089753431159},
        {"price": 6, "sale": -14.813350513134456, "elasticity": -2.9360797984163574},
        {"price": 7, "sale": -17.971471809306248, "elasticity": -3.158121296171791},
        {"price": 8, "sale": -20.979872388058393, "elasticity": -3.0084005787521444},
        {"price": 9, "sale": -24.406394351845183, "elasticity": -3.42652196378679},
    ]

    pd.testing.assert_frame_equal(pd.DataFrame(container), pd.DataFrame(container_truth), check_like=True)
