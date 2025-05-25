from .base_repository import BaseRepository
from models.models import Card, Player, Game, GamePlayer, GameDeck, PlayerHand, DiscardPile, PlayedCard


class CardRepository(BaseRepository[Card]):
    def __init__(self):
        super().__init__("cards", Card)


class PlayerRepository(BaseRepository[Player]):
    def __init__(self):
        super().__init__("players", Player)


class GameRepository(BaseRepository[Game]):
    def __init__(self):
        super().__init__("games", Game)


class GamePlayerRepository(BaseRepository[GamePlayer]):
    def __init__(self):
        super().__init__("game_players", GamePlayer)


class GameDeckRepository(BaseRepository[GameDeck]):
    def __init__(self):
        super().__init__("game_decks", GameDeck)


class PlayerHandRepository(BaseRepository[PlayerHand]):
    def __init__(self):
        super().__init__("player_hands", PlayerHand)


class DiscardPileRepository(BaseRepository[DiscardPile]):
    def __init__(self):
        super().__init__("discard_piles", DiscardPile)


class PlayedCardRepository(BaseRepository[PlayedCard]):
    def __init__(self):
        super().__init__("played_cards", PlayedCard)


__all__ = [
    "BaseRepository",
    "CardRepository",
    "PlayerRepository",
    "GameRepository",
    "GamePlayerRepository",
    "GameDeckRepository",
    "PlayerHandRepository",
    "DiscardPileRepository",
    "PlayedCardRepository",
]
