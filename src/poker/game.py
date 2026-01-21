from .card_collections import Deck, Hand
from .cards import Card, Ranks, Suits
from .entities import Dealer, Player
from .rules import HAND_RANKINGS, Logic


class Game:
    def __init__(self, numPlayers):
        self.rules = Logic()
        self.numPlayers = numPlayers
        self.players: list[Player] = []
        self.dealer = Dealer()
        self.deck = Deck()
        self.init_game()

    def init_game(self) -> None:
        if self.numPlayers < 1:
            raise ValueError("Number of players must be at least 1.")
        if self.numPlayers * 5 > 52:
            raise ValueError("Not enough cards in the deck to deal to all players.")
        hands: list[Hand] = self.dealer.deal(self.numPlayers, 5)
        for hand in hands:
            self.players.append(Player("Player" + str(len(self.players) + 1), hand))

    def reset_game(self) -> None:
        self.players = []
        self.deck = Deck()
        self.init_game()

    def get_players(self) -> list[Player]:
        return self.players

    def get_dealer(self) -> Dealer:
        return self.dealer


# main function for smoke testing (eventually make this the main loop for a CLI game?)
def main():
    straight_flush: list[Card] = [
        Card(suit=Suits.DIAMONDS, rank=Ranks.JACK),
        Card(suit=Suits.DIAMONDS, rank=Ranks.TEN),
        Card(suit=Suits.DIAMONDS, rank=Ranks.NINE),
        Card(suit=Suits.DIAMONDS, rank=Ranks.EIGHT),
        Card(suit=Suits.DIAMONDS, rank=Ranks.SEVEN),
    ]

    test_hand1: Hand = Hand(straight_flush)
    test_player: Player = Player("david", test_hand1)

    rules: Logic = Logic()

    print(test_player.hand)

    print(rules.calc_hand_rank(test_player))

    game: Game = Game(numPlayers=4)
    for player in game.get_players():
        print(player.name + "'s hand:")
        print(player.hand)
        hand_rank = game.rules.calc_hand_rank(player)
        print("Hand Category:", HAND_RANKINGS[hand_rank[0]])
        print("Hand Rank:", hand_rank)
        print()

    print("Dealer's deck has", len(game.get_dealer().deck), "cards remaining.")
    print("Winner(s):", game.rules.poker(game.get_players()))

    print("\nResetting game...\n")
    game.reset_game()
    for player in game.get_players():
        print(player.name + "'s hand:")
        print(player.hand)
        print()


if __name__ == "__main__":
    main()
