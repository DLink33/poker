
from .card_collections import Deck, Hand
from .cards import Card, Ranks, Suits
from .entities import Dealer, Player
from .rules import Logic


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
   

# main function for smoke testing
def main():
    straight_flush:list[Card] = [
        Card(suit=Suits.DIAMONDS, rank=Ranks.JACK),
        Card(suit=Suits.DIAMONDS, rank=Ranks.TEN),
        Card(suit=Suits.DIAMONDS, rank=Ranks.NINE),
        Card(suit=Suits.DIAMONDS, rank=Ranks.EIGHT),
        Card(suit=Suits.DIAMONDS, rank=Ranks.SEVEN) 
    ]

    test_hand1:Hand = Hand(straight_flush)
    test_player:Player = Player("david", test_hand1)
    
    rules:Logic = Logic()
    
    print(test_player.hand)

    print(rules.calc_hand_rank(test_player))



if __name__ == '__main__':
    main()