import re
from collections import defaultdict
from random import shuffle

from .cards import Card, Ranks, Suits


class CardCollection():
    '''
    Represents a set of cards (ordered with index-type lookups)
    '''
    @classmethod
    def from_str(cls, cards_str:str) -> "CardCollection":
        card_list: list[Card] = []
        cards: list[str] = re.split(r'[;,\s]+', cards_str)
        for card_str in cards:
            card_list.append(Card.from_str(card_str))
        return cls(card_list)
    
    @classmethod
    def from_str_list(cls, cards:list[str]) -> "CardCollection":
        card_list: list[Card] = []
        for card_str in cards:
            card_list.append(Card.from_str(card_str))
        return cls(card_list)

    def __init__(self, cards:list[Card] | None = None):
        self._cards:list[Card] = []  # represents order
        self._index:dict[tuple[Suits, Ranks], list[Card]] = defaultdict(list)   # fast look up
        if cards:
            for card in cards:
                self.add_card(card)

    def __len__(self) -> int:
        return len(self._cards)

    def __iter__(self):
        return iter(self._cards)

    def __str__(self) -> str:
        return "\n".join(str(card) for card in self._cards)
    
    def add_card(self, card: Card, position: int | None = None) -> None:
        """
        Adds a SINGLE card to the collection.
        If position is None, append at the end.
        """
        if position is None:
            self._cards.append(card)
        else:
            self._cards.insert(position, card)
        
        # can track more than one card of the same rank and suit with a list:
        self._index[(card.type.suit, card.type.rank)].append(card) 

    def remove_card(self, card: Card) -> None:
        """
        Removes this exact card object from the collection.
        """
        self._cards.remove(card)
        bucket = self._index[(card.type.suit, card.type.rank)]
        bucket.remove(card)
        if not bucket: # if there are no more cards of this type in the collection, delete dict entry
            del self._index[(card.type.suit, card.type.rank)]

    # ---- lookup by type ----

    def has_card_of_type(self, suit: Suits, rank: Ranks) -> bool:
        """
        Do we have at least one card with this suit/rank?
        """
        return bool(self._index.get((suit, rank)))

    def peek_card_of_type(self, suit: Suits, rank: Ranks) -> Card | None:
        """
        Return (without removing) one card of this type, if any.
        """
        bucket = self._index.get((suit, rank))
        return bucket[0] if bucket else None

    def pop_card_of_type(self, suit: Suits, rank: Ranks) -> Card | None:
        """
        Remove and return one card with this suit/rank.
        If multiple exist, arbitrarily returns one of them.
        """
        bucket = self._index.get((suit, rank))
        if not bucket:
            return None

        card = bucket.pop()          # pick one
        if not bucket:
            del self._index[(suit, rank)]

        self._cards.remove(card)
        return card

class Deck(CardCollection):
    """
    A standard 52-card deck of playing cards.
    This class represents a complete deck containing all combinations of suits and ranks.
    It provides stack-style operations (LIFO) and queue-style operations (FIFO) for
    drawing cards, as well as shuffling capabilities.
    Inherits from:
        CardCollection: Base class for managing collections of Card objects.
    Attributes:
        Inherited from CardCollection:
            _cards (list[Card]): The internal list of Card objects in the deck.
            _index (dict): Index mapping card types to their instances for fast lookup.
    """
    def __init__(self):
        cards:list[Card] = [
            Card(suit, rank)
            for suit in Suits
            for rank in Ranks
        ]
        super().__init__(cards)

    
    # ---- deck/stack-style helpers ----
    
    def _draw(self, top=True) -> Card | None:
        if not self._cards:
            return None
        
        card:Card | None = self._cards.pop() if top else self._cards.pop(0)

        if card is None:
            return None
        
        bucket = self._index[(card.type.suit, card.type.rank)]
        bucket.remove(card)
        if not bucket:
            del self._index[(card.type.suit, card.type.rank)]
        
        return card

        
    def draw_top(self) -> Card | None:
        """
        Pop from the end (top) of the collection.
        """
        self._draw(top=True)

    def draw_bottom(self) -> Card | None:
        """
        Pop from the beginning (bottom) of the collection.
        """
        self._draw(top=False)
    
    def shuffle(self) -> None:
        shuffle(self._cards)

class Hand(CardCollection):
    def __init__(self, cards:list[Card]):
        super().__init__(cards=cards)
        
    def getCards(self):
        return self._cards
    
    def getMinCard(self):
        return min(self.getCards())
    
    def getMaxCard(self):
        return min(self.getCards())


class Pile(CardCollection):
    def __init__(self):
        super().__init__()
        raise NotImplementedError

class DiscardPile(Pile):
    def __init__(self):
        super().__init__()
        raise NotImplementedError

# Main for smoke testing purposes   
def main():
    hand = Hand.from_str('AD KD QD JD, TD 9D, 8D; 7D 6D; 5D 4D, 3D 2D')
    print(hand)

if __name__ == '__main__':
    main()