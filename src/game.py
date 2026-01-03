from .card_collections import Deck, Hand
from .entities import Dealer, Player


class Game():
    _player_id = 0
    def __init__(self, numPlayers):
        self.numPlayers = numPlayers
        self.players:list[Player] = []
        self.dealer = Dealer()
        self.deck = Deck()
        self.init_players()

    def init_players(self) -> None:
        for i in range(self.numPlayers):
            self.players.append(Player(str(i), Hand()))

    def poker(self) -> Player:
        return max(self.players, key=self.calc_hand_rank)
    
    def calc_hand_rank(self, player):
        #TODO: Calculate the rank of a given player's hand
        # Need to determine the best way to represent the rank
        # There are 9 types of hand ranks that can be scored from 0 to 9
        # However there are also rules for ties within the same rank
        # This is the part that is going to be tricky
        hand:Hand = player.hand

        raise NotImplementedError
