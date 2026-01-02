from src.card_collections import Deck

#from src.game import Game


def main():
    #game:Game = Game()
    deck = Deck()
    print(deck)
    deck.shuffle()
    print(deck)

if __name__ == '__main__':
    main()