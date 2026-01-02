from src.poker import Deck


def main():
    deck = Deck()
    print(deck)
    deck.shuffle()
    print(deck)
    hand = Hand()

if __name__ == '__main__':
    main()