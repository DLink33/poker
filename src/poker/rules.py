from collections import Counter

from .card_collections import Hand
from .cards import RANKS, SUITS, Card
from .entities import Player


class Logic():
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

    @staticmethod
    def is_four_of_kind(hand: Hand) -> bool:
        cards: list[Card] = hand.getCards()
        if not cards:
            return False

        counts = Counter(card.type.rank for card in cards)
        return 4 in counts.values()

    @classmethod
    def poker(cls, players) -> Player:
        return max(players, key=cls.calc_hand_rank)
    
    @classmethod
    def calc_hand_rank(cls, player):
        hand: Hand = player.hand
        if (len(player.hand) < 5):
            return (0,0,0)
        hand_rank:list[int] = []
        cards:list[Card] = sorted(hand.getCards(),reverse=True)
        
        ### Straight Flush ###
        if cls.is_flush(hand) and cls.is_straight(hand):
            hand_rank = [9]
            # check for ace hi/lo
            ranks:list[int] = sorted(set(card.type.rank.value for card in cards))
            return ranks
            hand_rank.append(cards[0].type.rank.value)
        ### Four of a Kind ###
        # if cls.is_four_of_kind(hand):
        #     hand_rank = 

        return hand_rank
            
        

        #TODO: Calculate the rank of a given player's hand
        # Need to determine the best way to represent the rank
        # There are 9 types of hand ranks that can be scored from 0 to 9
        # However there are also rules for ties within the same rank
        # This is the part that is going to be tricky
        #hand:Hand = player.hand

        raise NotImplementedError