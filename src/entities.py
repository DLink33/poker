from .card_collections import Deck, Hand


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