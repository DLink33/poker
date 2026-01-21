from poker.card_collections import Deck


def test_deck_init():
    deck = Deck()
    assert len(deck) == 52
    unique_cards = set(deck._cards)
    assert len(unique_cards) == 52


def test_deck_shuffle():
    deck1 = Deck()
    deck2 = Deck()
    deck2.shuffle()
    assert deck1._cards != deck2._cards
