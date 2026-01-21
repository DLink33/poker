from dataclasses import dataclass
from enum import Enum, IntEnum, unique


@unique
class Suits(Enum):
    CLUBS = "♣"
    DIAMONDS = "♦"
    HEARTS = "♥"
    SPADES = "♠"


@unique
class Ranks(IntEnum):
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    SIX = 6
    SEVEN = 7
    EIGHT = 8
    NINE = 9
    TEN = 10
    JACK = 11
    QUEEN = 12
    KING = 13
    ACE = 14


SUIT_ABBR: dict[str, Suits] = {
    "C": Suits.CLUBS,
    "D": Suits.DIAMONDS,
    "H": Suits.HEARTS,
    "S": Suits.SPADES,
}

RANK_ABBR: dict[str, Ranks] = {
    "2": Ranks.TWO,
    "3": Ranks.THREE,
    "4": Ranks.FOUR,
    "5": Ranks.FIVE,
    "6": Ranks.SIX,
    "7": Ranks.SEVEN,
    "8": Ranks.EIGHT,
    "9": Ranks.NINE,
    "T": Ranks.TEN,
    "J": Ranks.JACK,
    "Q": Ranks.QUEEN,
    "K": Ranks.KING,
    "A": Ranks.ACE,
}


@dataclass(frozen=True)
class CardType:
    suit: Suits
    rank: Ranks


@dataclass
class Card:
    _nxt_id = 0

    @classmethod
    def _get_id(cls):
        cid = cls._nxt_id
        cls._nxt_id += 1
        return cid

    @staticmethod
    def suit_and_rank_from_str(card_str: str) -> tuple[Suits | None, Ranks | None]:
        n: int = len(card_str)
        if n != 2:
            return (None, None)

        rank_char: str = card_str[0].upper()
        suit_char: str = card_str[1].upper()

        s = SUIT_ABBR.get(suit_char)
        r = RANK_ABBR.get(rank_char)

        return (s, r)

    @classmethod
    def from_str(cls, card_str) -> "Card":
        s, r = cls.suit_and_rank_from_str(card_str)
        if s is None or r is None:
            raise TypeError(f"Cannot create card from card_str: {card_str}")
        return cls(suit=s, rank=r)

    def __init__(self, suit: Suits, rank: Ranks):
        self.id: int = self._get_id()
        self.type: CardType = CardType(suit, rank)
        self.revealed: bool = False

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

    def __hash__(self) -> int:
        return hash((self.type.suit, self.type.rank, self.id))


# main for smoke testing
def main():
    print("Card creation suit and rank:")
    ace_of_spades: Card = Card(suit=Suits.SPADES, rank=Ranks.ACE)
    print(ace_of_spades)

    print("Card creation from string:")
    ace_of_diamonds: Card = Card.from_str("AD")
    print(ace_of_diamonds)


if __name__ == "__main__":
    main()
