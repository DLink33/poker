from .card_collections import Deck, Hand
from .cards import Card, Ranks, Suits


class Entity:
    def __init__(self, name: str):
        self.name: str = name

    def __str__(self):
        return f"name: {self.name}"


class Dealer(Entity):
    def __init__(self):
        # TODO: Add ability to take in different rule sets for poker i.e. ace low versus ace hight etc.
        self.rule_set = None
        self.deck: Deck = Deck()
        super().__init__(name="dealer")

    def deal(self, num_hands: int, cards_per_hand: int) -> list[Hand]:
        hands: list[Hand] = []
        self.deck.shuffle()
        for _ in range(num_hands):
            hand: Hand = Hand(
                [
                    card
                    for card in [self.deck.draw_top() for _ in range(cards_per_hand)]
                    if card is not None
                ]
            )
            hands.append(hand)
        return hands


class Player(Entity):
    _nxt_id = 0

    @classmethod
    def _get_next_id(cls) -> int:
        cls._nxt_id += 1
        return cls._nxt_id

    def __init__(self, name, hand: Hand | None):
        super().__init__(name)
        self.id: int = self._get_next_id()
        self.hand: Hand | None = hand

    def __str__(self):
        return super().__str__() + "\n" + "hand:\n" + str(self.hand) + "\n"

    def __repr__(self) -> str:
        return f"Player(id={self.id}, name={self.name})"

    def __hash__(self) -> int:
        return hash(self.id + hash(self.name))


def main():
    ace_of_diamonds: Card = Card(Suits.DIAMONDS, Ranks.ACE)
    jack_of_spades: Card = Card(Suits.SPADES, Ranks.JACK)
    two_of_clubs: Card = Card(Suits.CLUBS, Ranks.TWO)
    smol_hand = [ace_of_diamonds, jack_of_spades, two_of_clubs]
    low_card = min(smol_hand)
    high_card = max(smol_hand)
    assert low_card == two_of_clubs
    assert high_card == ace_of_diamonds

    dealer: Dealer = Dealer()
    hands: list[Hand] = dealer.deal(4, 5)
    for i, hand in enumerate(hands):
        print(f"Hand {i + 1}: {hand.getCards()}")


if __name__ == "__main__":
    main()
