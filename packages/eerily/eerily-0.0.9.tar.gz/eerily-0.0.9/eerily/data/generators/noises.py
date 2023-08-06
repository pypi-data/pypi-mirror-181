from typing import Optional

import numpy as np


class GaussianNoise:
    """1 D Gaussian noise

    :param mu: mean of the Gaussian distribution
    :param std: standard deviation of the Gaussian distribution
    :param seed: seed of the RNG for reproducibility
    """

    def __init__(self, mu: float, std: float, seed: Optional[float] = None):
        self.mu = mu
        self.std = std
        self.rng = np.random.default_rng(seed=seed)

    def __next__(self) -> float:
        return self.rng.normal(self.mu, self.std)


class LogNormalNoise:
    """1 D lognormal noise

    :param mu: mean of the Gaussian distribution
    :param std: standard deviation of the Gaussian distribution
    :param seed: seed of the RNG for reproducibility
    """

    def __init__(self, mu: float, std: float, seed: Optional[float] = None):
        self.mu = mu
        self.std = std
        self.rng = np.random.default_rng(seed=seed)

    def __next__(self) -> float:
        return self.rng.lognormal(self.mu, self.std)


class MultiGaussianNoise:
    """A multivariate Gaussian noise

    To generate constants,

    ```python
    mge = MultiGaussianEpsilon(
        mu=np.array([1,2]), cov=np.array([
            [0, 0],
            [0, 0]
        ])
    )
    ```

    To generate independent noises,

    ```python
    mge = MultiGaussianEpsilon(
        mu=np.array([1,2]), cov=np.array([
            [1, 0],
            [0, 1]
        ])
    )
    ```

    :param mu: means of the variables
    :param cov: covariance of the variables
    :param seed: seed of the random number generator for reproducibility
    """

    def __init__(self, mu: np.ndarray, cov: np.ndarray, seed: Optional[float] = None):
        self.mu = mu
        self.cov = cov
        self.rng = np.random.default_rng(seed=seed)

    def __next__(self) -> np.ndarray:
        return self.rng.multivariate_normal(self.mu, self.cov)
