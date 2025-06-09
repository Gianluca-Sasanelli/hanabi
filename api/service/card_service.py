from typing import Optional
from api.repository import CardRepository
from api.models.models import Card
from sqlalchemy.orm import Session


class CardService:
    def __init__(self, db: Session):
        self.card_repo = CardRepository(db)

    async def get_first_card(self) -> Optional[Card]:
        try:
            return self.card_repo.find_by_id(1)
        except Exception:
            return None
