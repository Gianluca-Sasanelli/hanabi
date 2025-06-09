from uuid import UUID

from sqlalchemy import Integer, String, Boolean, ForeignKey
from sqlalchemy.dialects.postgresql import UUID as SQLUUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Enum

from api.models.enums import CardColor, CardValue, GameStatus
from api.models.base import Base


class Card(Base):
    __tablename__ = "cards"

    color: Mapped[CardColor] = mapped_column(Enum(CardColor), nullable=False)
    value: Mapped[CardValue] = mapped_column(Enum(CardValue), nullable=False)

    game_decks = relationship("GameDeck", back_populates="card")
    player_hands = relationship("PlayerHand", back_populates="card")
    discard_piles = relationship("DiscardPile", back_populates="card")
    played_cards = relationship("PlayedCard", back_populates="card")

    def __str__(self) -> str:
        return f"{self.color.capitalize()} {self.value}"


class User(Base):
    __tablename__ = "users"

    username: Mapped[str] = mapped_column(String, nullable=False)
    email: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String, nullable=False)

    games = relationship("Game", foreign_keys="Game.current_user_id", back_populates="current_user")
    game_players = relationship("GamePlayer", back_populates="user")
    player_hands = relationship("PlayerHand", back_populates="user")

    def __str__(self) -> str:
        return self.username


class Game(Base):
    __tablename__ = "games"

    status: Mapped[GameStatus] = mapped_column(Enum(GameStatus), nullable=False, default=GameStatus.WAITING)
    num_hints: Mapped[int] = mapped_column(Integer, nullable=False, default=8)
    num_lives: Mapped[int] = mapped_column(Integer, nullable=False, default=3)
    current_user_id: Mapped[UUID] = mapped_column(SQLUUID, ForeignKey("users.id"), nullable=False)

    current_user = relationship("User", back_populates="games")
    game_players = relationship("GamePlayer", back_populates="game")
    game_decks = relationship("GameDeck", back_populates="game")
    player_hands = relationship("PlayerHand", back_populates="game")
    discard_piles = relationship("DiscardPile", back_populates="game")
    played_cards = relationship("PlayedCard", back_populates="game")


class GamePlayer(Base):
    __tablename__ = "game_players"

    game_id: Mapped[UUID] = mapped_column(SQLUUID, ForeignKey("games.id"), nullable=False)
    user_id: Mapped[UUID] = mapped_column(SQLUUID, ForeignKey("users.id"), nullable=False)
    user_order: Mapped[int] = mapped_column(Integer, nullable=False)

    game = relationship("Game", back_populates="game_players")
    user = relationship("User", back_populates="game_players")


class GameDeck(Base):
    __tablename__ = "game_decks"

    game_id: Mapped[UUID] = mapped_column(SQLUUID, ForeignKey("games.id"), nullable=False)
    card_id: Mapped[UUID] = mapped_column(SQLUUID, ForeignKey("cards.id"), nullable=False)
    position: Mapped[int] = mapped_column(Integer, nullable=False, default=0)

    game = relationship("Game", back_populates="game_decks")
    card = relationship("Card", back_populates="game_decks")


class PlayerHand(Base):
    __tablename__ = "player_hands"

    game_id: Mapped[UUID] = mapped_column(SQLUUID, ForeignKey("games.id"), nullable=False)
    user_id: Mapped[UUID] = mapped_column(SQLUUID, ForeignKey("users.id"), nullable=False)
    card_id: Mapped[UUID] = mapped_column(SQLUUID, ForeignKey("cards.id"), nullable=False)
    position: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    color_known: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    value_known: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    game = relationship("Game", back_populates="player_hands")
    user = relationship("User", back_populates="player_hands")
    card = relationship("Card", back_populates="player_hands")


class DiscardPile(Base):
    __tablename__ = "discard_piles"

    game_id: Mapped[UUID] = mapped_column(SQLUUID, ForeignKey("games.id"), nullable=False)
    card_id: Mapped[UUID] = mapped_column(SQLUUID, ForeignKey("cards.id"), nullable=False)

    game = relationship("Game", back_populates="discard_piles")
    card = relationship("Card", back_populates="discard_piles")


class PlayedCard(Base):
    __tablename__ = "played_cards"

    game_id: Mapped[UUID] = mapped_column(SQLUUID, ForeignKey("games.id"), nullable=False)
    card_id: Mapped[UUID] = mapped_column(SQLUUID, ForeignKey("cards.id"), nullable=False)

    game = relationship("Game", back_populates="played_cards")
    card = relationship("Card", back_populates="played_cards")
