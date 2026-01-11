import itertools
from random import choice, randint, sample, shuffle
import pytest

from poker.cards import SUIT_ABBR, RANK_ABBR
from poker.card_collections import Hand
from poker.entities import Player
from poker.rules import Logic

# --- Helpers ---
PLAYER_NUM = itertools.count()


def make_hand(cards) -> Hand:
    return Hand.from_str_list(cards)


def make_player(hand: Hand):
    return Player(f"test_player_{next(PLAYER_NUM)}", hand)


SUITS = list(SUIT_ABBR.keys())

RANK_CHAR = {10: "T", 11: "J", 12: "Q", 13: "K", 14: "A"}


def rank_to_char(rank: int) -> str:
    """2..14 -> '2'..'9','T','J','Q','K','A'"""
    return RANK_CHAR.get(rank, str(rank))


def random_suit() -> str:
    return choice(SUITS)


def gen_random_royal_flush() -> list[str]:
    suit = random_suit()
    ranks = ["T", "J", "Q", "K", "A"]
    return [r + suit for r in ranks]


def gen_random_straight_flush() -> list[str]:
    suit = random_suit()

    # start_rank 2..10 gives 5-card straight up to A-high (10,J,Q,K,A)
    start = randint(2, 10)
    ranks = [rank_to_char(r) for r in range(start, start + 5)]
    return [r + suit for r in ranks]


def gen_random_four_of_a_kind() -> list[str]:
    suit_chars = list(SUIT_ABBR.keys())

    quad_rank = randint(2, 14)
    quad_rank_char = rank_to_char(quad_rank)
    four_cards = [quad_rank_char + s for s in suit_chars]  # all 4 suits

    kicker_rank = randint(2, 14)
    while kicker_rank == quad_rank:  # <-- fill in / keep this
        kicker_rank = randint(2, 14)

    kicker = rank_to_char(kicker_rank) + choice(suit_chars)
    four_cards.append(kicker)
    return four_cards


def gen_random_full_house() -> list[str]:
    suit_chars = list(SUIT_ABBR.keys())

    trip_rank = randint(2, 14)
    trip_rank_char = rank_to_char(trip_rank)
    trip_suits = sample(suit_chars, 3)
    three_cards = [trip_rank_char + s for s in trip_suits]

    pair_rank = randint(2, 14)
    while pair_rank == trip_rank:
        pair_rank = randint(2, 14)

    pair_rank_char = rank_to_char(pair_rank)
    pair_suits = sample(suit_chars, 2)
    two_cards = [pair_rank_char + s for s in pair_suits]

    return three_cards + two_cards


def gen_random_flush() -> list[str]:
    """
    Generate a flush that is NOT a straight flush.
    """
    suit = random_suit()

    while True:
        # choose 5 distinct ranks
        ranks_int = sample(range(2, 15), 5)
        ranks_int.sort()
        # avoid wheel/broadway/any straight patterns
        is_straight = (
            ranks_int[-1] - ranks_int[0] == 4 and len(set(ranks_int)) == 5
        ) or (ranks_int == [2, 3, 4, 5, 14])
        if is_straight:
            continue

        ranks = [rank_to_char(r) for r in ranks_int]
        return [r + suit for r in ranks]


def gen_random_straight() -> list[str]:
    """
    Generate a straight that is NOT a straight flush.
    (Also avoids accidental flush.)
    """
    start = randint(2, 10)
    ranks = [rank_to_char(r) for r in range(start, start + 5)]

    # Pick suits; ensure not all suits are the same.
    suits = [random_suit() for _ in range(5)]
    if len(set(suits)) == 1:
        # force at least one card to a different suit
        suits[0] = choice([s for s in SUITS if s != suits[0]])

    cards = [r + s for r, s in zip(ranks, suits)]
    return cards


def gen_random_three_of_a_kind() -> list[str]:
    suit_chars = list(SUIT_ABBR.keys())

    trip_rank = randint(2, 14)
    trip_rank_char = rank_to_char(trip_rank)
    trip_suits = sample(suit_chars, 3)
    three_cards = [trip_rank_char + s for s in trip_suits]

    kicker_ranks = sample([r for r in range(2, 15) if r != trip_rank], 2)
    kicker_chars = [rank_to_char(r) for r in kicker_ranks]
    kicker_cards = [rc + random_suit() for rc in kicker_chars]

    return three_cards + kicker_cards


def gen_random_two_pair() -> list[str]:
    suit_chars = SUITS[:]

    while True:
        pair_ranks = sample(range(2, 15), 2)
        pair_chars = [rank_to_char(r) for r in pair_ranks]

        pair_cards = []
        for pc in pair_chars:
            pair_suits = sample(suit_chars, 2)
            pair_cards.extend([pc + s for s in pair_suits])

        # choose 1 kicker rank different from both pair ranks
        kicker_rank = choice([r for r in range(2, 15) if r not in pair_ranks])
        kicker_char = rank_to_char(kicker_rank)
        kicker_card = kicker_char + random_suit()

        cards = pair_cards + [kicker_card]
        shuffle(cards)

        # --- filters to avoid accidentally creating other categories ---
        # Avoid flush (all suits same)
        if len({c[1] for c in cards}) == 1:
            continue

        return cards


def gen_random_one_pair() -> list[str]:
    """
    Generate exactly ONE pair (not two pair, not trips, not full house),
    and avoid accidental flush/straight.
    """
    suit_chars = SUITS[:]

    while True:
        pair_rank = randint(2, 14)
        pair_rank_char = rank_to_char(pair_rank)

        # pick 2 distinct suits for the pair
        pair_suits = sample(suit_chars, 2)
        pair_cards = [pair_rank_char + s for s in pair_suits]

        # choose 3 kicker ranks all distinct and different from pair_rank
        kicker_ranks = sample([r for r in range(2, 15) if r != pair_rank], 3)
        kicker_chars = [rank_to_char(r) for r in kicker_ranks]

        # assign random suits to kickers (can repeat suits; just avoid forming a flush)
        kicker_cards = [rc + random_suit() for rc in kicker_chars]

        cards = pair_cards + kicker_cards
        shuffle(cards)

        # --- filters to avoid accidentally creating other categories ---
        # Avoid flush (all suits same)
        if len({c[1] for c in cards}) == 1:
            continue

        # Avoid straight (based on ranks)
        # NOTE: ranks are single-char here, so c[0] is safe
        # If you ever support "10" strings, you'd need a smarter parser.
        char_to_rank = {v: k for k, v in RANK_CHAR.items()}

        def char_rank(ch: str) -> int:
            if ch in char_to_rank:
                return char_to_rank[ch]
            return int(ch)

        ranks_int = sorted({char_rank(c[0]) for c in cards})
        # if duplicates reduced set size < 5, it's not a straight anyway (pair implies duplicate)
        # but we still avoid weird cases like A2345 + pair? (won't happen due to duplicate)
        # So straight isn't possible here; keep the check minimal or omit.

        return cards


def gen_random_high_card() -> list[str]:
    suit_chars = SUITS[:]

    while True:
        ranks_int = sample(range(2, 15), 5)
        ranks_int.sort()
        # avoid straight patterns
        is_straight = (
            ranks_int[-1] - ranks_int[0] == 4 and len(set(ranks_int)) == 5
        ) or (ranks_int == [2, 3, 4, 5, 14])
        if is_straight:
            continue

        ranks = [rank_to_char(r) for r in ranks_int]
        cards = [r + random_suit() for r in ranks]

        # avoid flush
        if len({c[1] for c in cards}) == 1:
            continue

        return cards


# --- Fixtures ---
@pytest.fixture
def royal_flush_hand() -> Hand:
    cards = gen_random_royal_flush()
    return make_hand(cards)


@pytest.fixture
def straight_flush_hand() -> Hand:
    cards = gen_random_straight_flush()
    return make_hand(cards)


@pytest.fixture
def straight_wheel_hand() -> Hand:
    cards = ["5C", "4D", "3S", "2D", "AD"]
    return make_hand(cards)


@pytest.fixture
def four_of_a_kind_hand() -> Hand:
    cards = gen_random_four_of_a_kind()
    return make_hand(cards)


@pytest.fixture
def three_of_a_kind_hand() -> Hand:
    cards = gen_random_three_of_a_kind()
    return make_hand(cards)


@pytest.fixture
def full_house_hand() -> Hand:
    cards = gen_random_full_house()
    return make_hand(cards)


@pytest.fixture
def straight_hand() -> Hand:
    cards = gen_random_straight()
    return make_hand(cards)


@pytest.fixture
def flush_hand() -> Hand:
    cards = gen_random_flush()
    return make_hand(cards)


@pytest.fixture
def one_pair_hand() -> Hand:
    cards = gen_random_one_pair()
    return make_hand(cards)


@pytest.fixture
def two_pair_hand() -> Hand:
    cards = gen_random_two_pair()
    return make_hand(cards)


@pytest.fixture
def high_card_hand() -> Hand:
    cards = gen_random_high_card()
    return make_hand(cards)


# --- Single Param Tests ---
def test_lots_of_random_hands(straight_wheel_hand: Hand):
    assert Logic.is_straight(straight_wheel_hand) is True
    for _ in range(10000):
        assert Logic.is_flush(make_hand(gen_random_flush())) is True
        assert Logic.is_flush(make_hand(gen_random_royal_flush())) is True
        assert Logic.is_flush(make_hand(gen_random_straight_flush())) is True
        assert Logic.is_straight(make_hand(gen_random_straight_flush())) is True
        assert Logic.is_four_of_kind(make_hand(gen_random_four_of_a_kind())) is True
        assert Logic.is_full_house(make_hand(gen_random_full_house())) is True
        assert Logic.is_straight(make_hand(gen_random_straight())) is True
        assert Logic.is_full_house(make_hand(gen_random_full_house())) is True


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
