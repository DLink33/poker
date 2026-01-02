SUITS = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
RANKS = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King', 'Ace']


class Card():
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank
        self.revealed = False
    
    def __str__(self) -> str:
        return f"{self.rank} of {self.suit}"
    
class CardSet():
    '''
    Represents a set of cards (unique and unordered)
    '''
    def __init__(self, cards:set[Card | None]):
        self.cards:set[Card|None] = cards
    
    def __str__(self) -> str:
        "Prints out alist of cards currently in the Deck"
        out: str = ""
        for card in self.cards:
            out += str(card) + "\n"
        return out
    
    def take(self, numCards:int=1) -> None|Card|set[Card]:
        if not numCards:
            return
        if numCards == 1:
            return self.cards.pop()
        drawn = set()
        for i in range(numCards):
            drawn.add(self.cards.pop())
        return drawn
    
    def insert(self, cards:set[Card], numCards:int) -> None:
        if not cards:
            return
        for card in cards:
            self.cards.add(card)
    
class Pile():
    def __init__(self, cards:list[Card]):
        self.cards = cards
    def draw(self, numCards:int=1)-> Card|set[Card]:
        if numCards == 1:
            return self.cards.pop()
        retCards:set[Card] = set()
        for _ in range(numCards):
            retCards.add(self.cards.pop())
        return retCards


class Deck(Pile):
    """A class representing a standard deck of 52 playing cards."""


    def __init__(self):
        """Initialize the deck with 52 cards."""
        super().__init__([Card(suit, rank) for suit in SUITS for rank in RANKS])
    

    def shuffle(self) -> None:
        """Shuffle the deck of cards."""
        import random
        if not self.cards:
            return
        cards_list = list(self.cards)
        random.shuffle(cards_list)
        self.cards = set(cards_list)

class Entity:
    def __init__(self, name:str):
        self.name:str = name

class Dealer(Entity):
    def __init__(self, deck:Deck):
        self.deck:Deck = deck



