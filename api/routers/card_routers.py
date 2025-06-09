from fastapi import APIRouter, Request, HTTPException, Depends
from api.service.card_service import CardService
from api.shared.db_connections import get_postgres_session
from sqlalchemy.orm import Session

router = APIRouter()


@router.get("/card")
async def get_first_card(request: Request, db: Session = Depends(get_postgres_session)):
    card_service = CardService(db)
    card = await card_service.get_first_card()
    print("The card is", card)
    if not card:
        raise HTTPException(status_code=404, detail="Card not found")
    return card
