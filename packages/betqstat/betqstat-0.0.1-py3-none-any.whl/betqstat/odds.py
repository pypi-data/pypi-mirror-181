

def remove_com(odds: float, com: float):
    """Removed the commission from odds.

    Handy for calculating the true betfair back odds.

    Args:
        odds:
        com: The commission to be paid on the bet winnings.

    Returns:
      The true odds, without commission.
    """
    if not odds > 1:
        raise ValueError(
            f"The decimal odds must be grater than 1, not {odds}"
        )
    if not 0 <= com <= 0.2:
        raise ValueError(f"The commission (com) must be between 0 and 20%, not {com}")

    true_odds = (odds - 1) * (1 - com) + 1
    return round(true_odds, 6)
