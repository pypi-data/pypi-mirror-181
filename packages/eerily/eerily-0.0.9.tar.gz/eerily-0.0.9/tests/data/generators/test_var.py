import numpy as np
import pytest

from eerily.data.generators.var import VAR1ModelParams, VAR1Stepper


@pytest.fixture
def var_epsilon():
    class ConstantEpsilon:
        """Constant noise

        :param epsilon: the constant value to be returned
        """

        def __init__(self, epsilon=0):
            self.epsilon = epsilon

        def __next__(self):
            return self.epsilon

    return ConstantEpsilon(epsilon=np.array([0, 0]))


@pytest.fixture
def var_params(var_epsilon):

    model_params = VAR1ModelParams(
        delta_t=0.01,
        phi0=np.array([0.1, 0.1]),
        phi1=np.array([[0.5, -0.25], [-0.35, 0.45 + 0.2]]),
        epsilon=var_epsilon,
        initial_state=np.array([1, 0]),
        variable_names=["s1", "s2"],
    )

    return model_params


@pytest.fixture
def var_stepper(var_params):
    return VAR1Stepper(model_params=var_params)


def test_var_stepper(var_stepper, length):

    container = []
    for _ in range(length):
        container.append(next(var_stepper).tolist())

    container = np.array(container)

    container_truth = np.array(
        [
            [6.00000000e-01, -2.50000000e-01],
            [4.62500000e-01, -2.72500000e-01],
            [3.99375000e-01, -2.39000000e-01],
            [3.59437500e-01, -1.95131250e-01],
            [3.28501562e-01, -1.52638437e-01],
            [3.02410391e-01, -1.14190531e-01],
            [2.79752828e-01, -8.00674820e-02],
            [2.59893285e-01, -4.99573532e-02],
            [2.42435981e-01, -2.34349292e-02],
            [2.27076723e-01, -8.52971532e-05],
        ]
    )

    np.testing.assert_allclose(container, container_truth)
