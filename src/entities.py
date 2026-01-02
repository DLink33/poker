from card_collections import Deck, Hand


class Entity:
    def __init__(self, name:str):
        self.name:str = name

class Dealer(Entity):
    def __init__(self):
        self.deck:Deck = Deck()
        super().__init__(name='dealer')

class Player(Entity):
    def __init__(self, name, hand:Hand):
        super().__init__(name)
        self.hand:Hand = hand