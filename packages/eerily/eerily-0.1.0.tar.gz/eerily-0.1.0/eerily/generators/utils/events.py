from typing import Optional

import numpy as np


class PoissonEvent:
    """A Poisson process event generator.

    See [this notebook](https://github.com/btel/python-in-neuroscience-tutorials/blob/master/poisson_process.ipynb) for more about a Poisson process.

    ```python
    rate = 0.1
    pe = PoissonEvents(rate=rate)
    next(pe)
    ```

    :param lambda: the mean rate of the Poisson process
    :param seed: seed of the RNG for reproducibility
    """

    def __init__(self, rate: float, seed: Optional[float] = None):
        self.rate = rate
        self.rng = np.random.default_rng(seed=seed)

    def __next__(self) -> float:
        random_state = self.rng.random() <= self.rate
        return int(random_state)
