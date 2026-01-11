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


def _format_distribution(counts: dict[str, int], n: int) -> str:
    rows = []
    for name, count in counts.items():
        pct = (count / n) * 100.0
        exp_pct = EXPECTED_P[name] * 100.0
        rows.append((name, count, pct, exp_pct))

    # Sort by observed % descending
    rows.sort(key=lambda r: r[2], reverse=True)

    name_w = max(len(r[0]) for r in rows)
    lines = [
        f"{'hand type':<{name_w}}  {'obs %':>10}  {'exp %':>10}  {'obs':>10}  {'exp':>10}",
        f"{'-' * name_w}  {'-' * 10}  {'-' * 10}  {'-' * 10}  {'-' * 10}",
    ]
    for name, obs, obs_pct, exp_pct in rows:
        exp = n * (exp_pct / 100.0)
        lines.append(
            f"{name:<{name_w}}  {obs_pct:10.4f}  {exp_pct:10.4f}  {obs:10d}  {exp:10.1f}"
        )
    return "\n".join(lines)


@pytest.mark.slow
def test_hand_distribution_matches_5card_theory() -> None:
    n = int(os.getenv("HAND_DIST_N", "300000"))
    seed = int(os.getenv("HAND_DIST_SEED", "12345"))
    z = float(os.getenv("HAND_DIST_Z", "6.0"))

    # 0 = never print, 1 = print on fail, 2 = always print
    print_mode = int(os.getenv("HAND_DIST_PRINT", "1"))

    counts = _simulate_counts(n=n, seed=seed)

    if print_mode == 2:
        print("\n" + _format_distribution(counts, n))

    assert sum(counts.values()) == n
    assert set(counts.keys()) == set(EXPECTED_P.keys())

    try:
        for name, obs in counts.items():
            _assert_category_within_tolerance(name, obs, n=n, z=z)
    except AssertionError:
        if print_mode >= 1:
            print("\n=== HAND DISTRIBUTION (observed vs expected) ===")
            print(f"n={n}, seed={seed}, z={z}")
            print(_format_distribution(counts, n))
        raise


@pytest.mark.parametrize(
    "hand_factory, expected_rank",
    [
        (TestUtils.gen_random_high_card, 0),
        (TestUtils.gen_random_one_pair, 1),
        (TestUtils.gen_random_two_pair, 2),
        (TestUtils.gen_random_three_of_a_kind, 3),
        (TestUtils.gen_random_straight, 4),
        (TestUtils.gen_random_flush, 5),
        (TestUtils.gen_random_full_house, 6),
        (TestUtils.gen_random_four_of_a_kind, 7),
        (TestUtils.gen_random_straight_flush, 8),
    ],
    ids=[HAND_RANKINGS[i] for i in range(9)],
)
def test_calc_hand_rank_by_category(hand_factory, expected_rank: int) -> None:
    cards: list[str] = hand_factory()
    hand: Hand = TestUtils.make_hand(cards)
    player: Player = Player("Tester", hand=hand)

    rank: tuple[int, list[int]] = Logic.calc_hand_rank(player)
    assert rank[0] == expected_rank
