from typing import Optional
from repository import CardRepository
from models.models import Card


class CardService:
    def __init__(self):
        self.card_repo = CardRepository()

    async def get_first_card(self) -> Optional[Card]:
        try:
            return self.card_repo.find_by_id(1)
        except Exception:
            return None
