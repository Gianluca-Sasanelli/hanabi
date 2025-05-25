from dataclasses import dataclass
from typing import Optional
from datetime import datetime
from .enums import *

@dataclass
class Card:
    id: Optional[int] = None
    color: CardColor = CardColor.RED
    value: CardValue = CardValue.ONE
    
    def __str__(self) -> str:
        return f"{self.color.capitalize()} {self.value}"


@dataclass
class Player:
    id: Optional[int] = None
    name: str = ""
    created_at: Optional[datetime] = None
    
    def __str__(self) -> str:
        return self.name


@dataclass
class Game:
    id: Optional[int] = None
    status: GameStatus = GameStatus.WAITING
    num_hints: int = 8
    num_lives: int = 3
    current_player_id: Optional[int] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


@dataclass
class GamePlayer:
    game_id: int
    player_id: int
    player_order: int


@dataclass
class GameDeck:
    id: Optional[int] = None
    game_id: int = 0
    card_id: int = 0
    position: int = 0


@dataclass
class PlayerHand:
    id: Optional[int] = None
    game_id: int = 0
    player_id: int = 0
    card_id: int = 0
    position: int = 0
    color_known: bool = False
    value_known: bool = False

@dataclass
class DiscardPile:
    id: Optional[int] = None
    game_id: int = 0
    card_id: int = 0    

@dataclass
class PlayedCard:
    id: Optional[int] = None
    game_id: int = 0
    card_id: int = 0
    