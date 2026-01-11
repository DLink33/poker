import math
import os
import random

import pytest
from utils import TestUtils

from poker.card_collections import Hand
from poker.entities import Player
from poker.rules import Logic

HAND_RANKINGS = {
    0: "high card",
    1: "one pair",
    2: "two pair",
    3: "three of a kind",
    4: "straight",
    5: "flush",
    6: "full house",
    7: "four of a kind",
    8: "straight flush",
}

# Theoretical 5-card poker hand probabilities (single 5-card draw).
# Total distinct 5-card hands = 2,598,960.
# IMPORTANT:
# - "flush" excludes straight flushes
# - "straight" excludes straight flushes
EXPECTED_P = {
    "straight flush": 40 / 2_598_960,
    "four of a kind": 624 / 2_598_960,
    "full house": 3_744 / 2_598_960,
    "flush": 5_108 / 2_598_960,
    "straight": 10_200 / 2_598_960,
    "three of a kind": 54_912 / 2_598_960,
    "two pair": 123_552 / 2_598_960,
    "one pair": 1_098_240 / 2_598_960,
    "high card": 1_302_540 / 2_598_960,
}


@pytest.fixture
def random_hand() -> Hand:
    cards: list[str] = TestUtils.gen_random_hand()
    return TestUtils.make_hand(cards)


def _simulate_counts(n: int, seed: int) -> dict[str, int]:
    random.seed(seed)

    # Ensure every category exists in counts even if not observed (esp. rare ones).
    counts: dict[str, int] = {HAND_RANKINGS[i]: 0 for i in range(9)}

    player: Player = Player("Tester", hand=None)
    for _ in range(n):
        player.hand = TestUtils.make_hand(TestUtils.gen_random_hand())
        rank_idx = Logic.calc_hand_rank(player)[0]
        counts[HAND_RANKINGS[rank_idx]] += 1

    return counts


def _assert_category_within_tolerance(name: str, obs: int, n: int, z: float) -> None:
    """
    Compare observed count to expected count using a tolerance band.

    - For common events: binomial stddev sqrt(n p (1-p))
    - For rare events: use a more forgiving bound based on sqrt(lambda + 1)
      to reduce test flakiness while still catching big biases.
    """
    p = EXPECTED_P[name]
    expected = n * p  # lambda

    if expected < 25:
        tol = z * math.sqrt(expected + 1.0)
    else:
        tol = z * math.sqrt(n * p * (1.0 - p))

    lo = max(0.0, expected - tol)
    hi = expected + tol

    assert lo <= obs <= hi, (
        f"{name}: observed={obs}, expected={expected:.2f}, "
        f"allowed=[{lo:.2f}, {hi:.2f}] (n={n}, z={z})"
    )


@pytest.mark.slow
def test_hand_distribution_matches_5card_theory() -> None:
    """
    Monte-Carlo validation: with enough samples, your random dealing + ranking logic
    should match the known 5-card draw distribution.

    Override sample size if desired:
      HAND_DIST_N=500000 pytest -k distribution
    """
    n = int(os.getenv("HAND_DIST_N", "300000"))
    seed = int(os.getenv("HAND_DIST_SEED", "12345"))

    # Bigger z => less flaky. 6-sigma is generous.
    z = float(os.getenv("HAND_DIST_Z", "6.0"))

    counts = _simulate_counts(n=n, seed=seed)

    # Basic sanity check
    assert sum(counts.values()) == n

    # Ensure naming matches what we expect (catches typos / missing categories)
    assert set(counts.keys()) == set(EXPECTED_P.keys())

    # Check each category count
    for name, obs in counts.items():
        _assert_category_within_tolerance(name, obs, n=n, z=z)
