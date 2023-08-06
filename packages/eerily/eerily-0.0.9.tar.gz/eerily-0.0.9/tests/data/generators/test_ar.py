import numpy as np
import pytest

from eerily.data.generators.ar import AR1Stepper, ARModelParams


@pytest.fixture
def ar_epsilon():
    class ZeroEpsilon:
        """Constant noise

        :param epsilon: the constant value to be returned
        """

        def __init__(self, epsilon=0):
            self.epsilon = epsilon

        def __next__(self):
            return self.epsilon

    return ZeroEpsilon(epsilon=0)


@pytest.fixture
def ar_params(ar_epsilon):

    model_params = ARModelParams(
        delta_t=0.1,
        phi0=0,
        phi1=1.1,
        epsilon=ar_epsilon,
        initial_state=np.array([-1]),
        variable_names=["v"],
    )

    return model_params


@pytest.fixture
def ar_stepper(ar_params):
    return AR1Stepper(model_params=ar_params)


def test_ar_stepper(ar_stepper, length):

    container = np.array([])
    for _ in range(length):
        container = np.append(container, next(ar_stepper))

    container_truth = np.array(
        [
            -1.1,
            -1.21,
            -1.331,
            -1.4641,
            -1.61051,
            -1.771561,
            -1.9487171,
            -2.14358881,
            -2.357947691,
            -2.5937424601,
        ]
    )

    np.testing.assert_allclose(container, container_truth)
