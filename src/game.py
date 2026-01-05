from .card_collections import Deck, Hand
from .cards import RANKS, SUITS, Card
from .entities import Dealer, Player


class Game():
    _player_id = 0
    def __init__(self, numPlayers):
        self.rules = Logic()
        self.numPlayers = numPlayers
        self.players:list[Player] = []
        self.dealer = Dealer()
        self.deck = Deck()
        self.init_players()

    def init_players(self) -> None:
        for i in range(self.numPlayers):
            self.players.append(Player(str(i), Hand([])))

class Logic():
    @classmethod
    def poker(cls, players) -> Player:
        return max(players, key=cls.calc_hand_rank)
    
    @classmethod
    def calc_hand_rank(cls, player):
        #TODO: Calculate the rank of a given player's hand
        # Need to determine the best way to represent the rank
        # There are 9 types of hand ranks that can be scored from 0 to 9
        # However there are also rules for ties within the same rank
        # This is the part that is going to be tricky
        #hand:Hand = player.hand

        raise NotImplementedError
    
    @staticmethod
    def is_flush(hand:Hand) -> bool:
        cards:list[Card] = hand.getCards()
        if cards == []:
            return False
        first_suit:SUITS = cards[0].type.suit
        return all(card.type.suit == first_suit for card in cards)
    
    @staticmethod
    def is_straight(hand:Hand) -> bool:
        cards:list[Card] = hand.getCards()
        if not cards:
            return False
        
        ranks:list[RANKS] = sorted(set(card.type.rank for card in cards))
        
        if len(ranks) != 5:
            return False
        
        if ranks[4] - ranks[0] == 4:
            return True
        
        if ranks == [2, 3, 4, 5, 14]:
            return True
        
        return False

# main function for smoke testing
def main():
    ace_d = Card(suit=SUITS.diamonds, rank=RANKS.ace)
    two_d = Card(suit=SUITS.diamonds, rank=RANKS.two)
    three_d = Card(suit=SUITS.diamonds, rank=RANKS.three)
    four_d = Card(suit=SUITS.diamonds, rank=RANKS.four)
    five_d = Card(suit=SUITS.diamonds, rank=RANKS.five)
    cards:list[Card] = [ace_d, two_d, three_d, four_d, five_d]

    straight:Hand = Hand(cards)
    flush:Hand = Hand(cards)

    rules:Logic = Logic()
    assert rules.is_flush(flush)
    assert rules.is_straight(straight)

if __name__ == '__main__':
    main()