from poker.card_collections import Deck
from poker.cards import Card


def test_deck_init():
    deck: Deck = Deck()
    assert len(deck) == 52
    unique_cards = set(deck._cards)
    assert len(unique_cards) == 52


def test_deck_draw_top():
    deck: Deck = Deck()
    top_card = deck._cards[-1]
    drawn_card = deck.draw_top()
    assert drawn_card == top_card
    assert len(deck) == 51


def test_deck_draw_bottom():
    deck: Deck = Deck()
    bot_card: Card = deck._cards[0]
    drawn_card: Card | None = deck.draw_bottom()
    assert bot_card == drawn_card
    assert len(deck) == 51


def test_deck_shuffle():
    deck1: Deck = Deck()
    deck2: Deck = Deck()
    deck2.shuffle()
    assert deck1._cards != deck2._cards
