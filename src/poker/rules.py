from collections import Counter

from .card_collections import Hand
from .cards import Card, Ranks, Suits
from .entities import Player


class Logic:
    @staticmethod
    def is_flush(hand: Hand) -> bool:
        cards: list[Card] = hand.getCards()
        if cards == []:
            return False
        first_suit: Suits = cards[0].type.suit
        return all(card.type.suit == first_suit for card in cards)

    @staticmethod
    def is_straight(hand: Hand) -> bool:
        cards: list[Card] = hand.getCards()
        if not cards:
            return False

        # is it a hand of 5 unique cards
        ranks: list[Ranks] = sorted(set(card.type.rank for card in cards))
        if len(ranks) != 5:
            return False

        # is the hand sequential
        if ranks[4] - ranks[0] == 4:
            return True

        # if it is not sequential, does the low-ace rule apply
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

    @staticmethod
    def is_full_house(hand: Hand) -> bool:
        cards: list[Card] = hand.getCards()
        if not cards:
            return False

        counts = Counter(card.type.rank for card in cards)
        return sorted(counts.values()) == [2, 3]

    @staticmethod
    def is_three_of_kind(hand: Hand) -> bool:
        cards: list[Card] = hand.getCards()
        if not cards:
            return False
        counts = Counter(card.type.rank for card in cards)
        return 3 in counts.values() and not Logic.is_full_house(hand)

    @staticmethod
    def is_two_pair(hand: Hand) -> bool:
        cards: list[Card] = hand.getCards()
        if not cards:
            return False
        counts = Counter(card.type.rank for card in cards)
        pair_counts = list(count for count in counts.values() if count == 2)
        return len(pair_counts) == 2

    @staticmethod
    def is_one_pair(hand: Hand) -> bool:
        cards = hand.getCards()
        if len(cards) != 5:
            return False

        counts = Counter(card.type.rank for card in cards).values()
        return sorted(counts) == [1, 1, 1, 2]

    @staticmethod
    def is_high_card(hand: Hand) -> bool:
        # ensure no other hand types are present
        return not (
            Logic.is_one_pair(hand)
            or Logic.is_two_pair(hand)
            or Logic.is_three_of_kind(hand)
            or Logic.is_full_house(hand)
            or Logic.is_four_of_kind(hand)
            or Logic.is_straight(hand)
            or Logic.is_flush(hand)
        )

    @classmethod
    def poker(cls, players) -> Player:
        return max(players, key=cls.calc_hand_rank)

    @classmethod
    def calc_hand_rank(cls, player) -> tuple:
        def order_by_rank_freq(ranks: list[int], lo2hi: bool = False):
            rank_counts: Counter = Counter(ranks)
            return sorted(
                ranks,
                key=lambda x: (-rank_counts[x], -x)
                if not lo2hi
                else (rank_counts[x], x),
            )

        # get the player's hand
        hand: Hand = player.hand

        # Determine if the we even have a complete hand
        if len(player.hand) < 5:
            return (0, 0, 0)

        # get the player's cards and sort them
        cards: list[Card] = sorted(hand.getCards(), reverse=True)
        # get the ranks of the sorted cards (order preserved)
        ranks: list[int] = [card.type.rank.value for card in cards]
        # it is useful to also have the ranks ordered by frequency (hence the helper)
        ranks_by_freq: list[int] = order_by_rank_freq(ranks)
        hand_rank: list

        # DEBUG
        # print(ranks)
        # print(ranks_by_freq)

        ### Straight Flush ###
        if cls.is_flush(hand) and cls.is_straight(hand):
            hand_rank = [8, ranks[0]]
            # check for ace hi/lo
            if ranks == [14, 5, 4, 3, 2]:
                hand_rank[1] = 5
            return tuple(hand_rank)
        elif cls.is_four_of_kind(hand):
            hand_rank = [7, ranks_by_freq[0], ranks_by_freq[-1]]
            return tuple(hand_rank)
        elif cls.is_full_house(hand):
            hand_rank = [6, ranks_by_freq[0], ranks_by_freq[-1]]
            return tuple(hand_rank)
        elif cls.is_flush(hand):
            hand_rank = [5, ranks]
            return tuple(hand_rank)
        elif cls.is_straight(hand):
            hand_rank = [4, ranks[0]]
            return tuple(hand_rank)
        elif cls.is_three_of_kind(hand):
            hand_rank = [3, ranks_by_freq[0], ranks_by_freq[3:]]
            return tuple(hand_rank)
        elif cls.is_two_pair(hand):
            hand_rank = [2, ranks_by_freq[0], ranks_by_freq[2], ranks]
            return tuple(hand_rank)
        elif cls.is_one_pair(hand):
            hand_rank = [1, ranks_by_freq[0], ranks]
            return tuple(hand_rank)
        else:
            hand_rank = [0] + [rank for rank in ranks]
            return tuple(hand_rank)


# main for smoke testing
def main():
    rules: Logic = Logic()

    # Straight Flush
    hand: Hand = Hand.from_str("tc 9c 8c 7c 6c")
    player: Player = Player("Test Name", hand)
    print(player)
    print(rules.calc_hand_rank(player))

    # Four of a kind (smaller kicker)
    hand: Hand = Hand.from_str("qd qs qc qh 7d")
    player.hand = hand
    print("\n" + str(hand))
    print(rules.calc_hand_rank(player))

    # Four of a Kind (larger kicker)
    hand: Hand = Hand.from_str("7d 7s 7c 7h qd")
    player.hand = hand
    print("\n" + str(hand))
    print(rules.calc_hand_rank(player))

    # Four of a Kind
    hand: Hand = Hand.from_str("as ah ad ac qh")
    player.hand = hand
    print("\n" + str(hand))
    print(rules.calc_hand_rank(player))

    # Full House
    hand: Hand = Hand.from_str("8s 8h 8d ks kc")
    player.hand = hand
    print("\n" + str(hand))
    print(rules.calc_hand_rank(player))

    # Flush
    hand: Hand = Hand.from_str("8d 7d 2d kd td")
    player.hand = hand
    print("\n" + str(hand))
    print(rules.calc_hand_rank(player))

    # Straight
    hand: Hand = Hand.from_str("jc ts 9h 8d 7c")
    player.hand = hand
    print("\n" + str(hand))
    print(rules.calc_hand_rank(player))

    # Three of a Kind
    hand: Hand = Hand.from_str("7d, 7h, 7s, 5c, 2h")
    player.hand = hand
    print("\n" + str(hand))
    print(rules.calc_hand_rank(player))

    # Two Pair
    hand: Hand = Hand.from_str("9s 9h 3d 2h 2h")
    player.hand = hand
    print("\n" + str(hand))
    print(rules.calc_hand_rank(player))

    # One pair
    hand: Hand = Hand.from_str("2s 2h jh 6d 3s")
    player.hand = hand
    print("\n" + str(hand))
    print(rules.calc_hand_rank(player))

    # Nada
    # Two Pair
    hand: Hand = Hand.from_str("7s 5h 4d 3c 2h")
    player.hand = hand
    print("\n" + str(hand))
    print(rules.calc_hand_rank(player))


if __name__ == "__main__":
    main()
