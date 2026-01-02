from card_collections import CardCollection


class Entity:
    def __init__(self, name:str):
        self.name:str = name

class Dealer(Entity):
    def __init__(self, deck:CardCollection):
        self.deck:CardCollection = deck
        super().__init__(name='dealer')

class Player(Entity):
    def __init__(self, name):
        super().__init__(name)
        self.hand:CardCollection = CardCollection(cards=[])