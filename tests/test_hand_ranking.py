import itertools

import pytest

from poker.card_collections import Hand
from poker.entities import Player
from poker.rules import Logic

# --- Helpers ---
PLAYER_NUM = itertools.count()


def make_hand(cards) -> Hand:
    return Hand.from_str_list(cards)


def make_player(hand: Hand):
    return Player(f"test_player_{next(PLAYER_NUM)}", hand)


# --- Fixtures ---
@pytest.fixture
def royal_flush_hand() -> Hand:
    cards = ["AS", "KS", "QS", "JS", "TS"]
    return make_hand(cards)


@pytest.fixture
def straight_flush_hand() -> Hand:
    cards = ["JD", "TD", "9D", "8D", "7D"]
    return make_hand(cards)


@pytest.fixture
def four_of_a_kind_hand() -> Hand:
    cards = ["9C", "9D", "9H", "9S", "3D"]
    return make_hand(cards)


@pytest.fixture
def straight_wheel_hand() -> Hand:
    cards = ["5C", "4D", "3S", "2D", "AD"]
    return make_hand(cards)


@pytest.fixture
def straight_hand() -> Hand:
    cards = ["7D", "6H", "5S", "4H", "3C"]
    return make_hand(cards)


@pytest.fixture
def flush_hand() -> Hand:
    cards = ["AS", "6S", "2S", "QS", "4S"]
    return make_hand(cards)


@pytest.fixture
def pair_hand() -> Hand:
    cards = ["KH", "KD", "7S", "4C", "2D"]
    return make_hand(cards)


@pytest.fixture
def high_card_hand() -> Hand:
    cards = ["AH", "KD", "7S", "4C", "2D"]
    return make_hand(cards)


# --- Single Param Tests ---
# def test_is_flush_true(royal_flush_hand: Hand):
#     hand: Hand = royal_flush_hand
#     rslt: bool = Logic.is_flush(hand)
#     assert rslt is True


# --- Parameterized Tests ---
straight_hand_cases = [
    ("royal_flush_hand", True),
    ("straight_flush_hand", True),
    ("straight_wheel_hand", True),
    ("straight_hand", True),
    ("flush_hand", False),
    ("pair_hand", False),
    ("high_card_hand", False),
    ("four_of_a_kind_hand", False),
]


@pytest.mark.parametrize(
    "hand_fixture, expected",
    straight_hand_cases,
    ids=[c[0] for c in straight_hand_cases],
)
def test_is_straight_cases(request, hand_fixture, expected: bool):
    hand: Hand = request.getfixturevalue(hand_fixture)
    assert Logic.is_straight(hand) is expected


flush_hand_cases = [
    ("royal_flush_hand", True),
    ("straight_flush_hand", True),
    ("flush_hand", True),
    ("straight_hand", False),
    ("pair_hand", False),
    ("high_card_hand", False),
    ("four_of_a_kind_hand", False),
    ("straight_wheel_hand", False),
]


@pytest.mark.parametrize(
    "hand_fixture, expected",
    flush_hand_cases,
    ids=[c[0] for c in flush_hand_cases],
)
def test_is_flush_cases(request, hand_fixture, expected: bool):
    hand: Hand = request.getfixturevalue(hand_fixture)
    assert Logic.is_flush(hand) is expected


four_of_a_kind_cases = [
    ("four_of_a_kind_hand", True),
    ("royal_flush_hand", False),
    ("straight_flush_hand", False),
    ("straight_wheel_hand", False),
    ("straight_hand", False),
    ("flush_hand", False),
    ("pair_hand", False),
    ("high_card_hand", False),
]


@pytest.mark.parametrize(
    "hand_fixture, expected",
    four_of_a_kind_cases,
    ids=[c[0] for c in four_of_a_kind_cases],
)
def test_is_four_of_a_kind_cases(request, hand_fixture, expected: bool):
    hand: Hand = request.getfixturevalue(hand_fixture)
    assert Logic.is_four_of_kind(hand) is expected
