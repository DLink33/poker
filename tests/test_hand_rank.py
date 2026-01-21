from collections import Counter

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


# Fixture for a random hand
@pytest.fixture
def random_hand() -> Hand:
    cards: list[str] = TestUtils.gen_random_hand()
    return TestUtils.make_hand(cards)


# Fixtures for specific hand types
@pytest.fixture
def player_with_straight_flush() -> Player:
    cards: list[str] = ["TD", "JD", "QD", "KD", "AD"]
    hand: Hand = TestUtils.make_hand(cards)
    return Player("StraightFlushPlayer", hand=hand)


@pytest.fixture
def player_with_four_of_a_kind() -> Player:
    cards: list[str] = ["9H", "9D", "9S", "9C", "2D"]
    hand: Hand = TestUtils.make_hand(cards)
    return Player("FourOfAKindPlayer", hand=hand)


@pytest.fixture
def player_with_full_house() -> Player:
    cards: list[str] = ["8H", "8D", "8S", "7C", "7D"]
    hand: Hand = TestUtils.make_hand(cards)
    return Player("FullHousePlayer", hand=hand)


@pytest.fixture
def player_with_flush() -> Player:
    cards: list[str] = ["2H", "5H", "7H", "9H", "JH"]
    hand: Hand = TestUtils.make_hand(cards)
    return Player("FlushPlayer", hand=hand)


@pytest.fixture
def player_with_straight() -> Player:
    cards: list[str] = ["3H", "4D", "5S", "6C", "7D"]
    hand: Hand = TestUtils.make_hand(cards)
    return Player("StraightPlayer", hand=hand)


@pytest.fixture
def player_with_three_of_a_kind() -> Player:
    cards: list[str] = ["4H", "4D", "4S", "9C", "JD"]
    hand: Hand = TestUtils.make_hand(cards)
    return Player("ThreeOfAKindPlayer", hand=hand)


@pytest.fixture
def player_with_two_pair() -> Player:
    cards: list[str] = ["5H", "5D", "6S", "6C", "TD"]
    hand: Hand = TestUtils.make_hand(cards)
    return Player("TwoPairPlayer", hand=hand)


@pytest.fixture
def player_with_one_pair() -> Player:
    cards: list[str] = ["2H", "2D", "5S", "9C", "JD"]
    hand: Hand = TestUtils.make_hand(cards)
    return Player("OnePairPlayer", hand=hand)


@pytest.fixture
def player_with_high_card() -> Player:
    cards: list[str] = ["3H", "4D", "6S", "8C", "TD"]
    hand: Hand = TestUtils.make_hand(cards)
    return Player("HighCardPlayer", hand=hand)


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


# --- Player Hand Comparison Tests ---
@pytest.mark.parametrize(
    "player_fixture_1, player_fixture_2, expected_winner_fixture",
    [
        (
            "player_with_straight_flush",
            "player_with_four_of_a_kind",
            "player_with_straight_flush",
        ),
        ("player_with_full_house", "player_with_flush", "player_with_full_house"),
        ("player_with_straight", "player_with_three_of_a_kind", "player_with_straight"),
        ("player_with_two_pair", "player_with_one_pair", "player_with_two_pair"),
        ("player_with_high_card", "player_with_one_pair", "player_with_one_pair"),
        (
            "player_with_flush",
            "player_with_straight_flush",
            "player_with_straight_flush",
        ),
        (
            "player_with_four_of_a_kind",
            "player_with_full_house",
            "player_with_four_of_a_kind",
        ),
        (
            "player_with_three_of_a_kind",
            "player_with_two_pair",
            "player_with_three_of_a_kind",
        ),
        ("player_with_one_pair", "player_with_high_card", "player_with_one_pair"),
        ("player_with_straight", "player_with_flush", "player_with_flush"),
        (
            "player_with_full_house",
            "player_with_straight_flush",
            "player_with_straight_flush",
        ),
        (
            "player_with_four_of_a_kind",
            "player_with_straight_flush",
            "player_with_straight_flush",
        ),
        ("player_with_high_card", "player_with_two_pair", "player_with_two_pair"),
        (
            "player_with_straight_flush",
            "player_with_two_pair",
            "player_with_straight_flush",
        ),
    ],
    ids=[
        "straight flush beats four of a kind",
        "full house beats flush",
        "straight beats three of a kind",
        "two pair beats one pair",
        "one pair beats high card",
        "straight flush beats flush",
        "four of a kind beats full house",
        "three of a kind beats two pair",
        "one pair beats high card",
        "flush beats straight",
        "straight flush beats full house",
        "straight flush beats four of a kind",
        "two pair beats high card",
        "straight flush beats two pair",
    ],
)
def test_poker_hands_head_to_head(
    request, player_fixture_1, player_fixture_2, expected_winner_fixture
):
    player1: Player = request.getfixturevalue(player_fixture_1)
    player2: Player = request.getfixturevalue(player_fixture_2)
    expected_winner: Player = request.getfixturevalue(expected_winner_fixture)

    winner: Player = Logic.poker([player1, player2])[
        0
    ]  # assumes no ties for this test (one winner)
    assert winner == expected_winner


@pytest.mark.parametrize(
    "player_fixture_list, expected_winner_fixture_list",
    [
        (
            [
                "player_with_straight_flush",
                "player_with_full_house",
                "player_with_flush",
                "player_with_straight",
                "player_with_three_of_a_kind",
                "player_with_two_pair",
                "player_with_one_pair",
                "player_with_high_card",
                "player_with_high_card",
                "player_with_high_card",
                "player_with_high_card",
                "player_with_high_card",
                "player_with_high_card",
                "player_with_straight_flush",
            ],
            ["player_with_straight_flush", "player_with_straight_flush"],
        ),
        (
            ["player_with_straight_flush", "player_with_straight_flush"],
            ["player_with_straight_flush", "player_with_straight_flush"],
        ),
        (
            [
                "player_with_four_of_a_kind",
                "player_with_four_of_a_kind",
                "player_with_high_card",
                "player_with_one_pair",
                "player_with_two_pair",
                "player_with_three_of_a_kind",
            ],
            ["player_with_four_of_a_kind", "player_with_four_of_a_kind"],
        ),
        (
            [
                "player_with_straight_flush",
                "player_with_four_of_a_kind",
                "player_with_full_house",
            ],
            ["player_with_straight_flush"],
        ),
        (
            [
                "player_with_straight_flush",
                "player_with_straight_flush",
                "player_with_four_of_a_kind",
                "player_with_full_house",
                "player_with_flush",
                "player_with_straight",
                "player_with_three_of_a_kind",
                "player_with_two_pair",
                "player_with_one_pair",
                "player_with_high_card",
            ],
            ["player_with_straight_flush", "player_with_straight_flush"],
        ),
        (
            [
                "player_with_two_pair",
                "player_with_two_pair",
                "player_with_one_pair",
                "player_with_one_pair",
                "player_with_high_card",
            ],
            [
                "player_with_two_pair",
                "player_with_two_pair",
            ],
        ),
        (
            [
                "player_with_one_pair",
                "player_with_high_card",
                "player_with_high_card",
                "player_with_high_card",
            ],
            [
                "player_with_one_pair",
            ],
        ),
        (
            [
                "player_with_three_of_a_kind",
                "player_with_three_of_a_kind",
                "player_with_three_of_a_kind",
            ],
            [
                "player_with_three_of_a_kind",
                "player_with_three_of_a_kind",
                "player_with_three_of_a_kind",
            ],
        ),
    ],
    ids=[
        "2 straight flushes vs others",
        "straight flush vs straight flush",
        "2 four of a kinds vs others",
        "straight flush beats others",
        "2 straight flushes vs others",
        "2 two pairs vs others",
        "one pair vs high cards",
        "3 way tie with three of a kinds",
    ],
)
def test_multiple_poker_hands(
    request, player_fixture_list, expected_winner_fixture_list
):
    players = [request.getfixturevalue(n) for n in player_fixture_list]
    expected = [request.getfixturevalue(n) for n in expected_winner_fixture_list]

    winners = Logic.poker(players)

    assert Counter(p.name for p in winners) == Counter(p.name for p in expected)
