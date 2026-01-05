
from src.cards import Card
from src.game import Game


def main():
    game:Game = Game(1)
    print(f"Deck:\n{game.deck}")
    card:Card|None = game.deck.draw_top()
    if card:
        game.players[0].hand.add_card(card)
    print("Player hand:")
    game.rules.poker(game.players)

if __name__ == '__main__':
    main()