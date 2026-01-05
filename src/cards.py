from dataclasses import dataclass
from enum import Enum, IntEnum


class SUITS(Enum):
    clubs       = "♣"
    diamonds    = "♦"
    hearts      = "♥"
    spades      = "♠"

class RANKS(IntEnum):
    two         = 2
    three       = 3
    four        = 4
    five        = 5
    six         = 6
    seven       = 7
    eight       = 8
    nine        = 9
    ten         = 10
    jack        = 11
    queen       = 12
    king        = 13
    ace         = 14


@dataclass(frozen=True)
class CardType:
    suit:SUITS
    rank:RANKS

class Card():

    _nxt_id = 0
    @classmethod
    def _get_id(cls):
        cid = cls._nxt_id
        cls._nxt_id += 1
        return cid
    
    def __init__(self, suit:SUITS, rank:RANKS):
        self.id:int = self._get_id()
        self.type:CardType = CardType(suit, rank)
        self.revealed:bool = False
    
    def __str__(self) -> str:
        return f"{self.type.rank.name} of {self.type.suit.value}"
    
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Card):
            return NotImplemented
        return self.type.rank == other.type.rank
    
    def __lt__(self, other: object) -> bool:
        if not isinstance(other, Card):
            return NotImplemented
        return self.type.rank < other.type.rank
    
    def __gt__(self, other: object) -> bool:
        if not isinstance(other, Card):
            return NotImplemented
        return self.type.rank > other.type.rank
