import pytest

from poker.game import Game


@pytest.fixture
def game() -> Game:
    return Game(numPlayers=4)


@pytest.mark.parametrize("num_players", [2, 3, 4, 5, 6, 1])
def test_game_player_count(num_players: int):
    game: Game = Game(numPlayers=num_players)
    assert len(game.get_players()) == num_players


def test_game_with_invalid_player_count():
    with pytest.raises(ValueError):
        Game(numPlayers=0)
    with pytest.raises(ValueError):
        Game(numPlayers=11)


def test_game_initialization(game: Game):
    assert len(game.get_players()) == 4
    for player in game.get_players():
        assert player.hand is not None
        assert len(player.hand.getCards()) == 5


def test_dealer_deck_size(game: Game):
    dealer = game.get_dealer()
    assert len(dealer.deck) == 52 - (4 * 5)  # 52 cards minus dealt cards


def test_game_reset(game: Game):
    original_players = game.get_players().copy()
    game.reset_game()
    new_players = game.get_players()
    assert len(new_players) == 4
    for original, new in zip(original_players, new_players):
        assert (
            original.name != new.name or original.hand != new.hand
        )  # Ensure hands are different after reset


def test_player_ids_unique(game: Game):
    player_ids = [player.id for player in game.get_players()]
    assert len(player_ids) == len(set(player_ids))  # All player IDs should be unique


if __name__ == "__main__":
    pytest.main()
