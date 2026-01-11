from random import choice, randint, sample, shuffle

from poker.card_collections import Hand
from poker.cards import SUIT_ABBR


# --- Helpers Methods for Testing ---
class TestUtils:
    SUITS = list(SUIT_ABBR.keys())
    RANK_CHAR = {10: "T", 11: "J", 12: "Q", 13: "K", 14: "A"}

    @classmethod
    def make_hand(cls, cards: list[str]) -> Hand:
        return Hand.from_str_list(cards)

    @classmethod
    def rank_to_char(cls, rank: int) -> str:
        """2..14 -> '2'..'9','T','J','Q','K','A'"""
        return cls.RANK_CHAR.get(rank, str(rank))

    @classmethod
    def random_suit(cls) -> str:
        return choice(cls.SUITS)

    @classmethod
    def gen_random_hand(cls) -> list[str]:
        deck = [r + s for r in "23456789TJQKA" for s in cls.SUITS]
        return sample(deck, 5)

    @classmethod
    def gen_random_royal_flush(cls) -> list[str]:
        suit = cls.random_suit()
        ranks = ["T", "J", "Q", "K", "A"]
        return [r + suit for r in ranks]

    @classmethod
    def gen_random_straight_flush(cls) -> list[str]:
        suit = cls.random_suit()

        # start_rank 2..10 gives 5-card straight up to A-high (10,J,Q,K,A)
        start = randint(2, 10)
        ranks = [cls.rank_to_char(r) for r in range(start, start + 5)]
        return [r + suit for r in ranks]

    @classmethod
    def gen_random_four_of_a_kind(cls) -> list[str]:
        suit_chars = list(SUIT_ABBR.keys())

        quad_rank = randint(2, 14)
        quad_rank_char = cls.rank_to_char(quad_rank)
        four_cards = [quad_rank_char + s for s in suit_chars]  # all 4 suits

        kicker_rank = randint(2, 14)
        while kicker_rank == quad_rank:  # <-- fill in / keep this
            kicker_rank = randint(2, 14)

        kicker = cls.rank_to_char(kicker_rank) + choice(suit_chars)
        four_cards.append(kicker)
        return four_cards

    @classmethod
    def gen_random_full_house(cls) -> list[str]:
        suit_chars = list(SUIT_ABBR.keys())

        trip_rank = randint(2, 14)
        trip_rank_char = cls.rank_to_char(trip_rank)
        trip_suits = sample(suit_chars, 3)
        three_cards = [trip_rank_char + s for s in trip_suits]

        pair_rank = randint(2, 14)
        while pair_rank == trip_rank:
            pair_rank = randint(2, 14)

        pair_rank_char = cls.rank_to_char(pair_rank)
        pair_suits = sample(suit_chars, 2)
        two_cards = [pair_rank_char + s for s in pair_suits]

        return three_cards + two_cards

    @classmethod
    def gen_random_flush(cls) -> list[str]:
        """
        Generate a flush that is NOT a straight flush.
        """
        suit = cls.random_suit()

        while True:
            # choose 5 distinct ranks
            ranks_int = sample(range(2, 15), 5)
            ranks_int.sort()
            # avoid wheel/broadway/any straight patterns
            is_straight = (
                ranks_int[-1] - ranks_int[0] == 4 and len(set(ranks_int)) == 5
            ) or (ranks_int == [2, 3, 4, 5, 14])
            if is_straight:
                continue

            ranks = [cls.rank_to_char(r) for r in ranks_int]
            return [r + suit for r in ranks]

    @classmethod
    def gen_random_straight(cls) -> list[str]:
        """
        Generate a straight that is NOT a straight flush.
        (Also avoids accidental flush.)
        """
        start = randint(2, 10)
        ranks = [cls.rank_to_char(r) for r in range(start, start + 5)]

        # Pick suits; ensure not all suits are the same.
        suits = [cls.random_suit() for _ in range(5)]
        if len(set(suits)) == 1:
            # force at least one card to a different suit
            suits[0] = choice([s for s in cls.SUITS if s != suits[0]])

        cards = [r + s for r, s in zip(ranks, suits)]
        return cards

    @classmethod
    def gen_random_three_of_a_kind(cls) -> list[str]:
        suit_chars = list(SUIT_ABBR.keys())

        trip_rank = randint(2, 14)
        trip_rank_char = cls.rank_to_char(trip_rank)
        trip_suits = sample(suit_chars, 3)
        three_cards = [trip_rank_char + s for s in trip_suits]

        kicker_ranks = sample([r for r in range(2, 15) if r != trip_rank], 2)
        kicker_chars = [cls.rank_to_char(r) for r in kicker_ranks]
        kicker_cards = [rc + cls.random_suit() for rc in kicker_chars]

        return three_cards + kicker_cards

    @classmethod
    def gen_random_two_pair(cls) -> list[str]:
        suit_chars = cls.SUITS[:]

        while True:
            pair_ranks = sample(range(2, 15), 2)
            pair_chars = [cls.rank_to_char(r) for r in pair_ranks]

            pair_cards = []
            for pc in pair_chars:
                pair_suits = sample(suit_chars, 2)
                pair_cards.extend([pc + s for s in pair_suits])

            # choose 1 kicker rank different from both pair ranks
            kicker_rank = choice([r for r in range(2, 15) if r not in pair_ranks])
            kicker_char = cls.rank_to_char(kicker_rank)
            kicker_card = kicker_char + cls.random_suit()

            cards = pair_cards + [kicker_card]
            shuffle(cards)

            # --- filters to avoid accidentally creating other categories ---
            # Avoid flush (all suits same)
            if len({c[1] for c in cards}) == 1:
                continue

            return cards

    @classmethod
    def gen_random_one_pair(cls) -> list[str]:
        """
        Generate exactly ONE pair (not two pair, not trips, not full house),
        and avoid accidental flush/straight.
        """
        suit_chars = cls.SUITS[:]

        while True:
            pair_rank = randint(2, 14)
            pair_rank_char = cls.rank_to_char(pair_rank)

            # pick 2 distinct suits for the pair
            pair_suits = sample(suit_chars, 2)
            pair_cards = [pair_rank_char + s for s in pair_suits]

            # choose 3 kicker ranks all distinct and different from pair_rank
            kicker_ranks = sample([r for r in range(2, 15) if r != pair_rank], 3)
            kicker_chars = [cls.rank_to_char(r) for r in kicker_ranks]

            # assign random suits to kickers (can repeat suits; just avoid forming a flush)
            kicker_cards = [rc + cls.random_suit() for rc in kicker_chars]

            cards = pair_cards + kicker_cards
            shuffle(cards)

            return cards

    @classmethod
    def gen_random_high_card(cls) -> list[str]:
        while True:
            ranks_int = sample(range(2, 15), 5)
            ranks_int.sort()
            # avoid straight patterns
            is_straight = (
                ranks_int[-1] - ranks_int[0] == 4 and len(set(ranks_int)) == 5
            ) or (ranks_int == [2, 3, 4, 5, 14])
            if is_straight:
                continue

            ranks = [cls.rank_to_char(r) for r in ranks_int]
            cards = [r + cls.random_suit() for r in ranks]

            # avoid flush
            if len({c[1] for c in cards}) == 1:
                continue

            return cards
