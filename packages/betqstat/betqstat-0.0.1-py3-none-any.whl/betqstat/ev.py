from typing import Literal, get_args


STAKE_TYPES = Literal["cash", "bonus"]


def bet_standard(prob: float, stake: float, odds: float) -> float:
    """Calculates the expected value of a standard bet.

    Args:
      prob: The true probability of the bet being paid out, must be between 0 and 1.
      stake: The stake placed on the bet.
      odds: The decimal odds the bet is placed at.

    Returns:
      The expected value of the bet.
    """
    if not 0 <= prob <= 1:
        raise ValueError(
            f"The probability the bet pays out (prob) must be between 0 and 1, not {prob}"
        )

    win_result = stake * (odds - 1)
    win_prob = prob
    lose_result = -1 * stake
    lose_prob = 1 - prob
    return win_prob * win_result + lose_prob * lose_result


def bet_bonus(prob: float, stake: float, odds: float) -> float:
    """Calculates the expected value of a bonus bet.

    Assumes the bonus bet stake is not returned.

    Args:
      prob: The true probability of the bet being paid out, must be between 0 and 1.
      stake: The bonus stake placed on the bet.
      odds: The decimal odds the bet is placed at.

    Returns:
      The expected value of the bet.
    """
    if not 0 <= prob <= 1:
        raise ValueError(
            f"The probability the bet pays out (prob) must be between 0 and 1, not {prob}"
        )

    win_result = stake * (odds - 1)
    win_prob = prob
    lose_result = 0
    lose_prob = 1 - prob
    return win_prob * win_result + lose_prob * lose_result


def bet_stake_refund(
    prob: float,
    stake: float,
    odds: float,
    prob_refund: float,
    max_refund: float,
    type_refund: STAKE_TYPES = "bonus",
    bonus_em: float = 0.6,
) -> float:
    """Calculates the expected value of a bet, where the stake is returned if the bet loses and some condition.

    A common example is the promotion "bonus back 2nd or 3rd", where a win bet stake is refunded in bonus bets.

    Args:
      prob: The true probability of the bet being paid out, must be between 0 and 1.
      stake: The stake placed on the bet.
      odds: The decimal odds the bet is placed at.
      prob_refund: The true probability of the refund occurring, must be between 0 and 1.
      max_refund: The maximum amount that will be refunded.
      type_refund: The stake type to be refunded, "cash" or "bonus".
      bonus_em: The expected margin of a bonus bet.

    Returns:
      The expected value of the bet.
    """
    if not 0 <= prob <= 1:
        raise ValueError(
            f"The probability the bet pays out (prob) must be between 0 and 1, not {prob}"
        )
    if not 0 <= prob_refund <= 1:
        raise ValueError(
            f"The probability of the bet being refunded (prob_refund) must be between 0 and 1, not {prob_refund}"
        )
    if not 0 <= prob + prob_refund <= 1:
        raise ValueError(
            f"The probability the bet pays out or is refunded "
            f"(prob + prob_refund) must be between 0 and 1, not {prob + prob_refund}"
        )
    if type_refund not in get_args(STAKE_TYPES):
        raise ValueError(f"The specified type of refund (type_refund) is not valid")

    win_result = stake * (odds - 1)
    win_prob = prob
    refund_amount = min(stake, max_refund)
    refund_result = -1 * stake + refund_amount * (
        bonus_em if type_refund == 'bonus' else 1
    )
    refund_prob = prob_refund
    lose_result = -1 * stake
    lose_prob = 1 - prob - refund_prob
    return win_prob * win_result + refund_prob * refund_result + lose_prob * lose_result


def bet_double_winnings(
    prob: float,
    stake: float,
    odds: float,
    max_double: float,
    type_double: STAKE_TYPES = "bonus",
    bonus_em: float = 0.6,
) -> float:
    """Calculates the expected value of a bet, where the winnings are doubled.

    A common example is the promotion "double your winnings in bonus bets".

    Args:
      prob: The true probability of the bet being paid out, must be between 0 and 1.
      stake: The stake placed on the bet.
      odds: The decimal odds the bet is placed at.
      max_double: The maximum amount that will be doubled.
      type_double: The stake type to be paid out for the double winnings, "cash" or "bonus".
      bonus_em: The expected margin of a bonus bet.

    Returns:
      The expected value of the bet.
    """
    if not 0 <= prob <= 1:
        raise ValueError(
            f"The probability the bet pays out (prob) must be between 0 and 1, not {prob}"
        )
    if type_double not in get_args(STAKE_TYPES):
        raise ValueError(f"The specified type of refund (type_refund) is not valid")

    winnings_amount = min(stake * (odds - 1), max_double)
    win_result = stake * (odds - 1) + winnings_amount * (
        bonus_em if type_double == 'bonus' else 1
    )
    win_prob = prob
    lose_result = -1 * stake
    lose_prob = 1 - prob
    return win_prob * win_result + lose_prob * lose_result


def bet_extra_chance(
    prob: float,
    stake: float,
    odds: float,
    prob_extra_but_lose: float,
    max_stake_extra: float = None,
) -> float:
    """Calculates the expected value of a bet, where an extra chance of winning the bet is given.

    Common examples include "early payout if your team leads at half-time" or "protest payout" or "if your fighter
    loses by split decision, you'll be paid out as a winner".

    Args:
      prob: The true probability of the bet being paid out normally as a winner, must be between 0 and 1.
      stake: The stake placed on the bet.
      odds: The decimal odds the bet is placed at.
      prob_extra_but_lose: The true probability of the bet being paid because of the extra condition but the main bet
        going on to lose, must be between 0 and 1.
      max_stake_extra: The maximum stake that will be paid out for the extra condition. Optional, if there is no max stake.

    Returns:
      The expected value of the bet.
    """
    if not 0 <= prob <= 1:
        raise ValueError(
            f"The probability the bet pays out (prob) must be between 0 and 1, not {prob}"
        )
    if not 0 <= prob_extra_but_lose <= 1:
        raise ValueError(
            f"The probability of the extra chance of the bet being paid out early "
            f"(prob_extra_but_lose) must be between 0 and 1, not {prob_extra_but_lose}"
        )
    if not 0 <= prob + prob_extra_but_lose <= 1:
        raise ValueError(
            f"The probability the bet pays out normally or by extra chance "
            f"(prob + prob_extra_but_lose) must be between 0 and 1, not {prob + prob_extra_but_lose}"
        )

    if max_stake_extra is None:
        max_stake_extra = stake

    win_result = stake * (odds - 1)
    win_prob = prob
    win_extra_stake = min(stake, max_stake_extra)
    win_extra_result = -1 * stake + win_extra_stake * (odds - 1)
    win_extra_prob = prob_extra_but_lose
    lose_result = -1 * stake
    lose_prob = 1 - prob - prob_extra_but_lose
    return (
        win_prob * win_result
        + win_extra_prob * win_extra_result
        + lose_prob * lose_result
    )
