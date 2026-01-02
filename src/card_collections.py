from collections import defaultdict
from random import shuffle

from .cards import RANKS, SUITS, Card


class CardCollection():
    '''
    Represents a set of cards (ordered with index-type lookups)
    '''
    def __init__(self, cards:list[Card] | None = None):
        self._cards:list[Card|None] = []                                        # represents order
        self._index:dict[tuple[SUITS, RANKS], list[Card]] = defaultdict(list)   # fast look up
        if cards:
            for card in cards:
                self.add(card)

    def __len__(self) -> int:
        return len(self._cards)

    def __iter__(self):
        return iter(self._cards)

    def __str__(self) -> str:
        return "\n".join(str(card) for card in self._cards)
    
    def add(self, card: Card, position: int | None = None) -> None:
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

    def has_card_of_type(self, suit: SUITS, rank: RANKS) -> bool:
        """
        Do we have at least one card with this suit/rank?
        """
        return bool(self._index.get((suit, rank)))

    def peek_card_of_type(self, suit: SUITS, rank: RANKS) -> Card | None:
        """
        Return (without removing) one card of this type, if any.
        """
        bucket = self._index.get((suit, rank))
        return bucket[0] if bucket else None

    def pop_card_of_type(self, suit: SUITS, rank: RANKS) -> Card | None:
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
    '''
    Docstring for Deck
    '''
    def __init__(self):
        cards:list[Card] = [
            Card(suit, rank)
            for suit in SUITS
            for rank in RANKS
        ]
        super().__init__(cards)

    
    # ---- deck/stack-style helpers ----

    def draw_top(self) -> Card | None:
        """Pop from the end (top) of the collection."""
        if not self._cards:
            return None

        card = self._cards.pop()

        if card is None:
            return None
        
        bucket = self._index[(card.type.suit, card.type.rank)]
        bucket.remove(card)
        if not bucket:
            del self._index[(card.type.suit, card.type.rank)]

        return card

    def draw_bottom(self) -> Card | None:
        """Pop from the beginning (bottom) of the collection."""
        if not self._cards:
            return None

        card = self._cards.pop(0)
        if card is None:
            return None
        bucket = self._index[(card.type.suit, card.type.rank)]
        bucket.remove(card)
        if not bucket:
            del self._index[(card.type.suit, card.type.rank)]

        return card
    
    def shuffle(self) -> None:
        shuffle(self._cards)

class Hand(CardCollection):
    def __init__(self):
        super().__init__()
        raise NotImplementedError

class Pile(CardCollection):
    def __init__(self):
        super().__init__()
        raise NotImplementedError

class DiscardPile(Pile):
    def __init__(self):
        super().__init__()
        raise NotImplementedError