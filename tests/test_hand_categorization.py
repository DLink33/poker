import pytest
from utils import TestUtils

from poker.card_collections import Hand
from poker.rules import Logic


# --- Fixtures ---
@pytest.fixture
def royal_flush_hand() -> Hand:
    cards = TestUtils.gen_random_royal_flush()
    return TestUtils.make_hand(cards)


@pytest.fixture
def straight_flush_hand() -> Hand:
    cards = TestUtils.gen_random_straight_flush()
    return TestUtils.make_hand(cards)


@pytest.fixture
def straight_wheel_hand() -> Hand:
    cards = ["5C", "4D", "3S", "2D", "AD"]
    return TestUtils.make_hand(cards)


@pytest.fixture
def four_of_a_kind_hand() -> Hand:
    cards = TestUtils.gen_random_four_of_a_kind()
    return TestUtils.make_hand(cards)


@pytest.fixture
def three_of_a_kind_hand() -> Hand:
    cards = TestUtils.gen_random_three_of_a_kind()
    return TestUtils.make_hand(cards)


@pytest.fixture
def full_house_hand() -> Hand:
    cards = TestUtils.gen_random_full_house()
    return TestUtils.make_hand(cards)


@pytest.fixture
def straight_hand() -> Hand:
    cards = TestUtils.gen_random_straight()
    return TestUtils.make_hand(cards)


@pytest.fixture
def flush_hand() -> Hand:
    cards = TestUtils.gen_random_flush()
    return TestUtils.make_hand(cards)


@pytest.fixture
def one_pair_hand() -> Hand:
    cards = TestUtils.gen_random_one_pair()
    return TestUtils.make_hand(cards)


@pytest.fixture
def two_pair_hand() -> Hand:
    cards = TestUtils.gen_random_two_pair()
    return TestUtils.make_hand(cards)


@pytest.fixture
def high_card_hand() -> Hand:
    cards = TestUtils.gen_random_high_card()
    return TestUtils.make_hand(cards)


# --- Single Param Tests ---
def test_lots_of_random_hands(straight_wheel_hand: Hand):
    assert Logic.is_straight(straight_wheel_hand) is True
    for _ in range(10000):
        assert Logic.is_flush(TestUtils.make_hand(TestUtils.gen_random_flush())) is True
        assert (
            Logic.is_flush(TestUtils.make_hand(TestUtils.gen_random_royal_flush()))
            is True
        )
        assert (
            Logic.is_flush(TestUtils.make_hand(TestUtils.gen_random_straight_flush()))
            is True
        )
        assert (
            Logic.is_straight(
                TestUtils.make_hand(TestUtils.gen_random_straight_flush())
            )
            is True
        )
        assert (
            Logic.is_four_of_kind(
                TestUtils.make_hand(TestUtils.gen_random_four_of_a_kind())
            )
            is True
        )
        assert (
            Logic.is_full_house(TestUtils.make_hand(TestUtils.gen_random_full_house()))
            is True
        )
        assert (
            Logic.is_straight(TestUtils.make_hand(TestUtils.gen_random_straight()))
            is True
        )
        assert (
            Logic.is_full_house(TestUtils.make_hand(TestUtils.gen_random_full_house()))
            is True
        )


# --- Test Cases for Parameterized Tests ---
straight_hand_cases = [
    ("royal_flush_hand", True),
    ("straight_flush_hand", True),
    ("straight_wheel_hand", True),
    ("straight_hand", True),
    ("flush_hand", False),
    ("high_card_hand", False),
    ("four_of_a_kind_hand", False),
    ("full_house_hand", False),
    ("two_pair_hand", False),
    ("one_pair_hand", False),
    ("three_of_a_kind_hand", False),
]

full_house_cases = [
    ("full_house_hand", True),
    ("four_of_a_kind_hand", False),
    ("three_of_a_kind_hand", False),
    ("two_pair_hand", False),
    ("one_pair_hand", False),
    ("flush_hand", False),
    ("straight_hand", False),
    ("straight_flush_hand", False),
    ("royal_flush_hand", False),
    ("high_card_hand", False),
]

four_of_a_kind_cases = [
    ("four_of_a_kind_hand", True),
    ("royal_flush_hand", False),
    ("straight_flush_hand", False),
    ("straight_wheel_hand", False),
    ("straight_hand", False),
    ("flush_hand", False),
    ("one_pair_hand", False),
    ("two_pair_hand", False),
    ("high_card_hand", False),
    ("full_house_hand", False),
    ("three_of_a_kind_hand", False),
]

three_of_a_kind_cases = [
    ("three_of_a_kind_hand", True),
    ("four_of_a_kind_hand", False),
    ("royal_flush_hand", False),
    ("straight_flush_hand", False),
    ("straight_wheel_hand", False),
    ("straight_hand", False),
    ("flush_hand", False),
    ("one_pair_hand", False),
    ("two_pair_hand", False),
    ("high_card_hand", False),
    ("full_house_hand", False),
]

two_pair_cases = [
    ("two_pair_hand", True),
    ("royal_flush_hand", False),
    ("straight_flush_hand", False),
    ("straight_wheel_hand", False),
    ("straight_hand", False),
    ("flush_hand", False),
    ("one_pair_hand", False),
    ("high_card_hand", False),
    ("full_house_hand", False),
    ("four_of_a_kind_hand", False),
]

one_pair_cases = [
    ("one_pair_hand", True),
    ("royal_flush_hand", False),
    ("straight_flush_hand", False),
    ("straight_wheel_hand", False),
    ("straight_hand", False),
    ("flush_hand", False),
    ("high_card_hand", False),
    ("full_house_hand", False),
    ("four_of_a_kind_hand", False),
    ("two_pair_hand", False),
]

high_card_hand_cases = [
    ("high_card_hand", True),
    ("royal_flush_hand", False),
    ("straight_flush_hand", False),
    ("straight_wheel_hand", False),
    ("straight_hand", False),
    ("flush_hand", False),
    ("one_pair_hand", False),
    ("full_house_hand", False),
    ("four_of_a_kind_hand", False),
    ("two_pair_hand", False),
]

flush_hand_cases = [
    ("royal_flush_hand", True),
    ("straight_flush_hand", True),
    ("flush_hand", True),
    ("straight_hand", False),
    ("high_card_hand", False),
    ("four_of_a_kind_hand", False),
    ("straight_wheel_hand", False),
    ("full_house_hand", False),
    ("four_of_a_kind_hand", False),
    ("two_pair_hand", False),
    ("one_pair_hand", False),
]


# --- Parameterized Tests ---
@pytest.mark.parametrize(
    "hand_fixture, expected",
    straight_hand_cases,
    ids=[c[0] for c in straight_hand_cases],
)
def test_is_straight_cases(request, hand_fixture, expected: bool):
    hand: Hand = request.getfixturevalue(hand_fixture)
    assert Logic.is_straight(hand) is expected


@pytest.mark.parametrize(
    "hand_fixture, expected",
    flush_hand_cases,
    ids=[c[0] for c in flush_hand_cases],
)
def test_is_flush_cases(request, hand_fixture, expected: bool):
    hand: Hand = request.getfixturevalue(hand_fixture)
    assert Logic.is_flush(hand) is expected


@pytest.mark.parametrize(
    "hand_fixture, expected",
    four_of_a_kind_cases,
    ids=[c[0] for c in four_of_a_kind_cases],
)
def test_is_four_of_a_kind_cases(request, hand_fixture, expected: bool):
    hand: Hand = request.getfixturevalue(hand_fixture)
    assert Logic.is_four_of_kind(hand) is expected


@pytest.mark.parametrize(
    "hand_fixture, expected",
    three_of_a_kind_cases,
    ids=[c[0] for c in three_of_a_kind_cases],
)
def test_is_three_of_a_kind_cases(request, hand_fixture, expected: bool):
    hand: Hand = request.getfixturevalue(hand_fixture)
    assert Logic.is_three_of_kind(hand) is expected


@pytest.mark.parametrize(
    "hand_fixture, expected",
    full_house_cases,
    ids=[c[0] for c in full_house_cases],
)
def test_is_full_house_cases(request, hand_fixture, expected: bool):
    hand: Hand = request.getfixturevalue(hand_fixture)
    assert Logic.is_full_house(hand) is expected


@pytest.mark.parametrize(
    "hand_fixture, expected",
    two_pair_cases,
    ids=[c[0] for c in two_pair_cases],
)
def test_is_two_pair_cases(request, hand_fixture, expected: bool):
    hand: Hand = request.getfixturevalue(hand_fixture)
    assert Logic.is_two_pair(hand) is expected


@pytest.mark.parametrize(
    "hand_fixture, expected",
    one_pair_cases,
    ids=[c[0] for c in one_pair_cases],
)
def test_is_one_pair_cases(request, hand_fixture, expected: bool):
    hand: Hand = request.getfixturevalue(hand_fixture)
    assert Logic.is_one_pair(hand) is expected


@pytest.mark.parametrize(
    "hand_fixture, expected",
    high_card_hand_cases,
    ids=[c[0] for c in high_card_hand_cases],
)
def test_is_high_card_cases(request, hand_fixture, expected: bool):
    hand: Hand = request.getfixturevalue(hand_fixture)
    assert Logic.is_high_card(hand) is expected
