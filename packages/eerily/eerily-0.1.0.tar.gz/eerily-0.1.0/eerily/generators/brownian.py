import copy
from dataclasses import dataclass
from typing import Dict, Iterator

from eerily.generators.utils.stepper import BaseStepper, StepperModelParams


@dataclass(frozen=True)
class BrownianMotionParams(StepperModelParams):
    """
    Parameters for Brownian motion

    :param gamma: the damping factor $\gamma$ of the Brownian motion.
    :param delta_t: the minimum time step $\Delta t$.
    :param force_densities: the stochastic force densities, e.g.
        [`GaussianNoise`][eerily.generators.utils.noise.GaussianNoise].
    :param initial_state: the initial velocity $v(0)$.
    :param variable_names: variable names of the given initial condition
    """

    gamma: float
    delta_t: float
    force_densities: Iterator


class BrownianMotionStepper(BaseStepper):
    """Calculates the next step in a brownian motion.

    ??? note "Brownian Motion"

        Macroscopically, Brownian Motion can be described by the notion of random forces on the particles,

        $$\\frac{d}{dt} v(t) + \gamma v(t) = R(t),$$

        where $v(t)$ is the velocity at time $t$ and $R(t)$ is the stochastic force density from the reservoir particles.

        To simulate it numerically, we rewrite

        $$\\frac{d}{dt} v(t) + \gamma v(t) = R(t),$$

        as

        $$\Delta v (t+1) = R(t) \Delta t - \gamma v(t) \Delta t$$


    !!! example "Example Code"

        ```python
        guassian_force = GaussianForce(mu=0, std=1, seed=seed)
        bm_params = BrownianMotionParams(
            gamma=0, delta_t=0.1, force_densities=guassian_force, initial_state=np.array([0]),
            variable_names=["v"]
        )

        bms = BrownianMotionStepper(
            model_params = bm_params
        )

        next(bms)
        ```

    :param model_params: a dataclass that contains the necessary parameters for the model.
        e.g., [`BrownianMotionParams`][eerily.generators.brownian.BrownianMotionParams]
    """

    def __next__(self) -> Dict[str, float]:

        force_density = next(self.model_params.force_densities)

        v_next = (
            self.current_state
            + force_density * self.model_params.delta_t
            - self.model_params.gamma * self.current_state * self.model_params.delta_t
        )

        self.current_state = v_next

        return copy.deepcopy(self.current_state)
