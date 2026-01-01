from poker import Deck, Hand


def main():
    deck = Deck()
    print(deck)
    deck.shuffle()
    print(deck)
    hand = Hand()

if __name__ == '__main__':
    main()