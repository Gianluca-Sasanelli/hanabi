from pydantic import BaseModel
from typing import Literal

CardColor = Literal["Red", "Blue", "Yellow", "Green", "White"]
CardValue = Literal[1, 2, 3, 4, 5]
HintType = Literal["color", "number"]

class Card(BaseModel):
    card_id: str
    value: CardValue
    color: CardColor

class Board(BaseModel):
    cards: list[Card]
    num_hints: int
    num_lifes: int
