import copy
from typing import Dict, Iterator, Optional, Sequence, Union

from loguru import logger

from eerily.data.generators.stepper import BaseStepper


class ElasticityStepper(BaseStepper):
    """Generates the next time step for an given initial condition.

    We use the following formula to generate the data

    $$
    \ln Q' = \ln Q + \epsilon (\ln P' - \ln P)
    $$

    Define new log transformed variables to make this a linear relation

    $$
    y' = y + \epsilon (x' - x).
    $$

    For example, with initial condition

    ```
    initial_condition = {"price": 0, "sales": 10}
    ```

    For a deterministic model, we have

    ```python
    length = 10
    elasticity = [-3] * length
    prices = range(length)
    initial_condition = {"price: 0.5, "sale": 3}

    es = ElasticityStepper(
        initial_condition=initial_condition,
        elasticity=elasticity,
        prices=prices
    )

    next(es)
    ```

    !!! warning "Initial Condition"
        Initial condition is a dictionary with at least two keys `sale` and `price`.

        Note that the initial condition is NOT returned in the iterator.

    """

    def __init__(
        self,
        initial_condition: Dict[str, float],
        elasticity: Union[Iterator, Sequence],
        prices: Union[Iterator, Sequence],
        length: Optional[int] = None,
    ):
        self.initial_condition = copy.deepcopy(initial_condition)
        self.current_state = copy.deepcopy(initial_condition)
        self.elasticity = elasticity
        self.prices = prices

        self.length = length

        if not isinstance(self.prices, Iterator):
            self.length = len(self.prices)
            self.prices = iter(self.prices)

        if not isinstance(self.elasticity, Iterator):
            elasticity_length = len(self.elasticity)
            self.elasticity = iter(self.elasticity)
            if (self.length is not None) and (elasticity_length != self.length):
                logger.warning(
                    f"elasticity length {elasticity_length} is different "
                    f"from prices length {self.length}; "
                    "Setting length to the min of the two."
                )
            self.length = min(self.length, elasticity_length)

    def __iter__(self):
        return self

    def __next__(self):

        price = next(self.prices)
        elasticity = next(self.elasticity)
        sale = self.current_state["sale"] + elasticity * (price - self.current_state["price"])

        self.current_state["sale"] = sale
        self.current_state["price"] = price
        self.current_state["elasticity"] = elasticity

        return copy.deepcopy(self.current_state)

    def __repr__(self) -> str:
        return (
            "ElasticityStepper: \n"
            f"initial_condition: {self.initial_condition}\n"
            f"current_state: {self.current_state}"
        )
