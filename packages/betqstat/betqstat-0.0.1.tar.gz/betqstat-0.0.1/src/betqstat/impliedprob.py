import numpy as np
import pandas as pd
from scipy.optimize import bisect
from typing import Union, Sequence, Literal, List, get_args

METHODS = Literal["multiplicative", "additive", "power", "shin"]


def _multiplicative(probs: Sequence[float]) -> np.array:
    """In this method the raw probability is rescaled by the total market probability to rescale the market to 100%.

    Args:
        probs: the inverse of the raw odds.

    Returns:
      The implied probability of each entrant, as calculated by the multiplicative method.
    """
    return probs / sum(probs)


def _additive(probs: Sequence[float]) -> np.array:
    """In this method an equal proportion is removed from each entrant to rescale the market to 100%.

    Args:
        probs: the inverse of the raw odds.

    Returns:
      The implied probability of each entrant, as calculated by the additive method.
    """
    return probs + 1 / len(probs) * (1 - sum(probs))


def _power_func(pi: Sequence[float], k: float):
    """The probability is raised to the power of a constant k.

    Args:
        pi: the inverse of the raw odds.
        k: the constant k of the power method.

    Returns:
      The implied probability of each entrant, as calculated by the power method.
    """
    return pi**k


def _power_objective(k: float, pi: Sequence[float]):
    """The objective function to optimise for the power method.

    Args:
        k: the constant k of the power method to be optimised.
        pi: the inverse of the raw odds.

    Returns:
      The objective to be optimised - as close to 100% as possible.
    """
    implied_probs = _power_func(pi=pi, k=k)
    return 1 - sum(implied_probs)


def _power(probs: Sequence[float]) -> np.array:
    """In this method the inverse of the odds is raised to a value of k to rescale the market to 100%.

    Args:
        probs: the inverse of the raw odds.

    Returns:
      The implied probability of each entrant, as calculated by the power method.
    """
    k_opt = bisect(f=_power_objective, a=0, b=100, args=probs)
    implied_probs = _power_func(pi=probs, k=k_opt)
    return implied_probs


def _shin_func(pi: Sequence[float], z: float):
    """The probability is adjusted with formula involving a constant z.

    Args:
        pi: the inverse of the raw odds.
        z: the constant z of the shin method.

    Returns:
      The implied probability of each entrant, as calculated by the shin method.
    """
    return ((z**2 + 4 * (1 - z) * pi**2 / sum(pi)) ** 0.5 - z) / (2 - 2 * z)


def _shin_objective(z: float, pi: Sequence[float]):
    """The objective function to optimise for the shin method.

    Args:
        z: the constant z of the shin method to be optimised.
        pi: the inverse of the raw odds.

    Returns:
      The objective to be optimised - as close to 100% as possible.
    """
    implied_probs = _shin_func(pi=pi, z=z)
    return 1 - sum(implied_probs)


def _shin(probs: Sequence[float]) -> np.array:
    """In this method the inverse of the odds is put through the shin formula to rescale the market to 100%.

    Args:
        probs: the inverse of the raw odds.

    Returns:
      The implied probability of each entrant, as calculated by the shin method.
    """
    z_opt = bisect(f=_shin_objective, a=0, b=10, args=probs)
    implied_probs = _shin_func(pi=probs, z=z_opt)
    return implied_probs


def get(odds: Sequence[float], method: METHODS = "power") -> np.array:
    """Calculate the implied probability of entrants in a market from their odds.

    Args:
        odds: the raw odds of every entrant in the market.
        method: the method to use to calculate the implied probabilities

    Returns:
        An array of the implied probability of each entrant.
    """
    if not len(odds) > 1:
        raise ValueError(
            'number of entrants in market (len(odds)) must greater than 1, not {odds}'
        )
    if any(odd <= 1 for odd in odds):
        raise ValueError('all odds in market must be grater than 1')
    if method not in get_args(METHODS):
        raise ValueError(f"The specified method is not valid")

    odds = np.array(odds)
    raw_probs = 1 / odds

    if method == "multiplicative":
        implied_probs = _multiplicative(probs=raw_probs)
    elif method == "additive":
        implied_probs = _additive(probs=raw_probs)
    elif method == "power":
        implied_probs = _power(probs=raw_probs)
    elif method == "shin":
        implied_probs = _shin(probs=raw_probs)

    return implied_probs


def df_apply(odds: pd.Series, method: METHODS = "power") -> pd.Series:
    """A function that can be used as by pd.DataFrame.groupby.apply to calculate implied probabilities.

    Args:
        odds: the raw odds of every entrant in the market.
        method: the method to use to calculate the implied probabilities

    Returns:
        A series of the implied probability for each entrant.
    """
    implied_probs = get(odds, method)
    return pd.Series(implied_probs, index=odds.index, dtype='float')


def df_get(
    markets: pd.DataFrame,
    market_id_col: Union[str, int, List[str], List[int]] = "race_id",
    price_col: float = "price",
    method: METHODS = "power",
) -> pd.DataFrame:
    """Calculate the implied probability of entrants in a market from their odds.

    Args:
        markets: the raw odds of every entrant in the market.
        market_id_col: the dataframe column identifying the market.
        price_col: the dataframe column containing the raw price to derive the implied probability from.
        method: the method to use to calculate the implied probabilities

    Returns:
        The original dataframe with additional columns with implied probability and standardised price.
    """
    if not isinstance(markets, pd.DataFrame):
        raise ValueError(
            f"the input markets object is not a dataframe"
        )
    if market_id_col not in markets.columns:
        raise ValueError(
            f"the specified market id column is not in the supplied dataframe"
        )
    if price_col not in markets.columns:
        raise ValueError(
            f"the specified price column is not in the supplied dataframe"
        )

    markets = markets.copy()
    markets["prob"] = markets.groupby(by=market_id_col, group_keys=False)[
        price_col
    ].apply(df_apply, method=method)
    markets["std_price"] = (1 / markets["prob"]).round(2)
    return markets
