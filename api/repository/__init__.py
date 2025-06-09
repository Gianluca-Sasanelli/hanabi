from api.repository.base_repository import BaseRepository
from api.models.models import Card, User, Game, GamePlayer, GameDeck, PlayerHand, DiscardPile, PlayedCard
from api.shared.db_connections import get_postgres_session
from sqlalchemy.orm import Session


class CardRepository(BaseRepository[Card]):
    def __init__(self, db: Session):
        super().__init__(db, Card)


class UserRepository(BaseRepository[User]):
    def __init__(self, db: Session):
        super().__init__(db, User)


class GameRepository(BaseRepository[Game]):
    def __init__(self, db: Session):
        super().__init__(db, Game)


class GamePlayerRepository(BaseRepository[GamePlayer]):
    def __init__(self, db: Session):
        super().__init__(db, GamePlayer)


class GameDeckRepository(BaseRepository[GameDeck]):
    def __init__(self, db: Session):
        super().__init__(db, GameDeck)


class PlayerHandRepository(BaseRepository[PlayerHand]):
    def __init__(self, db: Session):
        super().__init__(db, PlayerHand)


class DiscardPileRepository(BaseRepository[DiscardPile]):
    def __init__(self, db: Session):
        super().__init__(db, DiscardPile)


class PlayedCardRepository(BaseRepository[PlayedCard]):
    def __init__(self, db: Session):
        super().__init__(db, PlayedCard)


__all__ = [
    "BaseRepository",
    "CardRepository",
    "UserRepository",
    "GameRepository",
    "GamePlayerRepository",
    "GameDeckRepository",
    "PlayerHandRepository",
    "DiscardPileRepository",
    "PlayedCardRepository",
]
