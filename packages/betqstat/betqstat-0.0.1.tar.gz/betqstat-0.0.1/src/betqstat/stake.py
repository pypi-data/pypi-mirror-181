import math
from typing import Literal, get_args


STAKE_TYPES = Literal["cash", "bonus"]


def _smallest_denominator(value: float, smallest_denominator: float = 0.01):
    """Rounds a value up to the smallest denominator.

    Args:
      value: The value to be rounded.
      smallest_denominator: The smallest desired denominator.

    Returns:
      The final value rounded up to the closest cent.
    """
    if value < smallest_denominator:
        value = math.ceil(value / smallest_denominator) * smallest_denominator
    return math.ceil(value * 100) / 100.00


def fixed_flat_amount(stake_amount: float, min_stake: float = 0.01):
    """Staking a fixed amount.

    Args:
      stake_amount: The amount to place on the bet.
      min_stake: The minimum allowable stake, values smaller than this will be rounded up.

    Returns:
      The stake amount to place on the bet.
    """
    if not stake_amount > 0:
        raise ValueError(
            f"The stake of the bet (stake_amount) must be greater than 0, not {stake_amount}"
        )
    stake = round(stake_amount, 2)
    return _smallest_denominator(value=stake, smallest_denominator=min_stake)


def fixed_to_win(win_amount: float, odds: float, min_stake: float = 0.01):
    """Staking to win a fixed amount.

    Args:
      win_amount: The amount to bet to win.
      odds: The decimal odds the bet is placed at.
      min_stake: The minimum allowable stake, values smaller than this will be rounded up.

    Returns:
      The stake amount to place on the bet.
    """
    if not win_amount > 0:
        raise ValueError(
            f"The win amount of the bet (stake_amount) must be greater than 0, not {win_amount}"
        )
    if not odds > 1:
        raise ValueError(f"The decimal odds must be grater than 1, not {odds}")
    stake = win_amount / (odds - 1)
    return _smallest_denominator(value=stake, smallest_denominator=min_stake)


def proportional_flat_amount(bankroll: float, proportion: float, min_stake: float = 0.01):
    """Staking a flat proportional amount of the bankroll.

    Args:
      bankroll: The current bankroll size.
      proportion: The proportion of the bankroll to bet.
      min_stake: The minimum allowable stake, values smaller than this will be rounded up.

    Returns:
      The stake amount to place on the bet.
    """
    if not bankroll > 0:
        raise ValueError(f"Bankroll must be greater than 0, not {bankroll}")
    if not 0 <= proportion <= 1:
        raise ValueError(
            f"The proportion of bankroll (proportion) must be between 0 and 1, not {proportion}"
        )
    stake = bankroll * proportion
    return _smallest_denominator(value=stake, smallest_denominator=min_stake)


def proportional_to_win(bankroll: float, proportion: float, odds: float, min_stake: float = 0.01):
    """Staking to win a proportional amount of the bankroll.

    Args:
      bankroll: The current bankroll size.
      proportion: The proportion of the bankroll to bet.
      odds: The decimal odds the bet is placed at.
      min_stake: The minimum allowable stake, values smaller than this will be rounded up.

    Returns:
      The stake amount to place on the bet.
    """
    if not bankroll > 0:
        raise ValueError(f"Bankroll must be greater than 0, not {bankroll}")
    if not 0 <= proportion <= 1:
        raise ValueError(
            f"The proportion of bankroll (proportion) must be between 0 and 1, not {proportion}"
        )

    win_amount = bankroll * proportion
    stake = win_amount / (odds - 1)
    return _smallest_denominator(value=stake, smallest_denominator=min_stake)


def kelly(bankroll: float, odds: float, prob: float, partial: float, min_stake: float = 0.01):
    """Staking based on the Kelly Criterion.

    Args:
      bankroll: The current bankroll size.
      odds: The decimal odds the bet is placed at.
      prob: The estimated "true" probability of the bet being paid out.
      partial: the proportion of kelly staking to bet.
      min_stake: The minimum allowable stake, values smaller than this will be rounded up.

    Returns:
      The stake amount to place on the bet.
    """
    if not bankroll > 0:
        raise ValueError(f"Bankroll must be greater than 0, not {bankroll}")
    if not odds > 1:
        raise ValueError(f"The decimal odds must be grater than 1, not {odds}")
    if not 0 <= prob <= 1:
        raise ValueError(
            f"The probability the bet pays out (prob) must be between 0 and 1, not {prob}"
        )
    if not 0 <= partial <= 1:
        raise ValueError(
            f"The proportion of kelly staking to bet (partial) must be between 0 and 1, not {partial}"
        )

    # kelly criterion
    b = odds - 1
    p = prob
    q = 1 - prob
    f = (b * p - q) / b
    stake = f * bankroll * partial
    return _smallest_denominator(value=stake, smallest_denominator=min_stake)


def dutch_lay(
    back_stake: float,
    back_odds: float,
    lay_odds: float,
    lay_com: float,
    back_com: float = 0,
    back_type: STAKE_TYPES = "cash",
):
    """For a given back bet, calculates the amount to lay to ensure same outcome no matter the outcome.

    Args:
        back_stake:
        back_odds:
        back_com:
        lay_odds:
        lay_com:
        back_type:

    Returns:
      The stake amount to place on the lay bet, the liability of the lay bet and the result no matter the outcome.
    """
    if not back_stake > 0:
        raise ValueError(
            f"The stake of the back bet (back_stake) must be greater than 0, not {back_stake}"
        )
    if not back_odds > 1:
        raise ValueError(
            f"The decimal back odds must be grater than 1, not {back_odds}"
        )
    if not lay_odds > 1:
        raise ValueError(f"The decimal lay odds must be grater than 1, not {lay_odds}")
    if back_type not in get_args(STAKE_TYPES):
        raise ValueError(f"The specified back stake type (back_type) is not valid")
    if not 0 <= back_com <= 0.2:
        raise ValueError(f"The back commission (back_com) must be between 0 and 20%, not {back_com}")
    if not 0 <= lay_com <= 0.2:
        raise ValueError(f"The lay commission (lay_com) must be between 0 and 20%, not {lay_com}")

    # back side
    back_true_odds = (back_odds - 1)*(1 - back_com) + 1
    back_win = (back_true_odds - 1) * back_stake
    if back_type == 'bonus':
        back_lose = 0
    else:
        back_lose = -1 * back_stake

    # lay side
    # lay_win = lay_stake * (1 - lay_com)
    # lay_lose = - lay_stake * (lay_odds - 1)

    # dutch amount
    # solve back_win + lay_lose = back_lose + lay_win
    lay_stake = (back_win - back_lose)/(lay_odds - lay_com)
    lay_stake = _smallest_denominator(lay_stake)
    lay_lose = -1 * lay_stake * (lay_odds - 1)
    result = back_win + lay_lose
    return lay_stake, round(lay_lose, 2), round(result, 2)
