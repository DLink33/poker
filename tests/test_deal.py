import pytest

from poker.card_collections import Hand
from poker.cards import Card
from poker.entities import Dealer


@pytest.fixture
def dealer() -> Dealer:
    return Dealer()


@pytest.mark.parametrize(
    "dealer_fixture, num_hands, num_cards_per_hand, expected_hands, expected_cards_per_hand",
    [
        ("dealer", 4, 5, 4, 5),
        ("dealer", 2, 7, 2, 7),
        ("dealer", 3, 2, 3, 2),
        ("dealer", 5, 1, 5, 1),
        ("dealer", 6, 0, 6, 0),
        ("dealer", 1, 10, 1, 10),
        ("dealer", 0, 5, 0, 0),
    ],
)
def test_deal(
    request,
    dealer_fixture,
    num_hands,
    num_cards_per_hand,
    expected_hands,
    expected_cards_per_hand,
):
    dealer: Dealer = request.getfixturevalue(dealer_fixture)
    hands: list[Hand] = dealer.deal(num_hands, num_cards_per_hand)
    assert len(hands) == expected_hands
    for hand in hands:
        assert isinstance(hand, Hand)
        cards: list[Card] = hand.getCards()
        print(cards)
        assert len(cards) == expected_cards_per_hand
        for card in cards:
            assert isinstance(card, Card)
