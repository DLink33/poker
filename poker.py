SUITS = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
RANKS = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King', 'Ace']

class Card():
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank
        self.revealed = False
    
    def __str__(self) -> str:
        return f"Card {self.rank} of {self.suit}"

class Deck():
    """A class representing a standard deck of 52 playing cards."""


    def __init__(self):
        """Initialize the deck with 52 cards."""
        self.cards = [Card(suit, rank) for suit in SUITS for rank in RANKS]
    
    def __str__(self) -> str:
        "Prints out alist of cards currently in the Deck"
        out: str = ""
        for card in self.cards:
            out += str(card) + "\n"
        return out

    def shuffle(self):
        """Shuffle the deck of cards."""
        import random
        random.shuffle(self.cards)




