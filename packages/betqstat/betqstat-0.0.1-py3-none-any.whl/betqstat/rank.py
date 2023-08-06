import numpy as np
import pandas as pd
from typing import Sequence


def _harville(prob_perm_a: float, prob_win_j: float, sum_prob_win_a: float) -> float:
    """Generalised Harville (1973) formula to compute the ordering probability in a multi-entry competitions.

    The ordering of a multi-entry competition can be thought of as permutations of all the entrants in the competition. Let:
    n = total number of entrants in multi-entry competition
    r = the number of entrants to order i.e. 4 implies the first four runners in the race
    P = number of permutations = n!/(n-r)!

    This functions takes the probability of permutation with r-1 and computes the probability with r using Harville's method.

    Args:
        prob_perm_a: the probability of permutation a.
        prob_win_j: the win probability of entrant j.
        sum_prob_win_a: the sum of win probabilities for all entrants in the permutation a.

    Returns:
        The probability of the given permutation (finishing order), a then j.
    """
    return prob_perm_a * prob_win_j / (1 - sum_prob_win_a)


def _get_permutations(entrants: pd.DataFrame, perms: pd.DataFrame, r: int = 4, k: float = 1):
    """Takes a permutation for r-1 selections and does for r selections.

    Args:
        entrants: All the entrants in the multi-entry competition.
        perms: All the permutations with r-1 selections.
        r: The number of selections.
        k: The power to adjust the market by.

    Returns:
        All the permutations with r selections.
    """
    perms_plus_1 = pd.merge(left=perms, right=entrants.add_suffix(f"_{r}"), how="cross")
    for i in range(1, r):
        perms_plus_1 = perms_plus_1.loc[(perms_plus_1[f"index_entrant_{i}"] != perms_plus_1[f"index_entrant_{r}"])]

    market_power = sum(entrants["prob_win_entrant"]**k)
    perms_plus_1["sum_prob_win_a"] = 0
    for i in range(1, r):
        perms_plus_1["sum_prob_win_a"] += perms_plus_1[f"prob_win_entrant_{i}"]
    perms_plus_1[f"prob_first_{r}"] = perms_plus_1.apply(
        lambda e: _harville(
            prob_perm_a=e[f"prob_first_{r-1}"],
            prob_win_j=e[f"prob_win_entrant_{r}"],
            sum_prob_win_a=e["sum_prob_win_a"]
        ),
        axis=1
    )
    columns = (
            [f"index_entrant_{i}" for i in range(1, r+1)]
            + [f"prob_win_entrant_{i}" for i in range(1, r+1)]
            + [f"prob_first_{r}"]
    )
    return perms_plus_1[columns]


def harville(win_probs: Sequence[float], max_rank: int = 4, ks: Sequence[float] = None):
    """Calculates the ordering probabilities for a multi-entry competitions using the Harville (1973) method.

    Can also use the adjusted Harville method by supplying a list of k's to adjust the market by for each step.

    Args:
        win_probs: the winning probability of every entrant in the market.
        max_rank: The maximum number of rankings to compute ordering probabilities up to.
        ks: The power adjustment for each...

    Returns:
        The probability of the given permutation (finishing order), a then j.

    """
    if ks is None:
        ks = [1] * (max_rank-1)
    if not len(win_probs) >= 2:
        raise ValueError(f"The number of entrants must be greater than or equal 2")
    if not max_rank <= len(win_probs):
        raise ValueError(
            f"The max_rank must be less than or equal to the number of win probabilities supplied"
        )
    if not round(sum(win_probs), 4) == 1.0:
        raise ValueError(f"Sum of win probabilities must be equal to 1")
    if not len(ks) == (max_rank - 1):
        raise ValueError(f"The supplied list of ks must have length equal to the maximum ranking minus 1")

    entrants = pd.DataFrame(data={'prob_win_entrant': win_probs}).reset_index().rename(columns={"index": "index_entrant"})
    out = {"first_1": entrants.add_suffix("_1")}
    out["first_1"]["prob_first_1"] = out["first_1"]["prob_win_entrant_1"]
    for i in range(2, max_rank + 1):
        out[f"first_{i}"] = _get_permutations(entrants=entrants, perms=out[f"first_{i-1}"], r=i, k=ks[i-2])

    return out
