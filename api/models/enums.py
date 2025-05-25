from enum import Enum, auto
from typing import Optional, List, Dict, Any
from datetime import datetime
from dataclasses import dataclass




class CardValue(int, Enum):
    ONE = 1
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5

class GameStatus(str, Enum):
    WAITING = "waiting"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    LOST = "lost"

class CardColor(str, Enum):
    """Enum for the color of a card."""
    RED = "Red"
    YELLOW = "Yellow"
    GREEN = "Green"
    BLUE = "Blue"
    WHITE = "White"

class HintType(str, Enum):
    COLOR = "color"
    VALUE = "value"