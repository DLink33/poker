from .card_collections import Deck, Hand
from .cards import Card, Ranks, Suits


class Entity:
    def __init__(self, name:str):
        self.name:str = name

class Dealer(Entity):
    def __init__(self):
        #TODO: Add ability to take in different rule sets for poker i.e. ace low versus ace hight etc.
        self.rule_set = None
        self.deck:Deck = Deck()
        super().__init__(name='dealer')

class Player(Entity):
    def __init__(self, name, hand:Hand):
        super().__init__(name)
        self.hand:Hand = hand
    
def main():
    ace_of_diamonds:Card = Card(Suits.DIAMONDS, Ranks.ACE)
    jack_of_spades:Card = Card(Suits.SPADES, Ranks.JACK)
    two_of_clubs:Card = Card(Suits.CLUBS, Ranks.TWO)
    smol_hand = [ace_of_diamonds, jack_of_spades, two_of_clubs]
    low_card = min(smol_hand)
    high_card = max(smol_hand)
    assert low_card == two_of_clubs
    assert high_card == ace_of_diamonds

if __name__ == '__main__':
    main()